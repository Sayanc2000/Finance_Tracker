import uuid

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import EntryKind, ExpenseKind, Entry
from app.schemas import UserDisplay
from app.utils.time_functions import current_utc_time


def make_entries_from_csv(file: UploadFile, user: UserDisplay, db: Session):
    df = pd.read_csv(file.file)
    for i, r in df.iterrows():
        amount = df['amount'] if not pd.isna(df['amount']) else 0.0
        if not pd.isna(df['entry_kind']):
            if df['entry-kind'] == 'EXPENSE':
                entryKind = EntryKind.Expense
            elif df['entry-kind'] == 'INCOME':
                entryKind = EntryKind.Income
            else:
                continue
        else:
            continue
        if not pd.isna(df['expense-kind']):
            if df['expense-kind'] == 'NEED':
                expenseKind = ExpenseKind.Need
            elif df['expense-kind'] == 'WANT':
                expenseKind = ExpenseKind.Want
            else:
                expenseKind = None
        else:
            expenseKind = None
        entry = Entry(id=str(uuid.uuid4()), amount=amount, entryKind=entryKind, expenseKind=expenseKind,
                      creator_id=user.id, timestamp=current_utc_time())
        db.add(entry)
        db.commit()
