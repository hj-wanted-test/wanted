from sqlalchemy import and_, select

from apps.companies.model import CompanyTag
from apps.search.model import KeywordCompany, KeywordTag
from core.repository import Repository


class KeywordTagRepository(Repository):

    __table__ = KeywordTag

    def get_tags_by_names(self, unique_tags: list[str]) -> list[KeywordTag]:
        """
        태그 검색
        """

        find_tags = self.find_all_by(KeywordTag.tag_name.in_(unique_tags))

        return find_tags

    def search_tag(self, keyword: str, lang: str) -> list[str]:
        """
        태그로 회사를 검색하고 목적 언어로 사명을 반환한다
        """

        query = (
            select(
                KeywordCompany.company_name,
            )
            .select_from(KeywordTag)
            .join(CompanyTag, and_(KeywordTag.id == CompanyTag.tag_id))
            .join(
                KeywordCompany,
                and_(
                    KeywordCompany.company_id == CompanyTag.company_id,
                    KeywordCompany.lang == lang,
                ),
            )
            .where(KeywordTag.tag_name == keyword)
        )

        return self.fetch_all(query)
