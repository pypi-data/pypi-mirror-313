import os
import threading
import tracemalloc

from mm_mongo import DatabaseAny
from mm_std import Scheduler

from app.config import AppConfig
from mm_base1.services.dconfig_service import DConfigStorage
from mm_base1.services.dvalue_service import DValueStorage


class SystemService:
    def __init__(
        self,
        app_config: AppConfig,
        dconfig: DConfigStorage,
        dvalue: DValueStorage,
        scheduler: Scheduler,
        database: DatabaseAny,
    ) -> None:
        self.app_config = app_config
        self.dconfig = dconfig
        self.dvalue = dvalue
        self.logfile = self.app_config.data_dir + "/app.log"
        self.scheduler = scheduler
        self.database = database

    def read_logfile(self) -> str:
        with open(self.logfile, encoding="utf-8") as f:
            return f.read()

    def clean_logfile(self) -> None:
        with open(self.logfile, "w", encoding="utf-8") as f:
            f.write("")

    def get_stats(self) -> dict[str, object]:
        threads = []
        for t in threading.enumerate():
            thread_info = {"name": t.name, "daemon": t.daemon}
            target = t.__dict__.get("_target")
            if target:
                thread_info["func"] = target.__qualname__
            threads.append(thread_info)

        db_stats = {}
        for col in self.database.list_collection_names():
            db_stats[col] = self.database[col].estimated_document_count()

        return {
            "db": db_stats,
            "logfile": os.path.getsize(self.logfile),
            "dconfig": len(self.dconfig.keys()),
            "dvalue": len(self.dvalue.keys()),
            "dlog": self.database["dlog"].count_documents({}),
            "scheduler": self.scheduler.jobs,
            "threads": threads,
        }

    @staticmethod
    def tracemalloc_snapshot(key_type: str = "lineno", limit: int = 30) -> str:
        result = ""
        snapshot = tracemalloc.take_snapshot()
        for stat in snapshot.statistics(key_type)[:limit]:
            result += str(stat) + "\n"
        return result
