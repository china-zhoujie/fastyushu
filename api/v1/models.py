#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from sqlalchemy import Column, String, Integer, BigInteger, Date, Text, DateTime, SmallInteger, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from typing import Optional
from .database import Base as Base_

from passlib.context import CryptContext

class Base(Base_):
    __abstract__ = True
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
        

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(50))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(String(50))
    pubdate = Column(String(50))
    isbn = Column(String(100), nullable=False, unique=False)
    summary = Column(String(1000))
    image = Column(String(500))
    images = Column(String(500))
    category = Column(String(500))
    framing = Column(String(500))
    # created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')



class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24),unique=True)
    auth = Column(SmallInteger,default=1)
    role = Column(String(24),nullable=False)
    _password = Column('password',String(100))
    gift = relationship('Gift', back_populates='user')  
    # created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def keys(self):
        return ['id','email','nickname','auth']
        
    def encryption_password(self,pwd):
        encryption_pwd = CryptContext(
            schemes=["sha256_crypt", "md5_crypt", "des_crypt"]
        )
        password = encryption_pwd.hash(pwd)
        return password
        
        
    def encryption_password_or_decode(self,*, pwd: str, hashed_password: Optional[str] = None):
        """
        密码加密或解密
        :param pwd:
        :param hashed_password:
        :return:
        """
        encryption_pwd = CryptContext(
            schemas=["sha256_crypt", "md5_crypt", "des_crypt"]
        )
    
        def encryption_password(self):
            password = encryption_pwd.hash(pwd)
            return password
    
        def decode_password(self):
            password = encryption_pwd.verify(pwd, hashed_password)
            return password
    
        return self.decode_password() if hashed_password else self.encryption_password()


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = self.encryption_password(raw)
        
        
class Gift(Base):
    __tablename__ = "gift"
    id = Column(Integer,primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(25),nullable=False)
    launched = Column(Boolean,default=False)
    user = relationship('User', back_populates='gift')
    # created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
class Group(Base):
    __tablename__ = "group"
    UserGroupIdentity = Column(Integer,primary_key=True)
    UserGroupName = Column(String(45),nullable=False)
    #GroupDesc = Column(String(45),nullable=False)
    UserPrivileges = Column(String(2000),nullable=False)
    #RtType = Column(Integer,nullable=False,comment='角色')
    #OtherPrivileges = Column(Text,nullable=False,comment='其他权限值,用Json')
    #AppPrivileges = Column(Text,nullable=False)
    #isdeleted = Column(Integer,nullable=False,default=1)



""" 附上三个SQLAlchemy教程
SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html
Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html
SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""