import enum

from sqlalchemy import Column, String, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    total = Column(Float, default=0.0)

    entries = relationship("Entry", back_populates="creator")


class EntryKind(enum.Enum):
    Expense = "EXPENSE"
    Income = "INCOME"


class Entry(Base):
    __tablename__ = "entries"
    id = Column(String, primary_key=True, index=True)
    kind = Column(Enum(EntryKind))
    amount = Column(Float)
    timestamp = Column(String)

    creator_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    creator = relationship("User", back_populates="entries")
