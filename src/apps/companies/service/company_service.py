from apps.companies.dto import CompanyRequestDto, CompanyResponseDto, CompanyTagNameDto
from apps.companies.model import Company
from apps.companies.repository.company_repository import CompanyRepository
from apps.companies.service.tag_service import TagService
from apps.search.model import KeywordCompany, KeywordTag
from apps.search.repository.keyword_company_repository import KeywordCompanyRepository
from core.exception import PageNotFound


class CompanyService:
    def __init__(
        self,
        tag_service: TagService,
        company_repository: CompanyRepository,
        keyword_company_repository: KeywordCompanyRepository,
    ):
        self.tag_service = tag_service
        self.company_repository = company_repository
        self.keyword_company_repository = keyword_company_repository

    def create_company(self, request: CompanyRequestDto) -> None:
        """
        회사 생성
        """

        # 회사명은 정의된 언어 중 첫번째로 임의 설정한다(식별을 위해)
        company_name = list(request.company_name.values())[0]

        company = Company(company_name=company_name)
        self.company_repository.save(company, commit=True)

        # 회사명 검색어용으로 저장한다
        keyword_company_list = []
        for lang, name in request.company_name.items():
            keyword_company = KeywordCompany(
                company_name=name,
                company_id=company.id,
                lang=lang,
            )
            keyword_company_list.append(keyword_company)

        self.keyword_company_repository.save_bulk(keyword_company_list, commit=True)

        self.tag_service.associate_tags_to_company(
            company_id=company.id, tags=request.tags
        )

    def find_company_by_keyword(
        self, company_name: str, lang: str
    ) -> tuple[str, int, str]:
        """
        회사명으로 검색하고, 사명(검색어), 회사ID, 사명(목적 언어)을 반환한다
        """

        keyword_company = self.keyword_company_repository.find_company_name(
            company_name=company_name, lang=lang
        )
        if not keyword_company:
            raise PageNotFound("Company not found")

        return keyword_company

    def get_company_by_name(self, company_name: str, lang: str) -> CompanyResponseDto:
        """
        요청한 언어로 회사명과 태그를 반환한다
        """
        company_name, company_id, find_company_name = self.find_company_by_keyword(
            company_name=company_name, lang=lang
        )

        return CompanyResponseDto(
            company_name=company_name or find_company_name,
            tags=self.tag_service.get_tags_and_lang(company_id=company_id, lang=lang),
        )

    def add_tags(
        self, company_name: str, tags: list[CompanyTagNameDto], lang: str
    ) -> CompanyResponseDto:
        """
        회사에 태그를 추가한다
        """

        company_name, company_id, find_company_name = self.find_company_by_keyword(
            company_name=company_name, lang=lang
        )

        self.tag_service.associate_tags_to_company(company_id=company_id, tags=tags)

        return CompanyResponseDto(
            company_name=company_name or find_company_name,
            tags=self.tag_service.get_tags_and_lang(company_id=company_id, lang=lang),
        )

    def delete_tag(
        self, company_name: str, tag_name: str, lang: str
    ) -> CompanyResponseDto:
        """
        회사의 태그를 삭제한다
        """

        company_name, company_id, find_company_name = self.find_company_by_keyword(
            company_name=company_name, lang=lang
        )

        tags: list[KeywordTag] = self.tag_service.find_tag(tag_name=tag_name)
        self.tag_service.dissociate_tags_to_company(company_id=company_id, tag_ids=tags)

        return CompanyResponseDto(
            company_name=company_name or find_company_name,
            tags=self.tag_service.get_tags_and_lang(company_id=company_id, lang=lang),
        )
