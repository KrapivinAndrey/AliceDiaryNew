import datetime
import inspect
import sys
from typing import List, Union

import skill.dairy_api as dairy_api
import skill.texts as texts
from skill.alice import Request, big_image, button
from skill.constants import entities, intents, states
from skill.constants.exceptions import NeedAuth
from skill.constants.images import CONFUSED, GOODBYE
from skill.dataclasses import Students
from skill.loggerfactory import LoggerFactory
from skill.scenes_util import Scene
from skill.tools.dates_transformations import (
    transform_yandex_datetime_value_to_datetime as ya_date_transform,
)

from . import gr

logger = LoggerFactory.get_logger(__name__, log_level="DEBUG")
# region Выделение данных для запроса


def get_all_students_from_request(request: Request) -> Students:
    dump = request.user[states.STUDENTS]
    students = Students()
    if dump is not None:
        students.restore(dump)

    return students


def get_date_from_request(request: Request) -> datetime.date:
    if entities.DATETIME in request.entities_list:
        ya_date = request.entity(entities.DATETIME)[0].value
        ya_date = ya_date_transform(ya_date)
    elif intents.DAY in request.intents:
        day = request.slot(intents.DAY, "Day")
        delta = DAYS.index(day) - datetime.date.today().weekday()
        if delta < 0:
            delta += 7
        ya_date = datetime.datetime.today() + datetime.timedelta(days=delta)
    else:
        ya_date = None

    if ya_date is None and not request.entities_list:
        ya_date = date_from_tokens(request)

    return ya_date


def date_from_tokens(request: Request):
    ya_date = None
    rel_day = list(set(list(entities.relative_dates.keys())) & set(request.tokens))
    if rel_day:
        ya_date = datetime.datetime.today() + datetime.timedelta(
            days=entities.relative_dates[rel_day[0]]
        )

    if ya_date is None:
        days_of_weak = list(set(DAYS_RU) & set(request.tokens))
        if len(days_of_weak) > 0:
            day = days_of_weak[0]
            delta = DAYS_RU.index(day) - datetime.date.today().weekday()
            if delta < 0:
                delta += 7
            ya_date = datetime.datetime.today() + datetime.timedelta(days=delta)

    return ya_date


def get_time_from_request(request: Request) -> Union[None, datetime.time]:
    if entities.DATETIME in request.entities_list:
        ya_date = request.entity(entities.DATETIME)[0].value
        ya_date = ya_date_transform(ya_date)
    elif intents.DAY in request.intents:
        day = request.slot(intents.DAY, "Day")
        delta = DAYS.index(day) - datetime.date.today().weekday()
        if delta < 0:
            delta += 7
        ya_date = datetime.datetime.today() + datetime.timedelta(days=delta)
    else:
        return None

    return ya_date.time()


def get_students_from_request(
    request: Request, students: Students
) -> Union[List, None]:
    result = []
    if entities.FIO in request.entities_list:
        for fio in request.entity(entities.FIO):
            if fio.value["first_name"] == "алиса" and fio.start == 0:
                # Кто-то начал команду словами Алиса...
                continue
            found = students.by_name(fio.value["first_name"])
            if found is None:
                return None
            result.append(found)
    else:
        result = students.to_list()

    return result


def get_token(request: Request):
    return request.access_token
    # else request.user.get(states.AUTH_TOKEN):


# endregion

# region Общие сцены


def global_scene_from_request(request: Request):
    if len(intersection_list(intents.help_word_list, request.tokens)) > 0:
        next_scene = HelpMenuStart
    elif isIntentWhatCanYouDo(request.tokens):
        next_scene = WhatCanDo
    elif len(list(set(intents.clear_settings_word_list) & set(request.tokens))) > 0:
        next_scene = ClearSettings
    elif isIntentRepeat(request.tokens):
        next_scene = Repeat
    elif len(intersection_list(intents.exit_word_list, request.tokens)) > 0:
        next_scene = Goodbye
    # Глобальные команды
    elif len(intersection_list(intents.get_schedule_word_list, request.tokens)) > 0:
        next_scene = GetSchedule  # type: ignore
    elif len(intersection_list(intents.main_menu_word_list, request.tokens)) > 0:
        next_scene = Welcome  # type: ignore
    elif intents.LESSON_BY_NUM in request.intents:
        next_scene = LessonByNum  # type: ignore
    elif isIntentLessonByDate(request.tokens):
        next_scene = LessonByDate  # type: ignore
    elif isIntentMakrs(request.tokens):
        next_scene = Marks  # type: ignore
    else:
        next_scene = None

    return next_scene


def intersection_list(list1, list2):
    return list(set(list1) & set(list2))


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def handle_global_intents(self, request):
        # Должны быть обработаны в первую очередь
        scene = global_scene_from_request(request)
        if scene is not None:
            return scene()

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
    def __init__(self, students=None, saved_entities=None, saved_intents=None):
        self.students = students
        self.entities = saved_entities if saved_entities is not None else {}
        self.intents = saved_intents if saved_intents is not None else {}

    def reply(self, request: Request):
        save_states = {}
        auth = False
        if get_token(request) is None:
            # Нет вообще токена
            save_states = {
                states.ENTITIES: request.entities,
                states.INTENTS: request.intents,
            }
            auth = True
        elif request.authorization_complete:
            # Завершение авторизации
            try:
                self.students = dairy_api.get_students(request.access_token)
                request.restore_entities(request.session.get(states.ENTITIES, {}))
                request.restore_intents(request.session.get(states.INTENTS, {}))
            except NeedAuth as e:
                logger.warning("Failed to get students %s", e)
                auth = True
                save_states = {
                    states.ENTITIES: request.session.get(states.ENTITIES, {}),
                    states.INTENTS: request.session.get(states.INTENTS, {}),
                }
        else:
            try:
                self.students = get_all_students_from_request(request)
            except Exception as e:
                logger.warning("Old format for students %s", e)
                self.students = dairy_api.get_students(get_token(request))
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
                state=save_states,
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

        token = get_token(request)
        req_date = datetime.datetime.today()
        text = []
        tts = []

        title_text, title_tts = texts.welcome_start()
        text.append(title_text)
        tts.append(title_tts)

        for student in students.to_list():
            try:
                journal = dairy_api.get_marks(token, student.id, req_date)
            except NeedAuth:
                token = dairy_api.refresh_token(token)
                journal = dairy_api.get_marks(token, student.id, req_date)
            if journal.len:
                new_text, new_tts = texts.marks_for_student(student, journal)
            else:
                new_text, new_tts = texts.no_marks(student)
            text.append(new_text)
            tts.append(new_tts)

        buttons = [button("Расписание уроков"), button("Уроки завтра")]

        finish_text, finish_tts = texts.welcome_end()
        text.append(finish_text)
        tts.append(finish_tts)

        return self.make_response(
            request,
            "\n".join(text),
            "sil<[500]>".join(tts),
            buttons=buttons,
            user_state={states.STUDENTS: students.dump(), states.AUTH_TOKEN: token},
        )

    def handle_local_intents(self, request: Request):
        if request.is_intent(intents.CONFIRM):
            return GetSchedule()


class Goodbye(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.goodbye()
        return self.make_response(
            request,
            "",
            tts=tts,
            card=big_image(GOODBYE, description=text),
            end_session=True,
        )


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
            return HelpMenuMarks()
        if request.is_intent(intents.REJECT):
            return Welcome()


class HelpMenuMarks(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.help_menu_marks()
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
                request,
                "",
                tts=tts,
                card=big_image(CONFUSED, description=text),
                buttons=HELP,
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

        if self.students is None:
            students = Students()
            students.restore(request.user[states.STUDENTS])
        else:
            students = self.students
        req_students = get_students_from_request(request, students)

        if req_students is None:  # нет данных для запроса. Возможно не то имя
            text, tts = texts.unknown_student()
            return self.make_response(
                request, text, tts, state={states.NEED_FALLBACK: True}
            )

        token = get_token(request)
        req_date = get_date_from_request(request)
        text = []
        tts = []

        title_text, title_tts = texts.schedule_title(req_date)
        text.append(title_text)
        tts.append(title_tts)

        for student in req_students:
            try:
                schedule = dairy_api.get_schedule(token, student.id, req_date)
            except NeedAuth:
                token = dairy_api.refresh_token(token)
                schedule = dairy_api.get_schedule(token, student.id, req_date)

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
                states.AUTH_TOKEN: token,
            },
            state={states.SAVE_TEXT: result_text, states.SAVE_TTS: result_tts},
        )


class LessonByNum(SceneWithAuth):
    def reply(self, request: Request):
        auth = super().reply(request)
        if auth is not None:
            return auth

        num = request.entity(entities.NUMBER)

        if not num:
            # Странная ситуация. В запросе не пришел номер урока...
            # Тогда вернем целиком расписание
            return GetSchedule().reply(request)

        if self.students is None:
            students = Students()
            students.restore(request.user[states.STUDENTS])
        else:
            students = self.students
        req_students = get_students_from_request(request, students)

        if req_students is None:  # нет данных для запроса. Возможно не то имя
            text, tts = texts.unknown_student()
            return self.make_response(
                request, text, tts, state={states.NEED_FALLBACK: True}
            )

        number = num[0].value

        token = get_token(request)
        req_date = get_date_from_request(request)
        text = []
        tts = []

        title_text, title_tts = texts.lesson_num_title(number, req_date)
        text.append(title_text)
        tts.append(title_tts)

        for student in req_students:
            try:
                schedule = dairy_api.get_schedule(
                    get_token(request), student.id, req_date
                )
            except NeedAuth:
                token = dairy_api.refresh_token(token)
                schedule = dairy_api.get_schedule(
                    get_token(request), student.id, req_date
                )
            lesson = schedule.find_by_num(number)
            if lesson is None:
                new_text, new_tts = texts.no_lesson(student, number)
                text.append(new_text)
                tts.append(new_tts)
            else:
                new_text, new_tts = texts.num_lesson(student, lesson)
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
                states.AUTH_TOKEN: token,
            },
            state={states.SAVE_TEXT: result_text, states.SAVE_TTS: result_tts},
        )


class LessonByDate(SceneWithAuth):
    def reply(self, request: Request):
        auth = super().reply(request)
        if auth is not None:
            return auth


# endregion

# region Оценки


class Marks(SceneWithAuth):
    def reply(self, request: Request):
        auth = super().reply(request)
        if auth is not None:
            return auth

        if self.students is None:
            students = Students()
            students.restore(request.user[states.STUDENTS])
        else:
            students = self.students
        req_students = get_students_from_request(request, students)

        if req_students is None:  # нет данных для запроса. Возможно не то имя
            text, tts = texts.unknown_student()
            return self.make_response(
                request, text, tts, state={states.NEED_FALLBACK: True}
            )

        token = get_token(request)
        req_date = get_date_from_request(request)
        text = []
        tts = []

        title_text, title_tts = texts.journal_title(req_date)
        text.append(title_text)
        tts.append(title_tts)

        for student in req_students:
            try:

                journal = dairy_api.get_marks(token, student.id, req_date)

            except NeedAuth:
                token = dairy_api.refresh_token(token)
                journal = dairy_api.get_marks(token, student.id, req_date)

            if journal.len:
                new_text, new_tts = texts.marks_for_student(student, journal)
            else:
                new_text, new_tts = texts.no_marks(student)
            text.append(new_text)
            tts.append(new_tts)

        return self.make_response(
            request,
            "\n".join(text),
            "sil<[500]>".join(tts),
            user_state={
                states.STUDENTS: students.dump(),
                states.AUTH_TOKEN: token,
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


def listIntersection(List2, List1):
    result = []
    for i in List2:
        if i in result:
            continue
        for j in List1:
            if isinstance(j, list) and wordInList(i, j):
                result.append(i)
                break
            if i == j:
                result.append(i)
                break
    return result


def wordInList(word, List):
    for line in List:
        if type(line) == list:
            return wordInList(word, line)
        elif line.lower() == word.lower():
            return True
    return False


# region listKey


def listKeyLessonByDate():
    return [
        ["уроки", "предметы", "занятия"],
        ["вчера", "сегодня", "завтра", "послезавтра"],
        [
            "понедельник",
            "вторник",
            "среду",
            "четверг",
            "пятницу",
        ],
    ]


def listKeyLessonRepeat():
    return ["повтори"]


def listKeyLessonMarks():
    return ["оценки"]


# endregion


def isIntentHelp(intentList):
    helpIntentList_ = gr.help()
    result = len(listIntersection(intentList, helpIntentList_)) > (
        len(helpIntentList_) - 1
    )
    return result


def isIntentWhatCanYouDo(intentList):
    whatCanYouDoIntentList_ = gr.whatCanYouDo()
    result = len(listIntersection(intentList, whatCanYouDoIntentList_)) > (
        len(whatCanYouDoIntentList_) - 1
    )
    return result


def isIntentClean(intentList):
    IntentCleanList = gr.reset_settings()
    result = len(listIntersection(intentList, IntentCleanList)) > (
        len(IntentCleanList) - 1
    )
    return result


def isIntentLessonByDate(intentList):
    ListKey = listKeyLessonByDate()
    result = len(listIntersection(intentList, ListKey)) > (len(ListKey) - 1)
    return result


def isIntentRepeat(intentList):
    ListKey = listKeyLessonRepeat()
    result = len(listIntersection(intentList, ListKey)) > (len(ListKey) - 1)
    return result


def isIntentMakrs(intentList):
    ListKey = listKeyLessonMarks()
    result = len(listIntersection(intentList, ListKey)) > (len(ListKey) - 1)
    return result


SCENES = {scene.id(): scene for scene in _list_scenes()}
DEFAULT_SCENE = Welcome
YES_NO = [button("Да"), button("Нет")]
HELP = [button("Помощь")]
DEFAULT_BUTTONS = [
    button("Расписание на завтра"),
    button("Главное меню"),
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_RU = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]
