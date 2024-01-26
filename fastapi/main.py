
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, status,Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import db
import models
import models2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth
from typing import Optional

from datetime import datetime, timedelta

from typing import Annotated

# from jose import JWTError, jwt
from passlib.context import CryptContext


app= FastAPI()
origins=(
    "http://localhost:3000"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
@app.get("/all")
def get_all():
    data=db.all()
    return data

@app.post("/create")
def create(data:models.notes):
    id=db.create(data)
    return {"inserted": True, "inserted_id":id}

@app.get("/get")
def get_one(title:str):
    data=db.get_one(title)
    return data

@app.delete("/delete/{id}")
def delete(id):
    data=db.delete(id)
    return {"deleted":True, "deleted_count":data}

@app.put("/update/{id}")
def update(id, data:models.notes):
    a=db.update(id,data)
 
    return {"updated": True,"modified":a}
    


# SIGNUP
class User(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    disabled: bool

@app.post("/signup")
async def register_user(user_data: models2.notes):
    
    hashed_password = db.get_password_hash(user_data.password)

  
    new_user = User(
        username=user_data.username,
        full_name=user_data.name,
        email=user_data.email,
        disabled=False,
        hashed_password=hashed_password,
        

    )
    db.collection2.insert_one(dict(new_user))
   

    return new_user

# authentication


@app.post("/token", response_model=auth.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = auth.authenticate_user(db.collection2, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

