# -*- coding: utf-8 -*-

from fastapi import APIRouter
from . import todo


api_router = APIRouter()
api_router.include_router(todo.router, tags=["todo"])
