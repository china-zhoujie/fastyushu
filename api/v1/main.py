from fastapi import APIRouter, Depends, Request, status, HTTPException, Query
from typing import Optional, List, Union
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from api.v1 import crud, schemas
from api.v1.database import engine, Base, SessionLocal
from utils.response import SuccessResponse, ErrorResponse
from utils.tojson import MyEncoder
from utils.verifyall import *
import json
#from api.v1.models import City, Data


application = APIRouter()


#将模型映射到数据库中
Base.metadata.create_all(bind=engine)

#创建数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def count_start(page: int):#计算起始
    return (page-1) * 50

@application.get("/search",status_code=status.HTTP_200_OK)#查询书籍
async def book(keyword: Optional[str] = None, isbn: Optional[str] = None,page: int = 1, limit: int = 50, db:Session = Depends(get_db)):
    data,count = crud.get_book(db,keyword = "%"+keyword.strip()+"%" if keyword else keyword,isbn = isbn.strip() if isbn else isbn,skip = count_start(page),limit=limit)
    bookdata = dict(
        books=[crud._cut_book_data(i) for i in data],
        count=count
    )
    return bookdata
    
@application.get("/book_detail",status_code = status.HTTP_200_OK)#书籍详情
async def book_detail(isbn: Optional[str], db:Session = Depends(get_db)):
    book_detail,count = crud.get_book_detail(db,isbn=isbn)
    print(book_detail)
    return dict(
        books = [crud._cut_book_data(book_detail)],
        count = count
    )

@application.post("/create_user",response_model = schemas.ReadUser)#创建用户
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user_data = crud.get_user(db=db,email = user.email)
    if user_data:
        raise HTTPException(status_code=400,detail="User already exists")
    return crud.create_user(db=db,user=user)
    
@application.post("/create_group",response_model = schemas.ReadGroup)#创建角色
async def create_group(request: Request, group: schemas.CreateGroup, db: Session = Depends(get_db), current_user: User = Depends(jwt_get_current_active_user)):
    route = str(request.url).split('/')[-1]#获取当前路由
    #print(route,current_user.group_detail)
    if route not in (current_user.group_detail).split(';'):#判断路由是否在权限中
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    get_group = crud.get_group(db=db,groupname=group.UserGroupName)
    if get_group:
        raise HTTPException(status_code=400,detail="User already exists")
    return crud.create_group(db=db,group=group)
    
    
@application.get("/items/")
async def read_items(q: str = Query(default=None, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@application.post("/jwt/token")#创建TOken
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = jwt_authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
@application.get("/jwt/users/me",response_model = schemas.ReadUser)#测试通过token获取用户信息
async def jwt_read_users_me(current_user: User = Depends(jwt_get_current_active_user)):
    return current_user
    
@application.post("/current_gift",response_model = schemas.ReadUser)#赠送礼物接口
async def current_user(isbn: Optional[str], user_data: User = Depends(jwt_get_current_active_user), db:Session =Depends(get_db)):
    
    # uid = crud.get_user(db=db,email=user_data.email).id if crud.get_book(db=db,isbn=isbn) else HTTPException(status_code=400,detail="Book is no exists")
    if crud.get_book(db=db,isbn=isbn,union=True):
        if crud.get_gift(db=db,isbn=isbn,uid=user_data.id):
            raise HTTPException(status_code=400, detail="This user has been given this book")
        else: 
            return crud.create_gift(db=db,uid=user_data.id,isbn=isbn)
    else:
        raise HTTPException(status_code=400, detail="This book does not exist")
        
    # return HTTPException(status_code=400,detail="gfift is exists") if crud.get_gfift(db=db,isbn=isbn,uid=uid) else crud.create_gfift(db=db,uid=uid,isbn=isbn)
    