from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.crud.user_crud import UserUseCases
from app.database import get_db


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

def token_verifier(db:Session=Depends(get_db), token=Depends(oauth_scheme)):
    uc = UserUseCases(db=db)
    uc.verify_token(access_token=token)


