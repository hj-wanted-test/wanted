from typing import Dict

from pydantic import BaseModel


class CompanyTagNameDto(BaseModel):
    tag_name: Dict[str, str]

class CompanyRequestDto(BaseModel):
    company_name: Dict[str, str]
    tags: list[CompanyTagNameDto]

class CompanyResponseDto(BaseModel):
    company_name: str
    tags: list[str]
