from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from actions import user as user_actions
from config import get_logger
from database import get_db
from schemas.user import User, UserCreate, UserUpdate

router = APIRouter()

logger = get_logger()


@router.post("/users", response_model=User, tags=['user'])
def create_user(db: Session = Depends(get_db),
                user: UserCreate = Body(
                    ...,
                    example={
                        'name': 'Bob',
                        'email': 'bob@example.com',
                        'password': 'Thes3cret_'
                    })):
    new_user = user_actions.create_user(db, user)
    return new_user


@router.get('/users/{id}', response_model=User, tags=['user'])
def get_user(id: UUID4, db: Session = Depends(get_db)):
    user = user_actions.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.put('/users/{id}', response_model=User, tags=['user'])
def update_user(id: UUID4,
                db: Session = Depends(get_db),
                new_user: UserUpdate = Body(
                    ..., example={
                        'name': 'Robert',
                        'bio': 'logy #puns'
                    })):
    updated_user = user_actions.update_user(db, id, new_user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return updated_user
