from typing import Union

from app.pydantic_models.entry_schemas import *
from app.pydantic_models.user_schemas import *
from app.pydantic_models.auth_schemas import *


class DefaultResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str

    class Config:
        orm_mode = True













