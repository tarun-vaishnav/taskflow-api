from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Task
from app.schemas import TaskCreate,TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks",tags=["Tasks"])

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreate,
    db:Session = Depends(get_db)
):
    task = Task(
        title=payload.title,
        description = payload.description
    )
    
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception:
        db.rollback()
        raise
    
    return task

@router.get("",response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    statement = select(Task).order_by(Task.id)
    return db.scalars(statement).all()

@router.get("/{task_id}",response_model=TaskResponse)
def get_task(
    task_id: int,
    db:Session = Depends(get_db),
):
    task = db.get(Task,task_id)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task

@router.patch("/{task_id}",response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = db.get(Task, task_id)
    
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    
    changes = payload.model_dump(exclude_unset=True)
    
    if not changes:
        raise HTTPException(
            status_code=422,
            detail="At least one field must be provided",
        )
    
    for field, value in changes.items():
        setattr(task,field,value)
        
    try:
        db.commit()
        db.refresh(task)
    except Exception:
        db.rollback()
        raise
    return task

@router.delete("/{task_id}",status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = db.get(Task,task_id)
    
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    
    try:
        db.delete(task)
        db.commit()
    except Exception:
        db.rollback()
        raise