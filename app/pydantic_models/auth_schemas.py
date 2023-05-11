from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    email: Union[str, None] = None
