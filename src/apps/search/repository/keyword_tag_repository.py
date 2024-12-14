from sqlalchemy import select, and_
from sqlalchemy.orm import aliased

from apps.companies.model import CompanyTag
from apps.search.model import KeywordTag, KeywordCompany
from core.repository import Repository


class KeywordTagRepository(Repository):

    __table__ = KeywordTag

    def get_tags_by_names(self, unique_tags:list[str]) -> list[KeywordTag]:

        find_tags = self.find_all_by(KeywordTag.tag_name.in_(unique_tags))
        return find_tags

    def search_tag(self, keyword:str, lang:str):
        query = (
            select(
                KeywordCompany.company_name
            )
            .select_from(KeywordTag)
            .join(CompanyTag, and_(KeywordTag.id == CompanyTag.tag_id))
            .join(KeywordCompany, and_(KeywordCompany.company_id == CompanyTag.company_id, KeywordCompany.lang == lang))
            .where(KeywordTag.tag_name == keyword)
        )

        return self.fetch_all(query)
