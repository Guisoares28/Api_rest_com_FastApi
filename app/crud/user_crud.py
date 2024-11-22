from datetime import datetime, timezone, timedelta


from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.exception.user_exception import UserException
from app.models.classes_modelos import Usuario
from app.schemas.user_schema import UserCreate
from jose import jwt, JWTError, ExpiredSignatureError

crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = 'chave-secreta'
ALGORITHM = 'HS256'


class UserUseCases:
    def __init__(self, db:Session):
        self.db = db

    def user_register(self, user:UserCreate):
        new_user = Usuario(
            usuario = user.usuario,
            senha = crypt_context.hash(user.senha)
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def user_login(self, user:Usuario, expires_in: int = 30):
        user_on_db = self.db.query(Usuario).filter_by(usuario=user.usuario).first()

        if not user_on_db:
            raise UserException("Usuario não encontrado")

        if not crypt_context.verify(user.senha, user_on_db.senha):
            raise UserException("Usuario não encontrado")

        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        exp_timestamp = int(exp.timestamp())
        payload = {
            "sub":user.usuario,
            'exp':exp_timestamp
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": access_token,
            "exp": exp_timestamp
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return data
        except ExpiredSignatureError:
            raise UserException("Token expirado")
        except JWTError:
            raise UserException("Token inválido")