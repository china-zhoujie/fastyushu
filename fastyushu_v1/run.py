#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

import time
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
#from utils.response import SuccessResponse, ErrorResponse
from api.v1 import application
from utils.verifyall import *

#重写库
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title='YushuBook',
    description='鱼书项目api接口',
    version='v1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)#跨域设置


# @app.middleware("http")
# async def check_token(request, call_next):
#     # 获取令牌
#     token = request.headers.get("Authorization")
#     if not token:
#         # 没有令牌，返回错误信息
#         return JSONResponse(
#             content={"message": "Authorization required"},
#             status_code=400
#         )
#     # 验证令牌是否合法
#     user_data = jwt_get_current_user(token)
#     #print(user_data)
#     if not user_data:
#         return JSONResponse(
#             content={"message": "Invalid authorization"},
#             status_code=401
#         )
#     # 继续处理请求
#     request.state.user = user_data
#     #response.headers['user_data'] = str(request.state.user)
#     response = await call_next(request)
#     return response
    
    
# @app.middleware('http') #中间件
# async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求做为参数
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers['X-Process-Time'] = str(process_time)  # 添加自定义的以“X-”开头的请求头
#     return response
# @app.get("/")
# async def index(page: int, limit: Optional[int] = None):
#     data = {
#         "page": page,
#         "limit": limit
#     }
#     return SuccessResponse(data=data)
    
    
app.include_router(application, prefix='/yushu/v1', tags=['鱼书api-v1.0.0'],dependencies=[Depends(verify_token)])

#app.include_router(application, prefix='/yushu/v1', tags=['鱼书api-v1.0.0'])

if __name__=='__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8888, reload=True, debug=True, workers=1)

