from typing import List

from pydantic import BaseModel


class UserModel(BaseModel):

    name: str
    email: str
    roles: List[str]
