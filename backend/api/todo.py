from fastapi import HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func
from datetime import datetime, date
from db import Todo, Remark, BaseTodo
from scheam import (
    TodoCreateSchema,
    TodoSchema,
    DataResponse,
    RemarkCreateSchema,
    RemarkSchema,
    BaseTodoCreateSchema,
    BaseTodoSchema,
)
from db import get_db
from fastapi import APIRouter
from typing import List, Union, Optional

router = APIRouter()


@router.post("/todos/")
async def create_todo(todo: TodoCreateSchema, db: AsyncSession = Depends(get_db)):
    existing_todo = await db.execute(
        select(Todo).where(Todo.title == todo.title, Todo.date == date.today())
    )
    if existing_todo.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="今日已存在该事项")
    todo_dict = todo.model_dump()
    db_todo = Todo(**todo_dict)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return DataResponse[TodoSchema](msg="创建成功", code=200, data=db_todo)


@router.get("/todos/")
async def get_todos(
    db: AsyncSession = Depends(get_db),
    date: Optional[date] = Query(None),
    year_month: Optional[str] = Query(None),
):
    stmt = select(Todo)
    if date:
        stmt = stmt.where(Todo.date == date)
    if year_month:
        year, month = map(int, year_month.split("-"))
        stmt = stmt.where(
            extract("year", Todo.date) == year, extract("month", Todo.date) == month
        )

    todos = await db.execute(stmt)
    return DataResponse[List[TodoSchema]](
        msg="获取成功", code=200, data=todos.scalars().all()
    )


@router.delete("/todos/{id}/")
async def delete_todo(id: int, db: AsyncSession = Depends(get_db)):
    todo = await db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=400, detail="已经被删除")
    await db.delete(todo)
    await db.commit()
    return DataResponse(msg="删除成功", code=200, data=None)


@router.delete("/todos_by_date_title/")
async def delete_todo_by_date_title(
    date: date = Query(...), title: str = Query(...), db: AsyncSession = Depends(get_db)
):
    todo = await db.execute(select(Todo).where(Todo.date == date, Todo.title == title))
    todo = todo.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=400, detail="已经被删除")
    await db.delete(todo)
    await db.commit()
    return DataResponse(msg="删除成功", code=200, data=None)


@router.post("/remarks/")
async def create_remark(remark: RemarkCreateSchema, db: AsyncSession = Depends(get_db)):
    remark_dict = remark.model_dump()
    db_remark = Remark(**remark_dict)
    db.add(db_remark)
    await db.commit()
    await db.refresh(db_remark)
    return DataResponse[RemarkSchema](msg="创建成功", code=200, data=db_remark)


@router.get("/remarks/")
async def get_remarks(
    date: Optional[date] = Query(...), db: AsyncSession = Depends(get_db)
):
    stmt = select(Remark).where(Remark.date == date)
    remarks = await db.execute(stmt)
    return DataResponse[List[RemarkSchema]](
        msg="获取成功", code=200, data=remarks.scalars().all()
    )


@router.post("/base_todos/")
async def create_base_todo(
    todo: BaseTodoCreateSchema, db: AsyncSession = Depends(get_db)
):
    todo_dict = todo.model_dump()
    db_todo = BaseTodo(**todo_dict)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return DataResponse[BaseTodoSchema](msg="创建成功", code=200, data=db_todo)


@router.get("/base_todos/")
async def get_base_todos(db: AsyncSession = Depends(get_db)):
    stmt = select(BaseTodo)
    base_todos = await db.execute(stmt)
    return DataResponse[List[BaseTodoSchema]](
        msg="获取成功", code=200, data=base_todos.scalars().all()
    )


# Include the router in the main app
