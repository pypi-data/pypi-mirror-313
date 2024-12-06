from mm_mongo import DatabaseAny, MongoCollection

from mm_base1.models import DConfig, DLog, DValue


class BaseDB:
    def __init__(self, database: DatabaseAny) -> None:
        self.dconfig: MongoCollection[DConfig] = DConfig.init_collection(database)
        self.dvalue: MongoCollection[DValue] = DValue.init_collection(database)
        self.dlog: MongoCollection[DLog] = DLog.init_collection(database)
