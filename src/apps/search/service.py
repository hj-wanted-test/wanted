from apps.search.dto import SearchCompanyResponseDto
from apps.search.repository.keyword_company_repository import KeywordCompanyRepository
from apps.search.repository.keyword_tag_repository import KeywordTagRepository


class SearchService:
    def __init__(
        self,
        keyword_company_repository: KeywordCompanyRepository,
        keyword_tag_repository: KeywordTagRepository,
    ):
        self.keyword_company_repository = keyword_company_repository
        self.keyword_tag_repository = keyword_tag_repository

    def search_company(self, query: str, lang: str):
        """
        사명 키워드 검색
        """

        result = self.keyword_company_repository.search_company(query, lang)

        return [SearchCompanyResponseDto(company_name=x) for x in result]

    def search_tag(self, query: str, lang: str):
        """
        태그로 회사 검색
        """

        result = self.keyword_tag_repository.search_tag(query, lang)
        return [SearchCompanyResponseDto(company_name=x) for x in result]
