import inspect
import logging
import sys

import skill.dairy_api as dairy_api
import skill.texts as texts
from skill.alice import Request, button, image_button, image_list
from skill.constants import entities, intents, states
from skill.constants.exceptions import NeedAuth
from skill.dataclasses.students import Students
from skill.scenes_util import Scene

logging.basicConfig()

logging.getLogger().setLevel(logging.DEBUG)
root_handler = logging.getLogger().handlers[0]
root_handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(name)s\t%(message)s\n"))

# region Декоратор: проверить что надо авторизоваться


def get_all_students_from_request(request: Request) -> Students:
    dump = request.user[states.STUDENTS]
    if dump is None:
        return []
    else:
        students = Students()
        students.restore(dump)

    return students


# endregion

# region Общие сцены


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def handle_global_intents(self, request):

        # Должны быть обработаны в первую очередь
        if intents.HELP in request.intents:
            return HelpMenuStart()
        if intents.WHAT_CAN_YOU_DO in request.intents:
            return WhatCanDo()
        if intents.CLEAN in request.intents:
            return ClearSettings()

        # Глобальные команды
        if intents.GET_SCHEDULE in request.intents:
            pass
        if intents.MAIN_MENU in request.intents:
            pass

    def handle_local_intents(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def fallback(self, request: Request):
        if request.session.get(states.NEED_FALLBACK, False):
            text, tts = texts.sorry_and_goodbye()
            return self.make_response(request, text, tts, end_session=True)
        else:
            save_state = {}
            # Сохраним важные состояние
            for save in states.MUST_BE_SAVE:
                if save in request.session:
                    save_state.update({save: request.session[save]})
            save_state[states.NEED_FALLBACK] = True
            text, tts = texts.fallback()
            return self.make_response(
                request,
                text,
                tts,
                buttons=HELP,
                state=save_state,
            )


class SceneWithAuth(GlobalScene):
    def __init__(self, students=None, context=None):
        self.students = students
        self.context = context

    def reply(self, request: Request):
        auth = False
        if request.access_token is None:
            # TODO: Сохранить контекст для повторного вызова
            auth = True
        elif request.authorization_complete:
            try:
                self.students = dairy_api.get_students(request.access_token)
            except NeedAuth as e:
                auth = True
        else:
            try:
                self.students = get_all_students_from_request(request)
            except Exception as e:
                logging.warning("Old format for students %s", e)
                self.students = dairy_api.get_students(request.access_token)
        if auth:
            logging.info("Need authentication for %s", self.id())
            text, tts = texts.need_auth(self.id())
            buttons = [
                button("Что ты умеешь?"),
            ]
            return self.make_response(
                request,
                text,
                tts,
                buttons=buttons,
                directives={"start_account_linking": {}},
                user_state=None,
            )


class Welcome(SceneWithAuth):
    def reply(self, request: Request):
        auth = super().reply(request)
        if auth is not None:
            return auth

        text, tts = texts.hello(None)
        buttons = [
            button("Что ты умеешь?"),
        ]

        return self.make_response(
            request,
            text,
            tts,
            buttons=buttons,
            user_state={states.STUDENTS: self.students.dump()},
        )

    def handle_local_intents(self, request: Request):
        pass


class Goodbye(GlobalScene):
    def reply(self, request: Request):
        text = tts = "До свидания"
        return self.make_response(request, text, tts, end_session=True)


class HaveMistake(GlobalScene):
    def reply(self, request: Request):
        text = tts = "Ошибка"
        return self.make_response(request, text, tts, end_session=True)


# endregion

# region Помощь


class HelpMenuStart(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.help_menu_start()
        return self.make_response(request, text, tts, buttons=YES_NO)

    def handle_local_intents(self, request: Request):
        if request.is_intent(intents.CONFIRM):
            return HelpMenuSpec()
        if request.is_intent(intents.REJECT):
            return Welcome()


class HelpMenuSpec(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.help_menu_spec()
        return self.make_response(request, text, tts, buttons=DEFAULT_BUTTONS)

    def handle_local_intents(self, request: Request):
        pass


class WhatCanDo(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.what_can_i_do()
        return self.make_response(
            request,
            text,
            tts,
            buttons=YES_NO,
            state={},
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return HelpMenuStart()
        if intents.REJECT in request.intents:
            return Welcome()


# endregion


class ClearSettings(GlobalScene):
    def reply(self, request: Request):

        return self.make_response(
            request,
            "Сброс",
            "Сброс",
            state={},
            user_state={x: None for x in request.user.keys()},
            end_session=True,
        )


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)

    scenes.remove(GlobalScene)
    scenes.remove(Scene)
    return scenes


SCENES = {scene.id(): scene for scene in _list_scenes()}

DEFAULT_SCENE = Welcome
YES_NO = [button("Да"), button("Нет")]
HELP = [button("Помощь")]
DEFAULT_BUTTONS = [
    button("Расписание на завтра"),
    button("Главное меню"),
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
