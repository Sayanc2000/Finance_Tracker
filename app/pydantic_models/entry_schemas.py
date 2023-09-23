from typing import Optional

from pydantic import BaseModel

from app.models import EntryKind, ExpenseKind


class EntryInput(BaseModel):
    kind: EntryKind
    amount: float
    expenseKind: Optional[ExpenseKind]


class EntryDisplay(EntryInput):
    id: str
    timestamp: str
    expenseKind: Optional[ExpenseKind]

    class Config:
        orm_mode = True


class EntryInputPatch(BaseModel):
    kind: Optional[EntryKind]
    amount: Optional[float]
    expenseKind: Optional[ExpenseKind]
