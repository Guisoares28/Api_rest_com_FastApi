from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.exception.user_exception import UserException
from app.models.classes_modelos import Usuario
from app.schemas.user_schema import UserCreate
from jose import jwt, JWTError

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

    def user_login(self, user:Usuario, expires_in =  30):
        user_on_db = self.db.query(Usuario).filter_by(usuario=user.usuario).first()

        if not user_on_db:
            raise UserException("Usuario não encontrado")

        if not crypt_context.verify(user.senha, user_on_db.senha):
            raise UserException("Usuario não encontrado")

        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        payload = {
            "sub":user.usuario,
            'exp':exp
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "acess_token": token,
            "exp": exp.isoformat()
        }