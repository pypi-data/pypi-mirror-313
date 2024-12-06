from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional, ParamSpec


class Message(ABC):
    """Абстрактный класс сообщения"""
    messenger_id = "abstract"

    @abstractmethod
    def generate_unique_id(self) -> str:
        """
        Генерирует уникальный идентификатор сообщения по его атрибутам.

        Абстрактный метод. В наследниках необходимо переопределить.
        :return: Уникальный идентификатор сообщения.
        """
        pass

    def __init__(
        self,
        user_id: str,
        body: str,
        template: str = "",
        unique_id: Optional[str] = None,
        author_user_id: Optional[int] = None,
        **kwargs: ParamSpec.kwargs,
    ) -> None:
        """
        Инициализирует экземпляр класса.

        :param user_id: Идентификатор пользователя-адресата.
        :param body: Строка с телом отправляемого сообщения.
        :param template: Идентификатор шаблона сообщения.
        :param unique_id: Уникальный идентификатор сообщения.
        :param kwargs: Опциональные параметры, актуальные для отдельных каналов отправки сообщений.
        :return: None.
        """
        self._messenger = self.messenger_id
        self._user_id = user_id
        self._body = body
        self._template = template
        self._custom_unique_id = unique_id
        self._author_user_id = author_user_id
        self._kwargs = kwargs

    def to_dict(self) -> dict[str, int | str]:
        """
        Возвращает словарь с данными сообщения.

        :return: Словарь с данными сообщения. Удобно передавать методам DbQueryService.
        """

        return {
            "messenger": self._messenger,
            "user_id": self._user_id,
            "body": self._body,
            "template": self._template,
            "unique_id": self._custom_unique_id or self.generate_unique_id(),
            "author_user_id": self._author_user_id
        }


class WebhookMessage(Message):
    """Класс сообщения, отправляемого вебхуком"""
    messenger_id = "webhook"

    def generate_unique_id(self) -> str:
        """
        Генерирует уникальный идентификатор сообщения по его атрибутам.

        В kwargs экземпляра можно передать параметр "uniqualizer",
        и он будет добавлен в начало unique_id. Так, скажем, можно проверять,
        был ли уже отправлен вебхук по конкретной записи из meta.object_log. 
        :return: Уникальный идентификатор сообщения.
        """
        unique_id_head = "webhook"
        if uniqualizer := self._kwargs.get("uniqualizer"):
            unique_id_head += f"_{uniqualizer}"       
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        return f"{unique_id_head}_{self._user_id}_{timestamp}"


class TelegramMessage(Message):
    """Класс сообщения, отправляемого через Telegram"""
    messenger_id = "telegram"

    def generate_unique_id(self) -> str:
        """
        Генерирует уникальный идентификатор сообщения по его атрибутам.

        :return: Уникальный идентификатор сообщения.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        return f"custom_message_{self._user_id}_{timestamp}"


class MailService:
    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__options = {}
        self.__data_get_cache = {}
        self.__metadb = app.db("meta")
        self.log = app.log

    def submit_mail(
        self,
        send_from: str,
        send_to: str,
        subject: str,
        body: str,
        unique_id: Optional[str] = None,
    ) -> None:
        """
        Добавляет письмо в очередь на отправку (фактически — запись в таблицу meta.mail).

        :param send_from: Отправитель.
        :param send_to: Получатель.
        :param subject: Тема письма.
        :param body: Тело письма. Можно с HTML.
        :param unique_id: Уникальный идентификатор письма.
            Лучше всего подойдет md5 + человекочитаемый префикс.
            Письмо с существующим unique_id не будут добавлено.
        :return: None.
        """
        self.__metadb.update(
            """
                INSERT INTO meta.mail(
                    "template",
                    "from",
                    "to",
                    "subject",
                    "body",
                    "attachments",
                    "unique_id"
                )
                VALUES ('meta', :send_from, :send_to, :subject, :body, null, :unique_id)
                ON CONFLICT (unique_id) DO NOTHING
            """,
            {
                "send_from": send_from,
                "send_to": send_to,
                "subject": subject,
                "body": body,
                "unique_id": unique_id,
            },
        )

    def submit_message(self, message: Message) -> None:
        """
        Добавляет сообщение в очередь на отправку (фактически — запись в таблицу meta.messenger).

        :param message: Экземпляр класса-наследника Message.
        :return: None.
        """
        self.__metadb.update(
            """
                INSERT INTO meta.messenger(
                    messenger,
                    user_id,
                    body,
                    unique_id,
                    author_user_id
                )
                VALUES (
                    :messenger::text,
                    :user_id::text,
                    :body::text,
                    :unique_id::text,
                    COALESCE(:author_user_id, valera_user_id())::bigint
                )
                ON CONFLICT (unique_id) DO NOTHING
            """,
            message.to_dict(),
        )
