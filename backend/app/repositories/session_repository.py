from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.session import UserSession


class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, code: str, company_id: int, nickname: str | None = None) -> UserSession:
        session = UserSession(code=code, company_id=company_id, nickname=nickname)
        self.db.add(session)
        self.db.flush()
        return session

    def get_by_code(self, code: str) -> UserSession | None:
        stmt = select(UserSession).where(UserSession.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def code_exists(self, code: str) -> bool:
        return self.get_by_code(code) is not None

    def touch(self, session: UserSession) -> UserSession:
        session.last_accessed_at = datetime.now(timezone.utc)
        self.db.flush()
        return session

    def delete(self, session: UserSession) -> None:
        self.db.delete(session)
        self.db.flush()

    def count_for_company(self, company_id: int) -> int:
        stmt = select(func.count()).select_from(UserSession).where(UserSession.company_id == company_id)
        return self.db.execute(stmt).scalar_one()
