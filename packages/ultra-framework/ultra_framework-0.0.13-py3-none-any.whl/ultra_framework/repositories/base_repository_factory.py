from abc import ABC, abstractmethod
from typing import Self, Type, Any, Mapping

from sqlalchemy.orm import Session
from ultra_framework.repositories.crud_repository import CRUDRepository


class BaseRepositoryFactory(ABC):

    repository_map: Mapping[str, Type[CRUDRepository]]

    def __init__(self, session: Session):
        self._repository_dict = {
            repository_name: repository_class(session)
            for repository_name, repository_class in self.repository_map.items()
        }

    @classmethod
    @abstractmethod
    def create_factory(cls, session: Session) -> Self:
        """implement session dependency"""

    def get_repository(self, repository_name: str) -> Any:
        return self._repository_dict.get(repository_name, None)
