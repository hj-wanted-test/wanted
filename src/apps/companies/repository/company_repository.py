from apps.companies.model import Company
from core.repository import Repository


class CompanyRepository(Repository):

    __table__ = Company

