from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db, User
from sqlalchemy.orm import Session

from authentication.hash import Hash
from models.user import UserLoginSchema, UserSchema
from authentication.jwt_handler import signJWT

user_router = APIRouter(tags=["User"])

@user_router.post("/register")
def register(user:UserSchema ,db:Session=Depends(get_db)):
        check_nim = db.query(User).filter(User.nim==user.nim).first()
        check_email = db.query(User).filter(User.email==user.email).first()
        if check_nim is not None:
                return {"Error":"Nim tersebut sudah terdaftar"}
        elif check_email is not None:
                return {"Error":"Email tersebut sudah terdaftar"}
        else:
                new_user=User(password=Hash.bcrypt(user.password),email=user.email,nim=user.nim)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
        
@user_router.post("/login")
def login(login:UserLoginSchema ,db:Session=Depends(get_db)):
        user=db.query(User).filter(User.email==login.email).first()
        if user is None:
                return  {"Error":"email belum terdaftar"}
        else:
                if Hash.verify(user.password, login.password):
                        return signJWT(user.email)
                else:
                        return {"Error":"Password dan Email tidak sesuai"}