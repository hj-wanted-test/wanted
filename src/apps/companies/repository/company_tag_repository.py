from sqlalchemy import select

# from apps.companies.model import CompanyTag
from apps.search.model import KeywordTag
from core.repository import Repository


class CompanyTagRepository(Repository):

    # __table__ = CompanyTag

    def get_company_tags_by_lang(self, company_id: int, lang: str) -> list[str]:

        query = (
            select(
                KeywordTag.tag_name
            )
            .select_from(self.__table__)
            .join(KeywordTag, KeywordTag.id == self.__table__.tag_id)
            .where(self.__table__.company_id == company_id, self.__table__.lang == lang)
        )

        res = [x[0] for x in self.fetch_all(query, raw=True)]

        return res
