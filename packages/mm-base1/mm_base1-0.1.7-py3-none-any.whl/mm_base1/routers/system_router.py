import tracemalloc

from fastapi import APIRouter
from mm_std import Result
from starlette.responses import PlainTextResponse

from mm_base1.app import BaseApp
from mm_base1.telegram import BaseTelegram


def init(app: BaseApp, telegram: BaseTelegram) -> APIRouter:
    router = APIRouter()

    @router.get("/logfile", response_class=PlainTextResponse)
    def view_logfile() -> str:
        return app.system_service.read_logfile()

    @router.delete("/logfile")
    def clean_logfile() -> bool:
        app.system_service.clean_logfile()
        return True

    @router.post("/tracemalloc/start")
    def start_tracemalloc() -> dict[str, str]:
        tracemalloc.start()
        return {"message": "tracemalloc was started"}

    @router.post("/tracemalloc/stop")
    def stop_tracemalloc() -> dict[str, str]:
        tracemalloc.stop()
        return {"message": "tracemalloc was stopped"}

    @router.get("/tracemalloc/snapshot", response_class=PlainTextResponse)
    def snapshot_tracemalloc() -> str:
        return app.system_service.tracemalloc_snapshot()

    @router.post("/test-telegram-message", response_model=None)
    def test_telegram_message() -> Result[list[int]]:
        message = "bla bla bla " * 10
        return app.send_telegram_message(message)

    @router.get("/telegram-bot")
    def get_telegram_bot_status() -> bool:
        return telegram.is_started

    @router.post("/telegram-bot/start")
    def start_telegram_bot() -> dict[str, str]:
        err = telegram.start()
        return {"error": err} if err else {"start": "ok"}

    @router.post("/telegram-bot/stop")
    def stop_telegram_bot() -> dict[str, str]:
        telegram.stop()
        return {"stop": "ok"}

    return router
