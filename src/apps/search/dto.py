from pydantic import BaseModel


class SearchCompanyResponseDto(BaseModel):
    company_name: str
