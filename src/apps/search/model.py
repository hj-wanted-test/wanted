from sqlalchemy import Column, Constraint, Index, Integer, String, ForeignKey
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from apps.companies.model import Tag
from core.db import DBModel


class Fulltext(Constraint):
    def __init__(self, arg):
        self.arg = arg
        super().__init__()


@compiles(Fulltext)
def compile_ft(elem, compiler, **kw):
    return f"FULLTEXT({elem.arg}) WITH PARSER ngram"


class KeywordCompany(DBModel):
    __tablename__ = "keyword_company"

    id = Column(
        Integer, primary_key=True, autoincrement=True, name="keyword_company_id"
    )
    company_name = Column(String(200), nullable=False)
    lang = Column(String(10), nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.company_id"))

    company: Mapped["Company"] = relationship(back_populates="languages")

    __table_args__ = (
        Fulltext("company_name"),
    )

    def __str__(self):
        return f"<KeywordCompany name={self.company_name} company_id={self.company_id}>"


class KeywordTag(DBModel):
    __tablename__ = "keyword_tag"

    id = Column(Integer, primary_key=True, autoincrement=True, name="keyword_tag_id")
    tag_name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<KeywordTag id={self.id} tag={self.tag_name}>"
