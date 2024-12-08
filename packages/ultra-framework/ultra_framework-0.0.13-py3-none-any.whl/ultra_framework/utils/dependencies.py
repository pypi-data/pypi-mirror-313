from fastapi.params import Depends

from ultra_framework.database.session_factory import SessionFactory


def session_dependency(session_factory: SessionFactory) -> Depends:
    return Depends(session_factory.create_session)
