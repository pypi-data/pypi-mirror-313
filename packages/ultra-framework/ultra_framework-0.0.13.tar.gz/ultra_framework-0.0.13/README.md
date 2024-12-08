from typing import Self

# UltraFramework

## Description
Framework for FastAPI inspired by Java Spring.

* It exposes a base entity class SQLEntity that can be derived in order to define custom entities.
* It exposes a base repository class CRUDRepository[M]  that can be derived in order to define custom repositories. The following public methods are available:
  * save(entity: M): M
  * find_all(limit: int | None, offset: int | None): Iterable[M]
  * delete(entity: M): None

Example:

```python
from typing import Self, Annotated

from sqlalchemy import create_engine, DDL
from sqlalchemy.orm import mapped_column, Mapped, Session
from sqlalchemy.sql.elements import ColumnElement
from ultra_framework.entities.sql_entity import SQLEntity
from ultra_framework.repositories.crud_repository import CRUDRepository
from ultra_framework.repositories.base_repository_factory import BaseRepositoryFactory
from ultra_framework.utils.dependencies import session_dependency
from ultra_framework.database.session_factory import SessionFactory


engine = create_engine("sqlite:///", connect_args={"check_same_thread": False})

conn = engine.connect()
conn.execute(DDL("""create table users (
    id integer primary key, 
    name text
)"""))
conn.commit()

session_factory = SessionFactory(engine)


class UserEntity(SQLEntity):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]

  @classmethod
  def by_id(cls, idx: int) -> ColumnElement[bool]:
    return cls.id == idx


class UserRepository(CRUDRepository[UserEntity]):
  entity_class = UserEntity

  @CRUDRepository.auto_implement_one([UserEntity.by_id])
  def find_by_id(self, idx: int) -> UserEntity: ...


class RepositoryFactory(BaseRepositoryFactory):
  repository_map = {
    "users": UserRepository,
  }

  @property
  def user_repository(self) -> UserRepository:
    return self.get_repository("users")

  @classmethod
  def create_factory(cls, session: Annotated[Session, session_dependency(session_factory)]) -> Self:
    return cls(session)
```
