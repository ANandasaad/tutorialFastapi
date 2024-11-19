from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
from Database.database import get_db
from Schema.blog import Login
from hashing import verify_password
from tokens import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

auth= APIRouter(
    tags=['auth']
)
db_dependency= Annotated[Session, Depends(get_db)]

@auth.post("/login")
def login(request:Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):
    user=db.query(models.User).filter(models.User.email== request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentails')
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect Password')
    # access_token_expires= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token= create_access_token(
        data={'sub':user.email}
    )
    return {'access_token':access_token, "token_type":"bearer"}