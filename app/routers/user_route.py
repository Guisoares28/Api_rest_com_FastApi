from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.crud.user_crud import UserUseCases
from app.database import get_db
from app.depends import token_verifier
from app.models.classes_modelos import Usuario
from app.schemas.user_schema import UserResponse, UserCreate

router = APIRouter(prefix="/user")

@router.post("/register", response_model=UserResponse, status_code=200)
def register_new_user(user:UserCreate, db:Session = Depends(get_db)):
    uc = UserUseCases(db=db)
    return uc.user_register(user=user)

@router.post("/login", status_code=200)
def login(login_request_form: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    uc = UserUseCases(db=db)

    user = Usuario(
        usuario = login_request_form.username,
        senha = login_request_form.password
    )
    token = uc.user_login(user=user)
    return JSONResponse(
        content=token,
        status_code= 200
    )
