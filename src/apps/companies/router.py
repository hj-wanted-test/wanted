from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from apps.companies.dto import (CompanyRequestDto, CompanyResponseDto,
                                CompanyTagNameDto)
from apps.companies.service.company_service import CompanyService
from containers import Container
from core.dependency import get_wanted_language
from core.exception import DefaultExceptions

route = APIRouter(
    prefix="/companies",
    tags=["2. 회사"],
)


@route.get("/{company_name}")
@inject
def get_company(
    language: str = Depends(get_wanted_language),
    company_name: str = None,
    company_service: CompanyService = Depends(Provide[Container.company_service]),
):
    return company_service.get_company_by_name(company_name, language)


@route.post("")
@inject
def create_company(
    request: CompanyRequestDto,
    language: str = Depends(get_wanted_language),
    company_service: CompanyService = Depends(Provide[Container.company_service]),
):

    company_service.create_company(request)

    return CompanyResponseDto(
        company_name=request.company_name.get(language)
        or list(request.company_name.values())[0],
        tags=[tag.tag_name[language] for tag in request.tags],
    )


@route.put("/{company_name}/tags")
@inject
def update_company_tags(
    company_name: str = None,
    request: list[CompanyTagNameDto] = None,
    language: str = Depends(get_wanted_language),
    company_service: CompanyService = Depends(Provide[Container.company_service]),
):
    return company_service.add_tags(
        company_name=company_name, tags=request, lang=language
    )


@route.delete("/{company_name}/tags/{tag_name}")
@inject
def delete_company_tag(
    language: str = Depends(get_wanted_language),
    company_name: str = None,
    tag_name: str = None,
    company_service: CompanyService = Depends(Provide[Container.company_service]),
):
    return company_service.delete_tag(company_name=company_name, tag_name=tag_name, lang=language)
