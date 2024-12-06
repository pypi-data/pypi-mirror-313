from collections.abc import Callable
from dataclasses import dataclass
from logging import Logger

from mm_std import Result

from app.config import DConfigSettings, DValueSettings
from mm_base1.config import BaseAppConfig


@dataclass
class BaseServiceParams:
    app_config: BaseAppConfig
    logger: Logger
    dconfig: DConfigSettings
    dvalue: DValueSettings
    dlog: Callable[..., None]
    send_telegram_message: Callable[[str], Result[list[int]]]


class BaseService:
    def __init__(self, params: BaseServiceParams):
        self.app_config = params.app_config
        self.logger = params.logger
        self.dconfig = params.dconfig
        self.dvalue = params.dvalue
        self.dlog = params.dlog
        self.send_telegram_message = params.send_telegram_message
