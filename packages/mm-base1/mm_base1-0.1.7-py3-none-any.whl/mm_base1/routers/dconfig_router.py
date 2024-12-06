from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from mm_base1.app import BaseApp
from mm_base1.utils import plain_text


def init(app: BaseApp) -> APIRouter:
    router = APIRouter()

    @router.get("/yaml")
    def get_dconfig_yaml() -> PlainTextResponse:
        return plain_text(app.dconfig_service.export_dconfig_yaml())

    return router
