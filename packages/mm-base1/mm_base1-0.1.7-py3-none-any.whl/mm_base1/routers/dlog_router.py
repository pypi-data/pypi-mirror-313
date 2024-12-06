from fastapi import APIRouter
from mm_mongo import mongo_query
from pymongo.results import DeleteResult

from mm_base1.app import BaseApp
from mm_base1.models import DLog


def init(app: BaseApp) -> APIRouter:
    router = APIRouter()

    @router.get("")
    def get_dlogs(category: str | None = None, limit: int = 100) -> list[DLog]:
        return app.dlog_collection.find(mongo_query(category=category), "-created_at", limit=limit)

    @router.delete("", response_model=None)
    def delete_all_dlogs() -> DeleteResult:
        return app.dlog_collection.delete_many({})

    @router.get("/{pk}")
    def get_dlog(pk: str) -> DLog:
        return app.dlog_collection.get(pk)

    @router.delete("/{pk}", response_model=None)
    def delete_dlog(pk: str) -> DeleteResult:
        return app.dlog_collection.delete_by_id(pk)

    @router.delete("/category/{category}", response_model=None)
    def delete_by_category(category: str) -> DeleteResult:
        return app.dlog_collection.delete_many({"category": category})

    return router
