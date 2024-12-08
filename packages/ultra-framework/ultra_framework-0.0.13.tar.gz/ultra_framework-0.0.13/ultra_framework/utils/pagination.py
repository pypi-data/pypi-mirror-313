from typing import List, Self

from fastapi.params import Query
from pydantic import BaseModel


class PaginatedParams:

    def __init__(self,
                 page: int = Query(1, ge=1),
                 per_page: int = Query(100, ge=0)):
        self.limit = per_page * page
        self.offset = (page - 1) * per_page

        self.page = page
        self.per_page = per_page

    def __str__(self) -> str:
        return f"page={self.page}, per_page={self.per_page}"

    def __repr__(self):
        return str(self)


class PaginatedResponse[M: BaseModel](BaseModel):

    count: int
    fields: List[M]

    @classmethod
    def paginate(cls, fields: List[M]) -> Self:
        return cls(
            fields=fields,
            count=len(fields)
        )
