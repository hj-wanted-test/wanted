from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query

from apps.search.dto import SearchCompanyResponseDto
from apps.search.service import SearchService
from containers import Container
from core.dependency import get_wanted_language

route = APIRouter(
    tags=["1. 검색"],
)


@route.get("/search")
@inject
def search_name(
    language: str = Depends(get_wanted_language),
    query: Optional[str] = Query(None, description="검색어"),
    search_service: SearchService = Depends(Provide[Container.search_service]),
):
    return search_service.search_company(query, language)


@route.get("/tags")
@inject
def search_tags(
    language: str = Depends(get_wanted_language),
    query: Optional[str] = Query(None, description="검색어"),
search_service: SearchService = Depends(Provide[Container.search_service]),
): # -> list[SearchCompanyResponseDto]:
    return search_service.search_tag(query, language)
