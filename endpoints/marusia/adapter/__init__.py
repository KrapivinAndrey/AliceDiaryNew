import urllib.parse
import uuid
from typing import Union

import requests
import xmltodict

from skill.constants import intents as skill_intents
from skill.dairy_api import NeedAuth, get_permissions

from ..models import request_model, response_model
from . import request_parser, response_parser


class MarusiaAdapter:
    def __init__(self) -> None:
        self._last_request: Union[request_model.Model, None] = None
        self._last_response: Union[response_model.Model, None] = None
        self._auth: "AuthAdapter" = AuthAdapter()

    # public

    def parse_request(self, request: request_model.Model) -> dict:

        self._last_request = request
        self._set_auth_token(request)

        # event

        result = request_parser.parse(request)

        self._set_intents(result)
        self._set_entities(result)

        return result

    def parse_response(self, data) -> response_model.Model:

        # response

        if self._auth.need:
            resp = self._auth_dialog()
        elif self._auth.error:
            resp = self._auth_dialog_error()
        else:
            resp = response_parser.parse(data)

        ssml = self._ssml_from_tts(resp.response.tts)
        if ssml:
            resp.response.tts_type = "ssml"
            resp.response.tts = None
            resp.response.ssml = ssml

        # session

        resp.session = response_model.Session(
            session_id=self._last_request.session.session_id,
            message_id=self._last_request.session.message_id,
            user_id=self._last_request.session.user_id,
        )

        self._last_response = resp
        return resp

    # internal

    def _set_intents(self, event: dict) -> None:

        # TODO тут нужно дохера написать, нужен отдельный класс

        # GET_SCHEDULE = "get_schedule"
        # GET_HOMEWORK = "get_homework"
        # LESSON_BY_NUM = "what_lesson_num"
        # LESSON_BY_DATE = "what_lesson_time"
        # MARKS = "get_journal"
        # CLEAN = "reset_settings"
        # MAIN_MENU = "main_menu"
        # EXIT = "exit"
        # DAY = "day_of_week"

        intents = {}
        request = self._last_request.request
        if request.command.lower() == "расписание уроков":
            intents.setdefault(skill_intents.GET_SCHEDULE, {})
        if request.command.lower() == "помощь":
            intents.setdefault(skill_intents.HELP, {})
        if request.command.lower() == "уроки завтра":
            # TODO тут наверно надо что-то в контент накидать
            intents.setdefault(skill_intents.GET_HOMEWORK, {})

        if len(intents):
            event["request"].setdefault("nlu", {})
            event["request"]["nlu"].setdefault("intents", intents)

    def _set_entities(self, event: dict) -> None:
        pass

    def _set_auth_token(self, request: request_model.Model):

        auth_token, error = self._refresh_token(request)
        self._auth.need = error is True or auth_token is None
        self._auth.error = error is True

        request.state.user.auth_token = auth_token

    def _ssml_from_tts(self, tts: str) -> str:

        if not tts:
            return ""

        # sil <[500]> -> <break time="500ms"/>

        text = tts.replace("sil<[", '<break time="').replace("]>", '"/>')
        text = text.replace("<speaker audio='alice-sounds-game-loss-3.opus'>", "")
        text = text.replace('<speaker audio="alice-sounds-human-crowd-2.opus">', "")
        ssml = f'<?xml version ="1.0" encoding="UTF-8"?><speak>{text}</speak>'
        try:
            xmltodict.parse(ssml)
        except:
            # TODO лог
            return ""

        return ssml

    def _user_thumbprint(self, request):
        if request.session.user:
            # отпечаток авторизованного юзера
            user_thumbprint = request.session.user.user_id
        else:
            # отпечаток анонима
            user_thumbprint = request.session.application.application_id
        return user_thumbprint

    def _refresh_token(self, request: request_model.Model):
        error = False
        user_thumbprint = self._user_thumbprint(request)
        # from state
        if request.state.user.auth_token:
            auth_token = request.state.user.auth_token
        # check
        always_check = True
        if auth_token and always_check:
            try:
                get_permissions(auth_token)
            except NeedAuth:
                auth_token = None
            except:
                error = True
                auth_token = None
        # refresh
        if not auth_token:
            try:
                auth_token = self._auth.get_token(user_thumbprint)
            except:
                error = True
                auth_token = None

        return auth_token, error

    def _auth_dialog(self) -> response_model.Model:
        response = response_model.Response()
        response.text = "Привет, нажмите на кнопку чтобы войти в дневник"
        user_thumbprint = self._user_thumbprint(self._last_request)
        button = response_model.Button(
            title="Войти", url=self._auth.build_login_uri(user_thumbprint)
        )
        response.buttons.append(button)
        return response_model.Model(response=response)

    def _auth_dialog_error(self):
        response = response_model.Response()
        response.text = "Все сломалось, ничего не сделать"
        return response_model.Model(response=response)


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
