from typing import List

from sqlalchemy import Column, Integer, String, Index, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import DBModel


association_table = Table(
    "company_tag",
    DBModel.metadata,
    Column("company_id", ForeignKey("company.company_id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.tag_id"), primary_key=True),
)


class Company(DBModel):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True, name="company_id")
    company_name = Column(String(200), nullable=True)

    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=association_table,
        back_populates="companies",
    )
    languages: Mapped[List["KeywordCompany"]] = relationship("KeywordCompany", back_populates="company")


class Tag(DBModel):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True, name="tag_id")
    tag_name = Column(String(200), nullable=True)

    companies: Mapped[List["Company"]] = relationship(
        "Company",
        secondary=association_table,
        back_populates="tags",
    )
    languages: Mapped[List["TagLang"]] = relationship("TagLang", back_populates="tag")


class TagLang(DBModel):
    __tablename__ = "tag_lang"

    id = Column(Integer, primary_key=True, autoincrement=True, name="tag_lang_id")
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.tag_id"))
    lang = Column(String(10), nullable=False)
    tag_name = Column(String(200), nullable=True)
    tag: Mapped["Tag"] = relationship(back_populates="languages")
