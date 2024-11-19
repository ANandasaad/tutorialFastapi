from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session

from Database.database import engine, get_db
from OAuth2 import get_current_user
from Schema.blog import ShowBlog, Blog,User
import  models
blog_router=APIRouter(
    tags=['blogs']
)

db_dependency= Annotated[Session, Depends(get_db)]

@blog_router.get('/blog')
def blog(db:db_dependency, current_user: User= Depends(get_current_user)):
    get_blogs= db.query(models.Blog).all()
    return get_blogs


@blog_router.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db:db_dependency ,current_user: User= Depends(get_current_user)):
    new_blog= models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'data':new_blog}


@blog_router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:Blog , db:db_dependency, current_user: User= Depends(get_current_user)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
    blog=db.query(models.Blog).filter(models.Blog.id==id).update({'title':request.title})
    db.commit()
    return blog

@blog_router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:db_dependency, current_user: User= Depends(get_current_user)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
    db.query(models.Blog).filter(models.Blog.id== id).delete()
    db.commit()
    return {'done'}


@blog_router.get('/blog/{id}', status_code=200, response_model=ShowBlog)
def show(id,response:Response,db:db_dependency, current_user: User= Depends(get_current_user)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}
    return blog