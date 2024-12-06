import traceback
from collections.abc import AsyncGenerator, Callable, Coroutine
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Security
from fastapi.applications import AppType
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery
from mm_std import hr
from starlette import status
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
)
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_403_FORBIDDEN
from starlette.types import Lifespan

from mm_base1.app import BaseApp
from mm_base1.errors import UserError
from mm_base1.jinja import Templates
from mm_base1.json_encoder import add_custom_encodings
from mm_base1.routers import (
    base_ui_router,
    dconfig_router,
    dlog_router,
    dvalue_router,
    system_router,
)
from mm_base1.telegram import BaseTelegram


@dataclass
class AppRouter:
    router: APIRouter
    tag: str
    prefix: str = ""


def lifespan(app: BaseApp, telegram: BaseTelegram) -> Lifespan[AppType]:
    @asynccontextmanager
    async def lifespan_(_fastapi_app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: UP043
        yield
        app.logger.debug("server shutdown")
        telegram.stop()
        app.shutdown()

    return lifespan_


class Server:
    api_key_name = "access-token"
    key_query = Security(APIKeyQuery(name=api_key_name, auto_error=False))
    key_header = Security(APIKeyHeader(name=api_key_name, auto_error=False))
    key_cookie = Security(APIKeyCookie(name=api_key_name, auto_error=False))

    def __init__(self, app: BaseApp, telegram: BaseTelegram, routers: list[AppRouter], templates: Templates):
        self.app = app
        self.telegram = telegram
        self.server = FastAPI(
            title=app.app_config.app_name,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            openapi_tags=app.app_config.tags_metadata,
            middleware=[Middleware(SessionMiddleware, secret_key=self.app.app_config.access_token)],
            lifespan=lifespan(app, telegram),
        )
        self.templates = templates
        self._configure_server()
        self._configure_openapi()
        self._configure_routers(routers)
        telegram.start()

    def get_server(self) -> FastAPI:
        return self.server

    def _configure_routers(self, routers: list[AppRouter]) -> None:
        base_routers = [
            AppRouter(dconfig_router.init(self.app), "dconfig", "/api/dconfigs"),
            AppRouter(dvalue_router.init(self.app), "dvalue", "/api/dvalues"),
            AppRouter(dlog_router.init(self.app), "dlog", "/api/dlogs"),
            AppRouter(system_router.init(self.app, self.telegram), "system", "/api/system"),
            AppRouter(base_ui_router.init(self.app, self.templates, self.telegram), "base-ui"),
        ]

        for r in base_routers + routers:
            self.server.include_router(
                r.router,
                prefix=r.prefix,
                dependencies=[Depends(self._get_api_key())],
                tags=[r.tag],
            )

    def _configure_server(self) -> None:
        @self.server.exception_handler(Exception)
        async def exception_handler(_request: Request, err: Exception) -> PlainTextResponse:
            code = getattr(err, "code", None)

            message = str(err)

            hide_stacktrace = isinstance(err, UserError)
            if code in [400, 401, 403, 404, 405]:
                hide_stacktrace = True

            if not hide_stacktrace:
                self.app.logger.exception(err)
                message += "\n\n" + traceback.format_exc()

            if not self.app.app_config.debug:
                message = "error"

            return PlainTextResponse(message, status_code=500)

        # @self.server.on_event("shutdown")
        # def shutdown_server() -> None:
        #     self.app.logger.debug("server shutdown")
        #     self.telegram.stop()
        #     self.app.shutdown()

        current_dir = Path(__file__).parent.absolute()
        self.server.mount("/static", StaticFiles(directory=current_dir.joinpath("static")), name="static")
        add_custom_encodings()

    def _configure_openapi(self) -> None:
        @self.server.get("/openapi.json", tags=["openapi"], include_in_schema=False)
        async def get_open_api_endpoint(_api_key: APIKey = Depends(self._get_api_key())) -> JSONResponse:
            return JSONResponse(
                get_openapi(
                    title=self.app.app_config.app_name,
                    version=self.app.app_config.app_version,
                    routes=self.server.routes,
                    tags=self.app.app_config.tags_metadata,
                ),
            )

        @self.server.get("/api", tags=["openapi"], include_in_schema=False)
        async def get_documentation(api_key: APIKey = Depends(self._get_api_key())) -> HTMLResponse:
            response = get_swagger_ui_html(openapi_url="/openapi.json", title=self.app.app_config.app_name)
            response.set_cookie(
                self.api_key_name,
                value=str(api_key),
                domain=self.app.app_config.domain,
                httponly=True,
                secure=True,
                max_age=60 * 60 * 24 * 30,
            )
            return response

        @self.server.get("/login", tags=["auth"])
        async def route_login_page(req: Request) -> HTMLResponse:
            return self.templates.render(req, "login.j2")

        @self.server.post("/login", tags=["auth"])
        async def route_login_action(access_token: str = Form(...)) -> RedirectResponse:
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(
                self.api_key_name,
                value=access_token,
                domain=self.app.app_config.domain,
                httponly=True,
                max_age=60 * 60 * 24 * 30,
            )
            return response

        @self.server.get("/logout", tags=["auth"])
        async def route_logout_and_remove_cookie() -> RedirectResponse:
            response = RedirectResponse(url="/")
            response.delete_cookie(self.api_key_name, domain=self.app.app_config.domain)
            return response

        @self.server.get("/api-post/{url:path}")
        def api_post(url: str, request: Request, api_key: APIKey = Depends(self._get_api_key())) -> object:
            return self._api_method("post", url, request, api_key)

        @self.server.get("/api-delete/{url:path}")
        def api_delete(url: str, request: Request, api_key: APIKey = Depends(self._get_api_key())) -> object:
            return self._api_method("delete", url, request, api_key)

    def _api_method(self, method: str, url: str, req: Request, api_key: APIKey) -> object:
        base_url = str(req.base_url)
        if not base_url.endswith("/"):
            base_url = base_url + "/"
        url = base_url + "api/" + url
        if self.app.app_config.use_https:
            url = url.replace("http://", "https://", 1)
        if req.query_params:
            q = ""
            for k, v in req.query_params.items():
                q += f"{k}={v}&"
            url += f"?{q}"
        headers = {self.api_key_name: api_key}
        res = hr(url, method=method, headers=headers, params=dict(req.query_params), timeout=600)
        if res.content_type and res.content_type.startswith("text/plain"):
            return PlainTextResponse(res.body)
        if res.json:
            return res.json
        return res.body

    def _get_api_key(self) -> Callable[[str, str, str], Coroutine[Any, Any, str]]:
        async def _get_api_key(
            query: str = Server.key_query,
            header: str = Server.key_header,
            cookie: str = Server.key_cookie,
        ) -> str:
            if query == self.app.app_config.access_token:
                return query
            if header == self.app.app_config.access_token:
                return header
            if cookie == self.app.app_config.access_token:
                return cookie
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="access denied")

        return _get_api_key
