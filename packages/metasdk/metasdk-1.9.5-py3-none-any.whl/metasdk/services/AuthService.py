import urllib.parse
from typing import Dict, List, TypedDict

import requests

from metasdk import UnexpectedError
from metasdk.exceptions import ForbiddenError, RequestError


class AuthUserInfo(TypedDict):
    auth_user_id: int
    company_id: int
    is_admin: bool


class AuthService:
    def __init__(self, app):
        """
        Класс проверяет авторизационный токен и определяет пользователя.

        :param app: metasdk.MetaApp
        """
        self.__app = app
        self.__admin_role_id: int = 6

    def verify_access_token(self, token: str, required_scopes: List = None, include_auth_info: bool = False) -> Dict:
        """
        Проверяет токен, определяет юзера и его права.

        Проверяет корректность токена. На основе ответа от сервера верификации
        добавляет дополнительную информацию о пользователе ,совершившим запрос.
        :param token: Access Token.
        :param required_scopes: список скоупов, которые требуются сервису.
        :param include_auth_info: добавить auth_info в результат.
        Доступны "accountmanagement" и "datahub".
        :return: ответ от сервера верификации.
        """
        auth_info = self._authenticate_user(token)
        if required_scopes:
            self._check_scopes(token_scopes=auth_info["scopes"], required_scopes=required_scopes)
        user_info = self.__set_permissions(auth_info=auth_info)
        if include_auth_info:
            user_info = dict(user_info)
            user_info.update(auth_info)
        return user_info

    def _authenticate_user(self, token: str) -> Dict:
        """
        Совершает запрос к серверу верификации на проверку Access токена.

        :param token: Access Token
        :return: ответ от сервера верификации
        """
        verify_url = "oauth2/verifyJWTAccessToken"
        url = urllib.parse.urljoin(self.__app.auth_service_host, verify_url)
        response = requests.get(url, params={"assertion": token})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            raise ForbiddenError("Invalid authorization token")
        else:
            raise UnexpectedError("Unexpected error with token validation")

    def _identify_user(self, token_user_id: int) -> int:
        """
        Проверяет user_id пользователя отправившего токен.

        Если получен токен сервисного аккаунта, то возвращает user_id владельца.
        В ином случае user_id из токена
        :param meta: мета.
        :param token_user_id: user_id, полученный от авторизационного сервера.
        :return: user ID.
        """
        query = """
        SELECT author_user_id  
        FROM meta.service_account_key 
        WHERE service_account_id = :service_account_id
        """
        data = self.__app.db("meta").one(query, {"service_account_id": int(token_user_id)})
        if data:
            return data["author_user_id"]
        else:
            return token_user_id

    def _check_scopes(self, token_scopes: List[str], required_scopes: List[str]):
        if not required_scopes or not isinstance(required_scopes, list):
            raise TypeError("Invalid format of the required_scopes")

        if not token_scopes or not isinstance(token_scopes, list):
            raise TypeError("Invalid format of the token_scopes")

        check = all(scope in token_scopes for scope in required_scopes)
        if not check:
            raise ForbiddenError("Not enough scopes")

        return True

    def _get_user_info(self, user_id: int) -> Dict:
        """
        Получает информацию о пльзователе по ID.

        :param meta: мета.
        :param user_id: ID пользователя в Мете.
        :return: информация о пользователе
        """
        query = """
        select company_id, roles from public.users where id = :user_id
        """
        result = self.__app.db("meta").one(query, {"user_id": int(user_id)})
        if not result:
            raise RequestError("Пользователь не найден")
        return result

    def __set_permissions(self, auth_info: Dict) -> AuthUserInfo:
        """
        Дополняет информацию о владельце токена.

        :param auth_info: ответ от сервера верификации.
        :return: None.
        """
        auth_user_id = self._identify_user(token_user_id=int(auth_info["userId"]))
        user_info = self._get_user_info(auth_user_id)
        company_id = user_info["company_id"]
        is_admin = True if self.__admin_role_id in user_info["roles"] else False
        return {
            "auth_user_id": int(auth_user_id),
            "company_id": int(company_id),
            "is_admin": is_admin,
        }
