from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Generic, TypeVar, Optional, List
from datetime import datetime, date

# Pydantic模型
T = TypeVar("T")


class BaseResponse(BaseModel):
    msg: str
    code: int


class DataResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None


class TodoCreateSchema(BaseModel):
    title: str


class TodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    date: date
    createTime: datetime

    @field_serializer("createTime")
    def ser_datetime(self, createTime: datetime, _info):
        return createTime.strftime("%Y-%m-%d %H:%M:%S")


class RemarkCreateSchema(BaseModel):
    content: str


class RemarkSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    date: date
    createTime: datetime

    @field_serializer("createTime")
    def ser_datetime(self, createTime: datetime, _info):
        return createTime.strftime("%Y-%m-%d %H:%M:%S")


class BaseTodoCreateSchema(BaseModel):
    title: str


class BaseTodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
