"""session_factory module"""
from typing import Iterator

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session


class SessionFactory:
    """SessionFactory class"""

    def __init__(self, engine: Engine):
        self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def create_session(self) -> Iterator[Session]:
        """creates a session object from the session maker"""
        session = self._session_maker()

        try:
            yield session
        finally:
            session.close()
