from sqlalchemy import select, and_
from sqlalchemy.dialects.mysql import match
from sqlalchemy.orm import aliased

from apps.search.model import KeywordCompany
from core.repository import Repository


match_expr = match(
    KeywordCompany.company_name,
    against="company_name",
)

class KeywordCompanyRepository(Repository):

    __table__ = KeywordCompany

    def find_company_name(self, company_name, lang) -> tuple[str, int, str]:
        """
        회사명으로 검색하고, 사명(검색어), 회사ID, 사명(목적 언어)을 반환한다
        """

        tbl1 = aliased(KeywordCompany)
        tbl2 = aliased(KeywordCompany)
        query = (
            select(
                tbl2.company_name,
                tbl1.company_id,
                tbl1.company_name,
            )
            .select_from(tbl1)
            .join(tbl2, and_(tbl1.company_id == tbl2.company_id, tbl2.lang == lang), isouter=True)
            .where(tbl1.company_name == company_name)
        )
        res = self.fetch_one(query, raw=True)

        return res

    def search_company(self, keyword:str, lang:str) -> list[tuple[str, int]]:
        """
        검색어로 회사를 검색하고 사명(목적 언어), 회사ID를 반환한다
        """

        tbl1 = aliased(KeywordCompany)
        tbl2 = aliased(KeywordCompany)
        query = (
            select(
                tbl2.company_name,
                tbl1.company_id,
            )
            .select_from(tbl1)
            .join(tbl2, and_(tbl1.company_id == tbl2.company_id, tbl2.lang == lang))
            .where(tbl1.company_name.match(keyword))
        )

        return self.fetch_all(query)
