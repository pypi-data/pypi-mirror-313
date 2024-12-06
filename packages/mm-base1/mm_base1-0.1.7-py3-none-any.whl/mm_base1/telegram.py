import functools
from collections.abc import Callable
from threading import Thread
from typing import Any

from mm_std import synchronized
from telebot import TeleBot
from telebot.types import Message
from telebot.util import split_string

from app.app import App

type CallableAny = Callable[..., Any]


class BaseTelegram:
    """Telegram is an alternative UI to the web API for the project. It works via telegram commands.
    If you need just to send a message to the project channel / group, use core.send_telegram_message()"""

    def __init__(self, app: App):
        self.app = app
        self.bot: TeleBot | None = None
        self.is_started = False
        self.admins: list[int] = []

    @synchronized
    def start(self) -> str | None:
        """
        Telegram bot can be started only if these bot settings are set:
        - telegram_token
        - telegram_admins
        - telegram_polling
        """
        telegram_token = self.app.dconfig.get("telegram_token")
        telegram_polling = self.app.dconfig.get("telegram_polling")

        try:
            self.admins = []
            for admin in self.app.dconfig.get("telegram_admins", "").split(","):  # type: ignore[attr-defined]
                admin = admin.strip()
                if admin:
                    self.admins.append(int(admin))
        except Exception as err:
            self.app.dlog("telegram_parse_admins", {"error": str(err)})
            return f"telegram_parse_admins: {err}"

        if telegram_token and telegram_polling and self.admins:
            Thread(target=self._start, args=(telegram_token,)).start()
            return None

        return "there are some unset configs: telegram_token or telegram_polling or telegram_admins"

    def _start(self, token: str) -> None:
        try:
            self.bot = TeleBot(token, skip_pending=True)
            self._init_base_commands()
            self.init_commands()
            self.is_started = True
            self.app.logger.debug("telegram bot started")
            self.bot.polling(none_stop=True)

        except Exception as e:
            self.is_started = False
            self.app.dlog("telegram_polling", {"error": str(e)})
            self.app.logger.error("telegram polling: %s", e)

    @synchronized
    def stop(self) -> None:
        self.is_started = False
        if self.bot:
            self.bot.stop_bot()
        self.app.logger.debug("telegram stopped")

    def _init_base_commands(self) -> None:
        if self.bot is None:
            return None

        @self.bot.message_handler(commands=["start", "help"])  # type: ignore[misc]
        @self.auth(admins=self.admins, bot=self.bot)
        def help_handler(message: Message) -> None:
            self._send_message(message.chat.id, self.app.app_config.telegram_bot_help)

        @self.bot.message_handler(commands=["ping"])  # type: ignore[misc]
        @self.auth(admins=self.admins, bot=self.bot)
        def ping_handler(message: Message) -> None:
            text = message.text.replace("/ping", "").strip()
            self._send_message(message.chat.id, f"pong {text}")

    def init_commands(self) -> None:
        pass

    def _send_message(self, chat_id: int, message: str) -> None:
        for text in split_string(message, 4096):
            self.bot.send_message(chat_id, text)  # type:ignore

    def send_to_channel(self, message: str) -> None:
        self._send_message(self.app.dconfig.get("telegram_chat_id"), message)  # type:ignore

    @staticmethod
    def auth(*, admins: list[int], bot: TeleBot) -> Callable[..., Any]:
        def outer(func: CallableAny) -> CallableAny:
            @functools.wraps(func)
            def wrapper(message: Message) -> object:
                if message.chat.id in admins:
                    return func(message)
                bot.send_message(message.chat.id, "Who are you?")

            return wrapper

        return outer
