from typing import  Annotated

import uvicorn

from fastapi import FastAPI

from Database.database import engine
from routers.user import user
from routers.blog import blog_router as blog
from routers.auth import auth
import models
app= FastAPI()


app.include_router(user)
app.include_router(blog)
app.include_router(auth)
models.Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)