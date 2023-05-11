from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Entry, User


async def user_exists(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data["email"]
    user = db.query(User).where(User.email == email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists with this email")


def entry_exists(request: Request, db: Session = Depends(get_db)):
    entry_id = None
    for key, val in request.path_params.items():
        if key == "entry_id":
            entry_id = val
    if not entry_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="entry_id not found")
    entry = db.query(Entry).where(Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This entry does not exist")
    return entry
