from contextlib import AbstractContextManager, contextmanager
from datetime import datetime
from typing import Callable

from core.date import now
from sqlalchemy import DateTime, Select, Table, create_engine, orm, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column

Base = declarative_base()


class Database:

    def __init__(self, db_url: str, echo=False) -> None:
        self._engine = create_engine(db_url, echo=echo)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_all(self) -> None:
        Base.metadata.create_all(self._engine)

    def drop_all(self) -> None:
        Base.metadata.drop_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class DBModel(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    @classmethod
    def table(cls) -> Table:
        return cls.__table__

    @classmethod
    def select(cls) -> Select:
        return select(cls)


class BaseTimeModel(DBModel):
    __abstract__ = True

    created_dt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now,
    )
    modified_dt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now,
        onupdate=now,
    )
