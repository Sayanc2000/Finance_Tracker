import uuid
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi_cache.decorator import cache
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.database import get_db
from app.models import Entry
from app.models import EntryKind
from app.oauth2 import get_current_active_user
from app.schemas import UserDisplay, EntryInput, EntryDisplay, DefaultResponse, EntryInputPatch
from app.utils.time_functions import current_utc_time
from app.utils.validators import entry_exists, entry_exists_delete
from app.utils.workers import make_entries_from_csv

router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("", response_model=List[EntryDisplay], response_model_exclude_none=True)
@cache(expire=60)
def get_entries_for_user(current_user: UserDisplay = Depends(get_current_active_user), db: Session = Depends(get_db)):
    entries = db.query(Entry).where(Entry.creator_id == current_user.id).order_by(
        desc(Entry.timestamp)).all()
    return entries


@router.get("/{entry_id}", response_model=EntryDisplay, response_model_exclude_none=True)
def get_entry_by_id(entry_id: str, current_user: UserDisplay = Depends(get_current_active_user),
                    entry: Entry = Depends(entry_exists)):
    return entry


@router.post("", response_model=EntryDisplay, response_model_exclude_none=True)
def make_entry(response: Response, data: EntryInput, current_user: UserDisplay = Depends(get_current_active_user),
               db: Session = Depends(get_db)):
    entry = Entry(**data.dict(), id=str(uuid.uuid4()), timestamp=current_utc_time(), creator_id=current_user.id)
    if entry.kind == EntryKind.Expense:
        current_user.total -= entry.amount
    else:
        current_user.total += entry.amount
    db.add(entry)
    db.commit()
    db.refresh(entry)
    response.status_code = status.HTTP_201_CREATED
    response.headers["Location"] = f"/entries/{entry.id}"
    return entry


@router.post("/file", response_model=DefaultResponse, include_in_schema=False)
def entry_from_file(file: UploadFile = File(...), current_user: UserDisplay = Depends(get_current_active_user),
                    db: Session = Depends(get_db)):
    make_entries_from_csv(file=file, user=current_user, db=db)
    return {
        "message": "CSV queued"
    }


@router.patch("/{entry_id}", response_model=EntryDisplay, response_model_exclude_none=True)
def edit_entry(entry_id: str, data: EntryInputPatch, entry: Entry = Depends(entry_exists),
               db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_active_user)):
    excluded_dict = data.dict(exclude_none=True)
    for key, value in excluded_dict.items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", response_model=DefaultResponse)
def delete_entry(entry_id: str, entry: Entry = Depends(entry_exists_delete), db: Session = Depends(get_db),
                 current_user: UserDisplay = Depends(get_current_active_user)):
    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted successfully"}
