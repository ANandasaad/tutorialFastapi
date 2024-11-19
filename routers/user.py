from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated, List
import  models
from Database.database import  engine, get_db
from Schema.blog import ShowUser,User

user= APIRouter()


db_dependency= Annotated[Session, Depends(get_db)]
@user.get('/user/{id}', response_model=ShowUser, status_code=200, tags=['users'])
def get_user(id: int , db:db_dependency):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User is not found by this id {id}')

    return user

@user.get("/users", response_model=List[ShowUser], status_code=200, tags=['users'])
def get_users(db:db_dependency):
    users=db.query(models.User).all()
    return users

pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")
@user.post("/user", response_model=ShowUser,status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request:User, db:db_dependency):
    hashedPassword= pwd_cxt.hash(request.password)
    new_user=models.User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user