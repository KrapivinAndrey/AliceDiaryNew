import urllib.parse
import uuid
import pymorphy2
from typing import Union

import requests
import xmltodict

from skill.constants import entities as skill_entities
from skill.constants import intents as skill_intents
from skill.dairy_api import NeedAuth, get_permissions
from skill.main import app_context
from skill.scenes import DAYS, DAYS_RU

from ..models import request_model, response_model
from . import request_parser, response_parser


class MarusiaAdapter:
    def __init__(self) -> None:
        self._last_request: Union[request_model.Model, None] = None
        self._last_response: Union[response_model.Model, None] = None
        self._auth: "AuthAdapter" = AuthAdapter()

    # public

    @app_context.perfmon
    def parse_request(self, request: request_model.Model) -> dict:

        self._last_request = request
        self._set_auth_token(request)

        # event

        result = request_parser.parse(request)

        self._set_intents(result)
        self._set_entities(result)

        return result

    @app_context.perfmon
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

    # auth_service

    @app_context.perfmon
    def refresh_token(self):
        """
        Реактивное обновление токена
        """
        # TODO можно поставить галочку и принудительно толкнуть новый токен в стейт
        # т.к. скил этого не сделает, скорее всего
        user_thumbprint = self._user_thumbprint(self._last_request)
        return self._auth.get_token(user_thumbprint)

    # internal

    def _set_intents(self, event: dict) -> None:
        self._set_day_of_weak(event)

        # TODO устарело, удалить

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
        self._set_relative_date(event)
        self._set_fio(event)

    def _set_relative_date(self, event: dict) -> None:
        date_index = self._get_relative_date_from_tokens(event)
        if date_index:
            event["request"]["nlu"].setdefault("entities", [])
            event["request"]["nlu"]["entities"].append(
                {
                    "type": "YANDEX.DATETIME",
                    "tokens": {"start": 0, "end": 0},
                    "value": {"day": date_index, "day_is_relative": True},
                }
            )

    def _get_relative_date_from_tokens(self, event: dict) -> None:
        request = self._last_request.request
        rel_day = list(
            set(list(skill_entities.relative_dates.keys())) & set(request.nlu.tokens)
        )
        if rel_day:
            return skill_entities.relative_dates[rel_day[0]]
        return None

    def _set_day_of_weak(self, event: dict) -> None:
        days_of_weak = self._get_dys_of_weak_from_tokens(self._last_request)
        if days_of_weak:
            event["request"]["nlu"].setdefault("intents", {})
            event["request"]["nlu"]["intents"].setdefault(
                "day_of_week",
                {
                    "slots": {
                        "Day": {
                            "type": "DayOfWeek",
                            "tokens": {"start": 0, "end": 0},
                            "value": days_of_weak,
                        }
                    }
                },
            )

    def _get_dys_of_weak_from_tokens(self, event: dict) -> None:
        request = self._last_request.request
        days_of_weak = list(set(DAYS_RU) & set(request.nlu.tokens))
        if len(days_of_weak) > 0:
            day = days_of_weak[0]
            index_date = DAYS_RU.index(day)
            days_en = DAYS[index_date]
            return days_en
        return None

    def _set_fio(self, event):
        morph = pymorphy2.MorphAnalyzer()
        list_word = event['request']['nlu']['tokens']
        name = ''
        patronymic = ''
        last_name = ''
        for word in list_word:
            parse_word = morph.parse(word)[0]
            if 'Name' in parse_word.tag:
                name = parse_word[2]
            if 'Patr' in parse_word.tag:
                patronymic = parse_word[2]
            if 'Surn' in parse_word.tag:
                last_name = parse_word[2]
        if name != '' or last_name != '':
            value = {
                        "type": 'FIO',
                        "first_name": {name},
                        "patronymic_name": {patronymic},
                        "last_name": {last_name}
                    }
            self._add_intents(event, value)

    def _add_intents(self, event, value):
        event["request"]["nlu"].setdefault("entities", {})
        event["request"]["nlu"]["entities"].append(value)

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
        auth_token = None
        # from state
        if request.state.user.auth_token:
            auth_token = request.state.user.auth_token
        # Проактивное обновление токена
        # TODO включить, чтобы обновлять токен проактивно
        always_check = False
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
