from fastapi import Depends
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


async def get_form_data(request: Request) -> FormData:
    return await request.form()


depends_form = Depends(get_form_data)


def plain_text(content: object) -> PlainTextResponse:
    return PlainTextResponse(content)


def redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url, status_code=HTTP_303_SEE_OTHER)


def get_registered_attributes(obj: object) -> list[str]:
    return [x for x in dir(obj) if not x.startswith("_")]
