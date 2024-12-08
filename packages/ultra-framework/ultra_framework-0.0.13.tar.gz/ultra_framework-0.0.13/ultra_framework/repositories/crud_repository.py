from typing import List, Union, Callable, Type

from sqlalchemy import ColumnElement, LambdaElement
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import SQLCoreOperations
from sqlalchemy.sql.roles import ExpressionElementRole, TypedColumnsClauseRole

from ultra_framework.entities.sql_entity import SQLEntity
from ultra_framework.mixins.session_mixin import SessionMixin

type Criterion[T] = Union[
    ColumnElement[T],
    SQLCoreOperations[T],
    ExpressionElementRole[T],
    TypedColumnsClauseRole[T],
    Callable[[], ColumnElement[T] | LambdaElement]
]


class CRUDRepository[T: SQLEntity](SessionMixin):

    entity_class: Type[T]

    def save(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.flush()
        return entity

    def find_all(self, limit: int | None = None, offset: int | None = None) -> List[T]:
        query = self.session.query(self.entity_class)
        return self.__set_limit_offset(query, limit, offset).all()

    def delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.commit()

    def filter_by_conditions(self, conditions: List[Criterion[bool]],
                               limit: int | None = None, offset: int | None = None) -> Query[T]:
        query = self.session.query(self.entity_class).filter(*conditions)
        return self.__set_limit_offset(query, limit, offset)

    @staticmethod
    def __set_limit_offset(query: Query, limit: int | None = None, offset: int | None = None) -> Query[T]:
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query
