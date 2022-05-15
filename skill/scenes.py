import datetime
import inspect
import sys

import skill.dairy_api as dairy_api
import skill.texts as texts
from skill.alice import Request, big_image, button
from skill.constants import entities, intents, states
from skill.constants.exceptions import NeedAuth
from skill.constants.images import CONFUSED
from skill.dataclasses.students import Students
from skill.loggerfactory import LoggerFactory
from skill.scenes_util import Scene
from skill.tools.dates_transformations import (
    transform_yandex_datetime_value_to_datetime as ya_date_transform,
)

logger = LoggerFactory.get_logger(__name__, log_level="DEBUG")
# region Выделение данных для запроса


def get_all_students_from_request(request: Request) -> Students:
    dump = request.user[states.STUDENTS]
    students = Students()
    if dump is not None:
        students.restore(dump)

    return students


def get_date_from_request(request: Request):
    if entities.DATETIME in request.entities_list:
        ya_date = request.entity(entities.DATETIME)[0]
        ya_date = ya_date_transform(ya_date)
    elif intents.DAY in request.intents:
        day = request.slot(intents.DAY, "Day")
        delta = DAYS.index(day) - datetime.date.today().weekday()
        if delta < 0:
            delta += 7
        ya_date = datetime.datetime.today() + datetime.timedelta(days=delta)
    else:
        ya_date = None

    return ya_date


def get_students_from_request(request: Request, students: Students):
    result = []
    if entities.FIO in request.entities_list:
        for fio in request.entity(entities.FIO):
            found = students.by_name(fio["first_name"])
            if found is None:
                return None
            result.append(found)
    else:
        result = students.to_list()

    return result


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
        if intents.REPEAT in request.intents:
            return Repeat()

        # Глобальные команды
        if intents.GET_SCHEDULE in request.intents:
            return GetSchedule()
        if intents.MAIN_MENU in request.intents:
            Welcome()

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
    def __init__(self, students=None, saved_entities={}, saved_intents={}):
        self.students = students
        self.entities = saved_entities
        self.intents = saved_intents

    def reply(self, request: Request):
        auth = False
        if request.access_token is None:
            save_entities = {
                states.ENTITIES: request.entities,
                states.INTENTS: request.intents,
            }
            auth = True
        elif request.authorization_complete:
            try:
                self.students = dairy_api.get_students(request.access_token)
                request.restore_entities(request.session.get(states.ENTITIES, {}))
                request.restore_intents(request.session.get(states.INTENTS, {}))
            except NeedAuth as e:
                auth = True
                save_entities = {
                    states.ENTITIES: request.session.get(states.ENTITIES, {}),
                    states.INTENTS: request.session.get(states.INTENTS, {}),
                }
        else:
            try:
                self.students = get_all_students_from_request(request)
            except Exception as e:
                logger.warning("Old format for students %s", e)
                self.students = dairy_api.get_students(request.access_token)
        if auth:
            logger.info("Need authentication for %s", self.id())
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
                state=save_entities,
                user_state=None,
            )


class Welcome(SceneWithAuth):
    def reply(self, request: Request):
        auth = super().reply(request)
        if auth is not None:
            return auth

        students = Students()
        if self.students is None:
            students.restore(request.user[states.STUDENTS])
        else:
            students = self.students
        req_date = datetime.datetime.today()
        text = []
        tts = []

        title_text, title_tts = texts.title("Расписание", req_date)
        text.append(title_text)
        tts.append(title_tts)

        for student in students.to_list():
            schedule = dairy_api.get_schedule(
                request.access_token, student.id, req_date
            )
            new_text, new_tts = texts.schedule_for_student(student, schedule)
            text.append(new_text)
            tts.append(new_tts)

        return self.make_response(
            request,
            "\n".join(text),
            "sil<[500]>".join(tts),
            user_state={states.STUDENTS: students.dump()},
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

# region Повтори


class Repeat(GlobalScene):
    def reply(self, request: Request):
        text = request.session.get(states.SAVE_TEXT)
        tts = request.session.get(states.SAVE_TTS, text)

        if text is None:
            text, tts = texts.nothing_to_repeat()
            return self.make_response(
                request, tts, card=big_image(CONFUSED, description=text), buttons=HELP
            )
        else:
            return self.make_response(request, text, tts, buttons=DEFAULT_BUTTONS)


# endregion

# region Расписание


class GetSchedule(SceneWithAuth):
    def reply(self, request: Request):
        auth = super().reply(request)
        if auth is not None:
            return auth

        req_date = get_date_from_request(request)
        students = Students()
        if self.students is None:
            students.restore(request.user[states.STUDENTS])
        else:
            students = self.students
        req_students = get_students_from_request(request, students)

        if req_students is None:  # нет данных для запроса. Возможно не то имя
            text, tts = texts.unknown_student()
            return self.make_response(
                request, text, tts, state={states.NEED_FALLBACK: True}
            )
        text = []
        tts = []

        title_text, title_tts = texts.title("Расписание", req_date)
        text.append(title_text)
        tts.append(title_tts)

        for student in req_students:
            schedule = dairy_api.get_schedule(
                request.access_token, student.id, req_date
            )
            new_text, new_tts = texts.schedule_for_student(student, schedule)
            text.append(new_text)
            tts.append(new_tts)

        result_text = "\n".join(text)
        result_tts = "sil<[500]>".join(tts)
        return self.make_response(
            request,
            result_text,
            result_tts,
            user_state={
                states.STUDENTS: students.dump(),
                states.SAVE_TEXT: result_text,
                states.SAVE_TTS: result_tts,
            },
        )


# endregion

# region Отладка


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


# endregion


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
