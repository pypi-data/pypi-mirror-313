import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from functools import partial
from typing import NoReturn

from jinja2 import ChoiceLoader, Environment, PackageLoader
from markupsafe import Markup
from mm_mongo import json_dumps
from mm_std import utc_now
from starlette.requests import Request
from starlette.responses import HTMLResponse

from mm_base1.app import BaseApp
from mm_base1.telegram import CallableAny


def dlog_data_truncate(data: object) -> str:
    if not data:
        return ""
    res = json_dumps(data)
    if len(res) > 100:
        return res[:100] + "..."
    return res


def timestamp(value: datetime | int | None, format_: str = "%Y-%m-%d %H:%M:%S") -> str:
    if isinstance(value, datetime):
        return value.strftime(format_)
    if isinstance(value, int):
        return datetime.fromtimestamp(value).strftime(format_)
    return ""


def empty(value: object) -> object:
    return value if value else ""


def yes_no(
    value: object,
    is_colored: bool = True,
    hide_no: bool = False,
    none_is_false: bool = False,
    on_off: bool = False,
) -> Markup:
    clr = "black"
    if none_is_false and value is None:
        value = False

    if value is True:
        value = "on" if on_off else "yes"
        clr = "green"
    elif value is False:
        if hide_no:
            value = ""
        else:
            value = "off" if on_off else "no"
        clr = "red"
    elif value is None:
        value = ""
    if not is_colored:
        clr = "black"
    return Markup(f"<span style='color: {clr};'>{value}</span>")


def json_url_encode(data: dict[str, object]) -> str:
    return json.dumps(data)


def nformat(
    value: str | int | float | Decimal | None,
    prefix: str = "",
    suffix: str = "",
    separator: str = "",
    hide_zero: bool = True,
    digits: int = 2,
) -> str:
    if value is None or value == "":
        return ""
    if float(value) == 0:
        if hide_zero:
            return ""
        return f"{prefix}0{suffix}"
    if float(value) > 1000:
        value = "".join(
            reversed([x + (separator if i and not i % 3 else "") for i, x in enumerate(reversed(str(int(value))))]),
        )
    else:
        value = round(value, digits)  # type: ignore[assignment, arg-type]

    return f"{prefix}{value}{suffix}"


def raise_(msg: str) -> NoReturn:
    raise RuntimeError(msg)


def form_choices(choices: list[str] | type[Enum], title: str = "") -> list[tuple[str, str]]:
    result = []
    if title:
        result.append(("", title + "..."))
    if isinstance(choices, list):
        for value in choices:
            result.append((value, value))
    else:
        for value in [e.value for e in choices]:
            result.append((value, value))
    return result


@dataclass
class CustomJinja:
    header_info: Callable[..., Markup] | None = None
    header_info_new_line: bool = False
    footer_info: Callable[..., Markup] | None = None
    filters: dict[str, CallableAny] | None = None
    globals: dict[str, CallableAny] | None = None


class Templates:
    def __init__(self, app: BaseApp, custom_jinja: CustomJinja):
        env = Environment(loader=ChoiceLoader([PackageLoader("mm_base1"), PackageLoader("app")]))  # nosec
        env.globals["get_flash_messages"] = get_flash_messages
        env.filters["timestamp"] = timestamp
        env.filters["dt"] = timestamp
        env.filters["empty"] = empty
        env.filters["yes_no"] = yes_no
        env.filters["nformat"] = nformat
        env.filters["n"] = nformat
        env.filters["json_url_encode"] = json_url_encode
        env.filters["dlog_data_truncate"] = dlog_data_truncate
        env.globals["app_config"] = app.app_config
        env.globals["dconfig"] = app.dconfig
        env.globals["dvalue"] = app.dvalue
        env.globals["now"] = utc_now
        env.globals["raise"] = raise_

        env.globals["confirm"] = Markup(""" onclick="return confirm('sure?')" """)
        if custom_jinja.filters:
            env.filters.update(custom_jinja.filters)
        if custom_jinja.globals:
            env.globals.update(custom_jinja.globals)

        header_info = custom_jinja.header_info if custom_jinja.header_info else lambda _: Markup("")
        footer_info = custom_jinja.footer_info if custom_jinja.footer_info else lambda _: Markup("")

        env.globals["header_info"] = partial(header_info, app)
        env.globals["footer_info"] = partial(footer_info, app)

        env.globals["header_info_new_line"] = custom_jinja.header_info_new_line

        self.env = env

    def render(self, request: Request, template_name: str, data: dict[str, object] | None = None) -> HTMLResponse:
        if not data:
            data = {"request": request}
        else:
            data["request"] = request
        html_content = self.env.get_template(template_name).render(data)
        return HTMLResponse(content=html_content, status_code=200)


def flash(request: Request, message: str, is_error: bool = False) -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "error": is_error})


def get_flash_messages(request: Request) -> list[dict[str, object]]:
    return request.session.pop("_messages") if "_messages" in request.session else []
