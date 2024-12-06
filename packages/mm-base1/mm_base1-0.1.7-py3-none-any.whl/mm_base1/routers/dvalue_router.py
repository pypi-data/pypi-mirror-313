from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from mm_base1.app import BaseApp
from mm_base1.models import DValue
from mm_base1.utils import plain_text


def init(app: BaseApp) -> APIRouter:
    router = APIRouter()

    @router.get("")
    def get_dvalues() -> list[DValue]:
        return app.dvalue_collection.find({})

    @router.get("/yaml")
    def get_dvalues_yaml() -> PlainTextResponse:
        return plain_text(app.dvalue_service.get_dvalues_yaml())

    @router.get("/{pk}")
    def get_dvalue(pk: str) -> DValue | None:
        return app.dvalue_collection.get_or_none(pk)

    @router.get("/{pk}/value")
    def get_dvalue_value(pk: str) -> object:
        return app.dvalue.get(pk)

    @router.get("/{pk}/yaml")
    def get_dvalue_yaml(pk: str) -> PlainTextResponse:
        return plain_text(app.dvalue_service.get_dvalue_yaml_value(pk))

    return router
