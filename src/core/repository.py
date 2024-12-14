from contextlib import AbstractContextManager
from typing import Callable, Any, Sequence

from sqlalchemy import Result, CursorResult, Row, select, func
from sqlalchemy.orm import Session

from core.db import DBModel


class Repository:

    __table__: DBModel = None

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _execute(self, query):# -> Result[Any] | CursorResult[Any]:
        with self.session_factory() as session:
            return session.execute(query)

    def fetch_all(self, query, raw=False):# -> Sequence[Row[Any]]:
        with self.session_factory() as session:
            if raw:
                return session.execute(query).fetchall()
            return session.execute(query).scalars().all()

    def fetch_one(self, query, raw=False):
        res = self.fetch_all(query, raw=raw)
        return None if not res else res[0]

    def get(self, id: int):# -> DBModel:
        query = self.__table__.select().where(self.__table__.id == id)
        return self.fetch_one(query)

    def find_by(self, *args, **kwargs):# -> DBModel:
        res = self.find_all_by(*args, **kwargs)
        return None if not res else res[0]

    def find_all_by(self, *args, **kwargs):# -> list[DBModel]:
        if not args and not kwargs:
            raise Exception("find_by requires either args or kwargs")

        conds = [*args]

        for key, value in kwargs.items():
            conds.append((getattr(self.__table__, key) == value))

        query = self.__table__.select().where(*conds)

        return self.fetch_all(query)

    def count_by(self, *args, **kwargs) -> int:
        conds = [*args]

        for key, value in kwargs.items():
            conds.append((getattr(self.__table__, key) == value))

        query = select(func.count()).where(*conds)

        return self.fetch_one(query)[0]

    def save(self, obj: DBModel, commit: bool = False) -> DBModel:
        with self.session_factory() as session:
            session.add(obj)
            if commit:
                session.commit()
            session.refresh(obj)

        return obj

    def save_bulk(self, objs: list[DBModel], commit: bool = False) -> list[DBModel]:
        with self.session_factory() as session:
            session.bulk_save_objects(objs)

            if commit:
                session.commit()

        return objs

    def delete_all_by(self, *args, **kwargs):
        conds = [*args]

        for key, value in kwargs.items():
            conds.append((getattr(self.__table__, key) == value))

        with self.session_factory() as session:
            session.query(self.__table__).filter(*conds).delete()
            session.commit()
