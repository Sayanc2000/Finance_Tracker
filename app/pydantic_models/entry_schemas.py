from typing import Optional

from pydantic import BaseModel

from app.models import EntryKind
from app.pydantic_models.user_schemas import UserDisplay


class EntryInput(BaseModel):
    kind: EntryKind
    amount: float


class EntryDisplay(EntryInput):
    id: str
    timestamp: str
    creator: UserDisplay

    class Config:
        orm_mode = True


class EntryInputPatch(BaseModel):
    kind: Optional[EntryKind]
    amount: Optional[float]