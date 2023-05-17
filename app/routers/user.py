import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.database import get_db
from app.models import Entry, EntryKind
from app.models import User
from app.oauth2 import get_password_hash, get_current_active_user
from app.schemas import UserDisplay, UserCreate, EntryDisplay
from app.utils.responses import user_responses
from app.utils.validators import user_exists

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserDisplay, dependencies=[Depends(user_exists)], responses=user_responses,
             status_code=201)
def create_user(response: Response, data: UserCreate, db: Session = Depends(get_db)):
    user = User(name=data.name, email=data.email, id=str(uuid.uuid4()), password=get_password_hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    response.headers["Location"] = '/user'
    return user


@router.get("", response_model=UserDisplay)
def get_user(current_user: UserDisplay = Depends(get_current_active_user)):
    print(current_user.total)
    return current_user


@router.get("/expenses", response_model=List[EntryDisplay])
def get_expenses(current_user: UserDisplay = Depends(get_current_active_user), db: Session = Depends(get_db)):
    expenses = db.query(Entry).where(Entry.creator_id == current_user.id).where(
        Entry.kind == EntryKind.Expense).order_by(desc(Entry.timestamp)).all()
    return expenses


@router.get("/incomes", response_model=List[EntryDisplay])
def get_expenses(current_user: UserDisplay = Depends(get_current_active_user), db: Session = Depends(get_db)):
    incomes = db.query(Entry).where(Entry.creator_id == current_user.id).where(
        Entry.kind == EntryKind.Income).order_by(desc(Entry.timestamp)).all()
    return incomes
