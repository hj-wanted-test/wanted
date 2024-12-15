import json

import requests
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import JSONResponse

from apps import routes
from config import conf
from containers import Container
from core.exception import DefaultExceptions


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_all()

    app = FastAPI(
        title=conf.APP_NAME,
    )
    app.container = container
    for r in routes:
        app.include_router(r)

    return app


app = create_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data_insert")
def data_insert():
    with open("../company_tag_sample.json", "r") as f:
        for line in f.readlines():
            r = requests.post("http://localhost:8000/companies", json=json.loads(line))
            print(r.status_code)

    return {"Hello": "World"}



@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        err_message = exc.__dict__["_errors"][0]["msg"]
    except Exception:
        err_message = "Invalid Request"
    ret = {
        "error": {
            "code": 400,
            "message": err_message,
        },
    }

    return JSONResponse(status_code=400, content=jsonable_encoder(ret))


@app.exception_handler(IntegrityError)
@app.exception_handler(DefaultExceptions)
def unicorn_exception_handler(request: Request, exc: Exception):
    http_code = 500
    if hasattr(exc, "http_code"):
        http_code = getattr(exc, "http_code")

    ret = {
        "error": {
            "code": http_code,
            "message": exc.__str__() if conf.DEBUG else "server error",
        },
    }

    return JSONResponse(status_code=http_code, content=jsonable_encoder(ret))
