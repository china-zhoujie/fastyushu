# 依赖安装：pip install orjson
from fastapi.responses import JSONResponse, ORJSONResponse as Response
from fastapi import status as http_status
from utils import status as http
from typing import Union

def SuccessResponse(*, data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            'code': 200,
            'message': "Success",
            'data': data,
        }
    )
def ErrorResponse(*, data: str = None, message: str="BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=http_status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'message': message,
            'data': data,
        }
    )


class SuccessResponse1(Response):
    """
    成功响应
    """
    def __init__(self, data=None, msg="success", code=http.HTTP_SUCCESS, status=http_status.HTTP_200_OK
                 , **kwargs):
        self.data = {
            "code": code,
            "message": msg,
            "data": data
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)


class ErrorResponse2(Response):
    """
    失败响应
    """
    def __init__(self, msg=None, code=http.HTTP_ERROR, status=http_status.HTTP_200_OK, **kwargs):
        self.data = {
            "code": code,
            "message": msg,
            "data": []
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)
