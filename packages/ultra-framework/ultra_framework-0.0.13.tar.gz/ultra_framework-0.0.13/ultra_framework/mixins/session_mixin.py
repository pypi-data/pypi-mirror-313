from sqlalchemy.orm import Session


class SessionMixin:

    def __init__(self, session: Session):
        self.session = session
