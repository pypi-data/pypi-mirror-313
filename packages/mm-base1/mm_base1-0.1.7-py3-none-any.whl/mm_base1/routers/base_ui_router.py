from fastapi import APIRouter
from mm_mongo import mongo_query
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from wtforms import BooleanField, Form, IntegerField, SelectField, TextAreaField

from mm_base1.app import BaseApp
from mm_base1.jinja import Templates, flash, form_choices
from mm_base1.models import DConfigType
from mm_base1.telegram import BaseTelegram
from mm_base1.utils import depends_form, redirect


class ImportDConfigForm(Form):  # type: ignore[misc]
    yaml_data = TextAreaField(render_kw={"rows": 20})


class DLogsFilterForm(Form):  # type: ignore[misc]
    category = SelectField()
    limit = IntegerField(default=100)


class UpdateValueForm(Form):  # type: ignore[misc] # for dconfig and dvalue
    yaml_value = TextAreaField(render_kw={"rows": 20})
    multiline_string = BooleanField()


class UpdateDConfigMultilineForm(Form):  # type: ignore[misc]
    value = TextAreaField(render_kw={"rows": 20})


def init(app: BaseApp, templates: Templates, telegram: BaseTelegram) -> APIRouter:
    router = APIRouter()

    @router.get("/system")
    def system_page(req: Request) -> HTMLResponse:
        stats = app.system_service.get_stats()
        telegram_is_started = telegram.is_started

        return templates.render(req, "system.j2", {"stats": stats, "telegram_is_started": telegram_is_started})

    @router.get("/dconfig")
    def dconfig_page(req: Request) -> HTMLResponse:
        return templates.render(req, "dconfig.j2")

    @router.get("/update-dconfig")
    def update_dconfig_page(req: Request) -> HTMLResponse:
        form = ImportDConfigForm()
        return templates.render(req, "update_dconfig.j2", {"form": form})

    @router.get("/update-dconfig-multiline/{key}")
    def update_dconfig_multiline_page(req: Request, key: str) -> HTMLResponse:
        form = UpdateDConfigMultilineForm(data={"value": app.dconfig.get(key)})
        return templates.render(req, "update_dconfig_multiline.j2", {"form": form, "key": key})

    @router.get("/dvalue")
    def dvalue_page(req: Request) -> HTMLResponse:
        return templates.render(req, "dvalue.j2")

    @router.get("/update-dvalue/{key}")
    def update_dvalue_page(req: Request, key: str) -> HTMLResponse:
        form = UpdateValueForm(yaml_value=app.dvalue_service.get_dvalue_yaml_value(key))
        return templates.render(req, "update_dvalue.j2", {"form": form, "key": key})

    @router.get("/dlogs")
    def dlogs_page(req: Request) -> HTMLResponse:
        category_stats = {}
        for category in app.dlog_collection.collection.distinct("category"):
            category_stats[category] = app.dlog_collection.count({"category": category})
        form = DLogsFilterForm(req.query_params)
        form.category.choices = form_choices(list(category_stats.keys()), title="category")
        query = mongo_query(category=form.data["category"])
        dlogs = app.dlog_collection.find(query, "-created_at", form.data["limit"])
        return templates.render(req, "dlogs.j2", {"dlogs": dlogs, "form": form, "category_stats": category_stats})

    # actions

    @router.post("/update-dconfig-admin")
    def update_dconfig_admin(req: Request, form_data: FormData = depends_form) -> RedirectResponse:
        data = {
            x: form_data.get(x) for x in app.dconfig.get_non_hidden_keys() if app.dconfig.get_type(x) != DConfigType.MULTILINE
        }
        app.dconfig_service.update(data)  # type: ignore[arg-type]
        flash(req, "dconfigs were updated")
        return redirect("/dconfig")

    @router.post("/update-dconfig-yaml")
    def update_dconfig_yaml(form_data: FormData = depends_form) -> bool | None:
        return app.dconfig_service.update_dconfig_yaml(form_data["yaml_data"])  # type: ignore[arg-type]

    @router.post("/update-dvalue/{key}")
    def update_dvalue(key: str, form_data: FormData = depends_form) -> RedirectResponse:
        form = UpdateValueForm(form_data)
        app.dvalue_service.set_dvalue_yaml_value(key, form.yaml_value.data, form.multiline_string.data)
        return redirect("/dvalue")

    @router.post("/update-dconfig-multiline/{key}", response_model=None)
    def update_dconfig_multiline(
        req: Request,
        key: str,
        form_data: FormData = depends_form,
    ) -> RedirectResponse | dict[str, object]:
        form = UpdateDConfigMultilineForm(form_data)
        if form.validate():
            app.dconfig_service.update_multiline(key, form.data["value"])
            flash(req, f"dconfig '{key}' was updated")
            return redirect(f"/update-dconfig-multiline/{key}")
        return {"errors": form.errors}

    return router
