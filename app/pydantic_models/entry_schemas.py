from typing import Optional

from pydantic import BaseModel

from app.models import EntryKind, ExpenseKind
from app.pydantic_models.user_schemas import UserDisplay


class EntryInput(BaseModel):
    kind: EntryKind
    amount: float
    expenseKind: Optional[ExpenseKind]


class EntryDisplay(EntryInput):
    id: str
    timestamp: str
    expenseKind: Optional[ExpenseKind]
    creator: UserDisplay

    class Config:
        orm_mode = True


class EntryInputPatch(BaseModel):
    kind: Optional[EntryKind]
    amount: Optional[float]
    expenseKind: Optional[ExpenseKind]
