from dependency_injector import containers, providers

from apps.companies.repository.company_repository import CompanyRepository
from apps.companies.repository.company_tag_repository import CompanyTagRepository
from apps.companies.repository.tag_repository import TagRepository
from apps.companies.service.company_service import CompanyService
from apps.companies.service.tag_service import TagService
from apps.search.repository.keyword_company_repository import KeywordCompanyRepository
from apps.search.repository.keyword_tag_repository import KeywordTagRepository
from apps.search.service import SearchService

from config import conf
from core.db import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["apps"])

    db = providers.Singleton(Database, db_url=conf.DB_URL, echo=conf.ENV != "PROD")

    company_repository = providers.Factory(
        CompanyRepository,
        session_factory=db.provided.session,
    )

    tag_repository = providers.Factory(
        TagRepository,
        session_factory=db.provided.session,
    )

    company_tag_repository = providers.Factory(
        CompanyTagRepository,
        session_factory=db.provided.session,
    )

    keyword_company_repository = providers.Factory(
        KeywordCompanyRepository,
        session_factory=db.provided.session,
    )

    keyword_tag_repository = providers.Factory(
        KeywordTagRepository,
        session_factory=db.provided.session,
    )

    tag_service = providers.Factory(
        TagService,
        tag_repository=tag_repository,
        company_tag_repository=company_tag_repository,
        keyword_tag_repository=keyword_tag_repository,
    )

    company_service = providers.Factory(
        CompanyService,
        tag_service=tag_service,
        company_repository=company_repository,
        keyword_company_repository=keyword_company_repository,
    )
    search_service = providers.Factory(
        SearchService,
        keyword_company_repository=keyword_company_repository,
        keyword_tag_repository=keyword_tag_repository,
    )
