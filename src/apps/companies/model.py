from sqlalchemy import Column, Integer, String, Index

from core.db import DBModel


class Company(DBModel):
    """회사 정보 테이블"""

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True, name="company_id")
    company_name = Column(String(200), nullable=True)


class CompanyTag(DBModel):
    """회사의 태그"""

    __tablename__ = "company_tag"

    id = Column(Integer, primary_key=True, autoincrement=True, name="company_tag_id")
    company_id = Column(Integer, nullable=False)
    tag_id = Column(Integer, nullable=False)
    lang = Column(String(10), nullable=False)

    __table_args__ = (
        Index("idx_company_id", company_id),
        Index("idx_tag_id", tag_id),
        Index("idx_company_lang", company_id, lang),
    )
