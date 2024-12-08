import json
from datetime import datetime

import requests

LOGIN_PATH = r"{}/_matrix/client/v3/login"

LOGIN_JSON = r"""{{
    "password": "{}",
    "identifier": {{
        "type": "m.id.thirdparty",
        "medium": "email",
        "address": "{}"
    }},
    "initial_device_display_name": "{}/riot.im: Chrome на Windows",
    "type": "m.login.password"
}}"""

JSON_MESSAGE = r"""{{
    "msgtype": "m.text",
    "body": "{}",
    "m.mentions": {{}}
}}"""

MESSAGE_LINK = r"{}/_matrix/client/v3/rooms/{}%3Aim.magnit.ru/send/m.room.message/m{}"

LOGOUT_LINK = r"{}/_matrix/client/v3/logout"

class Element:
    """
    Send messages to Element ex. riot

    Made for v3 Element API
    """
    auth_header: dict
    def __init__(self, messanger_path: str, email: str | None = None, password: str | None = None,
                 token: str | None = None) -> None:
        """
        To login you need to provide email and password OR token

        :param messanger_path: hostname of your element
        :param email: email for login
        :param password: password for login
        :param token: token that is given after authentication
        """
        self.__check_credentials(email, password, token)

        self.__email = email
        self.__password = password
        self.__token = token
        self.__messanger_path = messanger_path

        self.__register_token(token)

    def __register_token(self, token: None | str):
        """
        Register token in class and adds it to header that should be used for requests
        :param token: token that is given after authentication
        :return:
        """
        if token is None:
            login_path = LOGIN_PATH.format(self.__messanger_path)
            login_json = json.loads(LOGIN_JSON.format(self.__password, self.__email, self.__messanger_path))
            login_request = requests.post(login_path, json=login_json)
            if login_request.status_code == 200:
                self.__token = login_request.json().get("access_token")

        self.auth_header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.__token)
        }

    def get_token(self) -> str:
        """
        Returns token
        :return:  token string
        """
        return self.__token

    @staticmethod
    def __check_credentials(email: str | None, password: str | None, token: str | None) -> None:
        """
        Checks that username and password OR token is presented
        :param email: email for login
        :param password: password for login
        :param token: token that is given after authentication

        :raises RuntimeError: if username and password OR token is NOT presented

        :return: None
        """
        if (token is None) and ((email is None) or (password is None)):
            raise RuntimeError("Должны быть заполнены логин и пароль или токен")

    def send_message(self, room_name: str, message: str) -> None:
        """
        Send message
        :param room_name: room name of message receiver
        :param message: message that should be sent

        :raises Runtime error: if status code is not 200

        :return: None
        """
        current_time = round(datetime.timestamp(datetime.now()), 2)

        message_url: str = MESSAGE_LINK.format(self.__messanger_path, room_name, current_time)

        json_message = json.loads(JSON_MESSAGE.format(message))

        answer = requests.put(message_url, headers=self.auth_header, json=json_message)

        if answer.status_code != 200:
            raise RuntimeError(answer.json().get("error"))

    def logout(self) -> None:
        """
        Log out from Element
        :return: None
        """
        logout_url = LOGOUT_LINK.format(self.__messanger_path)
        requests.post(logout_url, headers=self.auth_header)
