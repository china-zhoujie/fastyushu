#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from datetime import date as date_
from datetime import datetime
from fastapi import Query
from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    email: str = Field(...)
    nickname: str = Field(...)
    role: str  = Field(...)
    password: str = Field(...,min_length=8,max_length=16)

# class CreateGfift(BaseModel):
#     uid: str = Field(...)
#     isbn: str = Field(...)
#     launched: str = Field(default=0)

class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: int
    
class CreateGroup(BaseModel):
    UserGroupName: str = Field(...,min_length=2,max_length=10)
    UserPrivileges: list = Field(...)
    
class ReadGroup(BaseModel):
    UserGroupIdentity: int
    UserGroupName: str
    UserPrivileges: str

    class Config:
        orm_mode = True

class ReadUser(BaseModel):
    id: int
    nickname: str
    auth: int
    role: str
    status: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class ReadCity(CreateCity):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True