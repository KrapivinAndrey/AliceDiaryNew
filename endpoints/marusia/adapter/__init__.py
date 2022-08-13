import cmd
from typing import Union
import requests
import urllib.parse
import uuid


from ..models import (
    RequestModel,
    ResponseModel,
    ResponseButton,
    ResponsePush,
    ResponseCommandText,
    ResponseCommandWidget,
)


class MarusiaAdapter:
    def __init__(self) -> None:
        self._last_request: Union[RequestModel, None] = None
        self._last_response: Union[ResponseModel, None] = None
        self._auth: "AuthAdapter" = AuthAdapter()

    def event(self, data: RequestModel):

        self._last_request = data

        # auth

        try:
            auth_token = self._auth.get_token(data.session.user_id)
        except Exception as e:
            self._auth.need = True
            self._auth.error = True
            auth_token = None

        if auth_token is None:
            self._auth.need = True
        else:
            self._auth.need = False

        # event

        event = data.dict(exclude_none=True)
        return event

    def response(self, data) -> ResponseModel:
        resp = ResponseModel(session=self._last_request.session)

        # response

        resp.response.text = data["response"]["text"]
        resp.response.tts = data["response"]["tts"]

        if self._auth.need:
            resp.response.text = "Привет"
            resp.response.tts = None
            button = ResponseButton(title="Войти", url="https://mail.ru")
            button2 = ResponseButton(title="Войти2", url="vk.com")
            # resp.response.buttons.append(button)
            # resp.response.buttons.append(button2)

            cmd1 = ResponseCommandWidget(
                layout_name="universal_internal",
                payload={
                    "items": [
                        {
                            "title": {"value": "Я заголовок"},
                            "description": {"value": "Я описание"},
                            "image": {
                                "type": "inline",
                                "items": [
                                    {"image_id": 451939019, "height": 30, "width": 30}
                                ],
                            },
                            "action": {"type": "open_url", "url": "https://vk.com"},
                        },
                        {
                            "title": {"value": "Заголовок2"},
                            "description": {"value": "Описание2"},
                            "image": {
                                "type": "inline",
                                "items": [
                                    {"image_id": 451937223, "height": 40, "width": 40}
                                ],
                            },
                            "action": {"type": "open_url", "url": "https://mail.ru"},
                        },
                    ]
                },
            )
            cmd2 = ResponseCommandText()
            # resp.response.buttons.append(button)
            # resp.response.commands.append(cmd2)
            resp.response.commands.append(cmd1)
        elif self._auth.error:
            button = ResponseButton(title="Все сломалось")
            resp.response.buttons.append(button)
        else:
            buttons_data = data["response"].get("buttons", [])
            for button_data in buttons_data:
                button = ResponseButton(title=button_data["title"])
                resp.response.buttons.append(button)

        # TODO хз от чего он зависит вообще, прямой аналогии у алисы не вижу

        resp.response.end_session = False

        # TODO сессии

        resp.session.new = False

        self._last_response = resp
        return resp

    def user_id(self):
        return self._last_request.session.user_id


class AuthAdapter:
    def __init__(self) -> None:
        self._re = requests.session()
        self._back = "https://functions.yandexcloud.net/d4er5fg80dbecq63tf12"
        self._front = "https://dnevnik2.petersburgedu.ru/api/journal/user/yandex-login"
        self.need = False
        self.error = False

    def get_token(self, user_id):
        resp = self._re.get(
            f"{self._back}",
            params={"state": user_id},
            headers={"X-Method": "get-jwt"},
        )
        if resp.status_code == 200:
            return resp.text
        elif resp.status_code == 404:
            return None
        else:
            resp.raise_for_status()

    def build_login_uri(self, user_id):
        args = {
            "scope": "read",
            "state": user_id,
            "redirect_uri": self._back,
            "response_type": "code",
            "client_id": str(uuid.uuid4()),
        }
        args_string = urllib.parse.urlencode(args)
        return f"{self._front}?{args_string}"
