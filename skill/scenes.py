import inspect
import sys

from skill.alice import Request, button, image_button, image_list
from skill.constants import entities, intents, states
from skill.scenes_util import Scene

# region Общие сцены

# класс общая сцена


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def handle_global_intents(self, request):

        # Должны быть обработаны в первую очередь
        if intents.HELP in request.intents:
            return HelpMenu()
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
            text = tts = "Пытаюсь понять но не получается"
            return self.make_response(request, text, tts, end_session=True)
        else:
            save_state = {}
            # Сохраним важные состояние
            for save in states.MUST_BE_SAVE:
                if save in request.session:
                    save_state.update({save: request.session[save]})
            save_state[states.NEED_FALLBACK] = True
            text = tts = "Не могу понять"
            return self.make_response(
                request,
                text,
                tts,
                buttons=HELP,
                state=save_state,
            )


class Welcome(GlobalScene):
    def reply(self, request: Request):
        text = tts = "Привет"
        buttons = [
            button("Что ты умеешь?"),
        ]

        return self.make_response(
            request,
            text,
            tts,
            buttons=buttons,
            user_state=None,
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


class WhatCanDo(GlobalScene):
    def reply(self, request: Request):
        return self.make_response(
            request,
            "Что я умею",
            "Что я умею",
            buttons=YES_NO,
            state={},
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return HelpMenu()
        if intents.REJECT in request.intents:
            return Welcome()


class HelpMenu(GlobalScene):
    def reply(self, request: Request):
        return self.make_response(request, "Помощь", "Помощь", buttons=YES_NO)

    def handle_local_intents(self, request: Request):
        pass


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
