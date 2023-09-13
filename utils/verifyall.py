#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from api.v1 import crud
from api.v1.database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from api.v1.schemas import ReadUser

#创建数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # 生成密钥 openssl rand -hex 32
ALGORITHM = "HS256"  # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期分钟

class Token(BaseModel):
    """返回给用户的Token"""
    access_token: str
    token_type: str

class User(BaseModel):#请求格式
    nickname: str
    email: Optional[str] = None
    status: Optional[bool] = None



class UserInDB(User):#入库格式
    password: str
    

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#密码加密

pwd_context = CryptContext(
        schemes=["sha256_crypt", "md5_crypt", "des_crypt"]
    )

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/yushu/v1/jwt/token")#获取tokenurl路径

def verify_password(plain_password: str, head_password: str):
    """
    对密码进行效验
    """
    return pwd_context.verify(plain_password,head_password)

def jwt_get_user(db, username: str):
    user = crud.get_user(db=db,email=username)
    # user_dict={"nickname":user.nickname,"email":user.email,"status":user.status,"password":user._password}
    if user:
        group_detail = crud.get_group(db=db,groupname=user.role)#获取当前的角色的权限
        if group_detail:
            user.group_detail = group_detail.UserPrivileges#将权限列加入到User
        return user
        
def jwt_authenticate_user(db, username: str, password: str):#验证用户信息
    user = jwt_get_user(db = db,username = username)
    if not user:
        return False
    if not verify_password(plain_password=password,head_password=user._password):
        return False
    return user
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):#创建token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def jwt_get_current_user(token: str = Depends(oauth2_schema),db:Session = Depends(get_db)):#获取当前用户
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = jwt_get_user(db=db, username=username)
    if not user:
        raise credentials_exception
    return user


def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):#获取活跃用户
    if current_user.status == "1":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    #delattr(current_user,'_password')#删除password类属性
    return current_user
