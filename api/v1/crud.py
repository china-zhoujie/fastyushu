#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from api.v1 import models, schemas
from typing import Optional


def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.province == name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).offset(skip).limit(limit).all()
    
def get_gift(db: Session, isbn: str, uid: str):
    return db.query(models.Gift).filter(models.Gift.isbn == isbn,models.Gift.uid == uid)


def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def create_group(db: Session, group: schemas.CreateGroup):
    db_group = models.Group(**group.dict())
    db_group.UserPrivileges = ';'.join(db_group.UserPrivileges) if len(db_group.UserPrivileges) > 1 else db_group.UserPrivileges
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group
    
def create_gift(db: Session, uid: str, isbn: str, launched: Optional[int]=0):
    gfift = {"uid":uid,"isbn":isbn,"launched":launched}
    print(gfift)
    db_gfift = models.Gift(**gfift)
    db.add(db_gfift)
    db.commit()
    db.refresh(db_gfift)
    return db_gfift

def get_book(db: Session, keyword: str = None, isbn: str = None, skip: int = 0, limit: int = 10, union=False):
    if keyword:
        bookdata,count = db.query(models.Book).filter(or_(models.Book.title.like(keyword),models.Book.author.like(keyword),models.Book.publisher.like(keyword))).offset(skip).limit(limit).all(),db.query(models.Book).filter(or_(models.Book.title.like(keyword),models.Book.author.like(keyword),models.Book.publisher.like(keyword))).count()
        return bookdata,count
    if isbn and union:
        bookdata= db.query(models.Book).filter(models.Book.isbn==isbn).all()
        return bookdata
    if isbn:
        bookdata,count = db.query(models.Book).filter(models.Book.isbn==isbn).all(),db.query(models.Book).filter(models.Book.isbn==isbn).count()
        return bookdata,count
    bookdata,count = db.query(models.Book).offset(skip).limit(limit).all(),db.query(models.Book).count()
    return bookdata,count
    
def get_book_detail(db: Session, isbn: str):
    #book_detail = db.query(func.count(models.Book.id)).filter(models.Book.isbn == isbn).scalar()#获取查询条数
    bookdata,count = db.query(models.Book).filter(models.Book.isbn == isbn).first(),db.query(models.Book).filter(models.Book.isbn == isbn).count()
    return bookdata,count
    
    
def get_data_count(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
        return db.query(models.Data).filter(models.Data.city.has(province=city)).count()  # 外键关联查询，这里不是像Django ORM那样Data.city.province
    return db.query(models.Data).count()
    
def get_group(db: Session, groupname: str):
    return db.query(models.Group).filter(models.Group.UserGroupName == groupname).first()


# def create_city_data(db: Session, data: schemas.CreateData, city_id: int):
#     db_data = models.Data(**data.dict(), city_id=city_id)
#     db.add(db_data)
#     db.commit()
#     db.refresh(db_data)
#     return db_data
    
#组装个对应前端需要的数据
def _cut_book_data(data):
    data1=[]
    #[data1.append(au) for au in data.author.replace('　','').split('，')]
    book_data={
        'author':data.author.replace('　','').split('，'),
        'binding':data.binding,
        'category':data.category,
        'id':data.id,
        'image':data.image,
        'images':{
            'large':data.image
        },
        'isbn':data.isbn,
        'pages':data.pages,
        'price':data.price,
        'pubdate':data.pubdate,
        'publisher':data.publisher,
        'subtitle':'',
        'summary':data.summary,
        'title':data.title,
        'translator':'',
        'framing':data.framing
    }
    return book_data