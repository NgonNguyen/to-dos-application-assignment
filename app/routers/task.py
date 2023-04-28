from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from services.auth import token_interceptor
from database import get_db_context

from schemas import Task, User
from models import TaskModel, TaskViewModel

router = APIRouter(prefix="/task", tags=["Task"])


@router.get("")
async def get_all_tasks(
        summary: str = Query(default=None),
        user_id: UUID = Query(default=None),
        page: int = Query(ge=1, default=1),
        size: int = Query(ge=1, le=50, default=10),
        user: User = Depends(token_interceptor),
        db: Session = Depends(get_db_context)
) -> List[TaskViewModel]:

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied")

    # Default of joinedload is LEFT OUTER JOIN
    query = db.query(Task).options(joinedload(Task.owner))

    if summary is not None:
        query = query.filter(Task.summary.like(f"{summary}%"))
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    return query.offset((page-1)*size).limit(size).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskModel,
                      user: User = Depends(token_interceptor),
                      db: Session = Depends(get_db_context)) -> TaskViewModel:
    print(user.id)
    user = db.query(User).filter(user.id == request.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=422, detail="Invalid user information")

    new_task = Task(**request.dict())
    new_task.created_at = datetime.utcnow()
    new_task.user_id = user.id

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/{task_id}")
async def get_task_detail(task_id: UUID, db: Session = Depends(get_db_context)) -> TaskViewModel:
    return db.query(Task).filter(Task.id == task_id)\
        .options(joinedload(Task.owner, innerjoin=True))\
        .first()


@router.put("/{task_id}")
async def update_task(task_id: UUID, request: TaskModel, db: Session = Depends(get_db_context)) -> TaskViewModel:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if task.user_id != request.user_id:
        changed_author = db.query(User).filter(
            User.id == request.user_id).first()
        if changed_author is None:
            raise HTTPException(
                status_code=422, detail="Invalid author information")
        else:
            task.user_id = request.user_id

    task.title = request.title
    task.description = request.description
    task.mode = request.mode
    task.rating = request.rating
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
