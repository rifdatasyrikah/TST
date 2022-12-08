from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db, User
from sqlalchemy.orm import Session

from authentication.hash import Hash
from models.user import UserLoginSchema, UserSchema
from authentication.jwt_handler import signJWT

user_router = APIRouter(tags=["User"])

@user_router.post("/register")
def register(user:UserSchema ,db:Session=Depends(get_db)):
        new_user=User(password=Hash.bcrypt(user.password),email=user.email,nim=user.nim)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

@user_router.post("/login")
def login(login:UserLoginSchema ,db:Session=Depends(get_db)):
        user=db.query(User).filter(User.email==login.email).first()
        if Hash.verify(user.password, login.password):
                return signJWT(user.email)
        else:
                return {"Error":"Password dan Email tidak sesuai"}