import json
from time import sleep

import requests
import time

from metasdk.exceptions import BadRequestError, UnexpectedError


class StarterService:
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def __init__(self, app, db, starter_api_url):
        """
        Прямые запросы к БД скорее всего уйдут в апи запускатора, так как скорее всего пбудет много БД для тасков запускатора, так как
        Если будет 100500 шард, то врядли все будет в одной БД
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__options = {}
        self.__data_get_cache = {}
        self.__metadb = db
        self.__starter_api_url = starter_api_url
        self.log = app.log
        self.max_retries = 30

    def update_task_result_data(self, task, sleep_sec: int | float = 15) -> None:
        """
        Обновляет результат работы таска запускатора.
        :param task: данные таска.
        :param sleep_sec: время ожидания между попытками обновления.
        :return: None.
        """
        # импорт тут, так как глобально над классом он не работает
        from metasdk import DEV_STARTER_STUB_URL

        if any([
            not task.get("serviceId"),
            self.__starter_api_url == DEV_STARTER_STUB_URL,
        ]):
            # В этом случае предполагается, что таск запущен локально.
            self.log.info("STARTER DEV. Результат таска условно обновлен", {"task": task})
            return

        self.log.info("Сохраняем состояние в БД", {"result_data": task['result_data']})
        if sleep_sec < 1:
            sleep_sec = 1
        if sleep_sec > 600:
            sleep_sec = 600
        max_tries = 10
        current_try = 0
        while True:
            url = self.__starter_api_url + '/services/' + task.get('serviceId') + '/tasks/updateResultData'
            try:
                resp = requests.post(
                    url=url,
                    data=json.dumps(task),
                    headers=self.headers,
                    timeout=15
                )
                """
                Осуществляем попытки, пока не получим код 200
                Иначе делаем паузу и пробуем снова
                """
                if resp.status_code == 200:
                    return
                else:
                    self.log.warning("Некорректный http статус при обновлении result_data задачи, пробуем снова", {
                        "task": task
                    })
                    current_try = current_try + 1
                    if current_try >= max_tries:
                        self.log.error("Некорректный http статус при обновлении result_data задачи, прерываем выполнение", {
                            "status_code": resp.status_code,
                            "task": task,
                            "response_text": resp.text
                        })
                        raise IOError("Starter response read error: " + resp.text)

            except Exception:
                self.log.warning("Неизвестная ошибка при обновлении result_data задачи, пробуем снова", {
                    "task": task
                })
                current_try = current_try + 1
                if current_try >= max_tries:
                    self.log.error("Неизвестная ошибка при обновлении result_data задачи, прерываем выполнение", {
                        "task": task
                    })
                    raise IOError("Starter response read error")
            time.sleep(sleep_sec)

    def await_task(self, task_id, service_id, callback_fn=None, sleep_sec=15):
        """
        Подождать выполнения задачи запускатора
        При работе с Координатором (запросом данных по API) мы будем обращаться к API до тех пор, пока не будет получен корректный ответ

        :param task_id: ID задачи, за которой нужно следить
        :param service_id: ID сервиса
        :param callback_fn: Функция обратного вызова, в нее будет передаваться task_info и is_finish как признак, что обработка завершена
        :param sleep_sec: задержка между проверкой по БД. Не рекомендуется делать меньше 10, так как это может очень сильно ударить по производительности БД
        :return: None|dict

        Пауза делается в начале, а не конце цикла для того, чтобы не сделать запрос слишком рано, когда задача, вероятно, наверняка еще не выполнена
        Тем не менее, при паузе больше 5 секунд она делится на две части - 5 секунд в начале цикла и остальное - после
        Это позволит не ждать слишком долго перед первым запросом и, в то же время, подерживать общую длинну паузы на заданном параметром уровне
        """
        sleep_pre_sec = sleep_sec
        sleep_post_sec = 0
        if sleep_sec > 5:
            sleep_pre_sec = 5
            sleep_post_sec = sleep_sec - 5
        max_tries = 10
        current_try = 0
        while True:
            time.sleep(sleep_pre_sec)
            data = {"taskId": task_id}
            url = self.__starter_api_url + '/services/' + service_id + '/tasks/getShortTaskInfo'
            try:
                resp = requests.post(
                    url=url,
                    data=json.dumps(data),
                    headers=self.headers,
                    timeout=15
                )
                """
                Если задача не найдена - возвращать null и правильно его тут обрабатывать!
                """
                if (len(resp.text) > 0):
                    serverResult = json.loads(resp.text)
                    if resp.status_code == 200:
                        self.log.info("Ждем выполнения задачи", {
                            "task_info": serverResult
                        })
                        is_finish = serverResult['status'] != 'NEW' and serverResult['status'] != 'PROCESSING'
                        if callback_fn:
                            # Уведомляем вызывающего
                            callback_fn(serverResult, is_finish)
                        if is_finish:
                            return serverResult
                else:
                    return None
            except Exception as e:
                self.log.warning("Неизвестная ошибка при выполнении await_task, пробуем снова", {"error": e})
                current_try = current_try + 1
                if current_try >= max_tries:
                    self.log.error("Неизвестная ошибка при выполнении await_task, прерываем выполнение", {"error": e})
                    raise IOError("Starter response read error")
            time.sleep(sleep_post_sec)

    def submit(self, service_id: str, data: dict = None):
        """
        Отправить задачу в запускатор

        :param service_id: ID службы. Например "meta.docs_generate"
        :param data: Полезная нагрузка задачи
        :return: dict
        """
        # импорт тут, так как глобально над классом он не работает
        from metasdk import DEV_STARTER_STUB_URL

        if self.__starter_api_url == DEV_STARTER_STUB_URL:
            self.log.info('STARTER DEV. Задача условно поставлена', {
                "service_id": service_id,
                "data": data,
            })
            return

        task = {"serviceId": service_id, "data": data}
        url = self.__starter_api_url + '/services/' + service_id + '/tasks'
        last_e = None
        for _idx in range(self.max_retries):
            try:
                resp = requests.post(
                    url=url,
                    data=json.dumps(task),
                    headers=self.headers,
                    timeout=15
                )
                try:
                    return json.loads(resp.text)
                except Exception:
                    raise IOError("Starter response read error: " + resp.text)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                # При ошибках подключения пытаемся еще раз
                last_e = e
                sleep(3)
        raise last_e

    def stop_task(self, task_id: str, service_id: str) -> str:
        """
        Остановить задачу запускатора.

        :param task_id: ID задачи
        :param service_id: ID службы. Например "meta.datasource_share"
        :return: None
        """
        last_e = None
        url = f"{self.__starter_api_url}/services/{service_id}/tasks/{task_id}"
        for _ in range(self.max_retries):
            try:
                resp = requests.delete(url=url, headers=self.headers, timeout=15)
                if resp.status_code == 200:
                    return task_id
                elif resp.status_code == 400:
                    error = resp.json()
                    raise BadRequestError("Bad Request", {"error": error})
                else:
                    raise UnexpectedError("Непредвиденная ошибка при остановке задачи", {"error": resp.text})
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                last_e = e
                sleep(3)
        raise last_e
