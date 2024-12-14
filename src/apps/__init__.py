from apps.companies.router import route as companies_router
from apps.search.router import route as search_router

routes = [
    search_router,
    companies_router,
]
