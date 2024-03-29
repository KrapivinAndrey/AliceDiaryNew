import datetime
from typing import Dict, List

from .constants import texts as text_constants
from .dataclasses import Journal, PlannedLesson, Schedule, Student

# region Общие сцены


def mistake():
    text = (
        "Прошу прощения, в навыке возникла непредвиденная ошибка.\n"
        "Мы её обязательно исправим. Возвращайтесь чуть позже."
    )

    tts = (
        "<speaker audio='alice-sounds-game-loss-3.opus'>"
        "Прошу прощения, в навыке возникла непредвиденная ошибка."
        "sil<[200]> Мы её обязательно исправим. Возвращайтесь чуть позже."
    )

    return text, tts


def sorry_and_goodbye():
    text = (
        "Прошу прощения, я очень стараюсь вас понять.\n"
        "Но пока не получается. Возможно, мне стоит отдохнуть. Возвращайтесь позже.\n"
        "До свидания!"
    )

    tts = (
        "<speaker audio='alice-sounds-game-loss-3.opus'>"
        "Прошу прощения, я очень стараюсь вас понять."
        "sil<[200]>Но пока не получается. Возможно, мне стоит отдохнуть. Возвращайтесь позже."
        "До свидания!"
    )

    return text, tts


def fallback():
    text = (
        "Извините, я вас не поняла. Пожалуйста, повторите.\n"
        'Скажите "Помощь", чтобы узнать как работает навык.'
    )
    tts = (
        "Извините, я вас не поняла. Пожалуйста, повторите.\n"
        "sil<[100]>"
        "Скажите Помощь, чтобы узнать как работает навык."
    )

    return text, tts


# endregion


def need_auth(scene_id):
    if scene_id == "Welcome":
        text = (
            "Привет! Это цифровой дневник для учеников Санкт-Петербурга.\n"
            "Я могу подсказать расписание уроков на любой день.\n"
            "Но для начала нужно выполнить авторизацию."
        )
        tts = (
            "Привет! Это цифровой дневник для школьников из города Санкт-Петербурга."
            "Я могу подсказать расписание уроков на любой день."
            "Скажите sil<[100]>Что ты умеешь? и расскажу подробнее."
        )
    else:
        text = "Сеанс устарел. Обновите данные."
        tts = text

    return text, tts


# region Меню помощь


def help_menu_start():
    text = (
        "С помощью этого навыка вы сможете узнать расписание в школе.\n"
        "Чтобы узнать расписание скажите:\n"
        '"Подскажи расписание?"\n'
        "Или, если хотите на определенный день:\n"
        '"Какие уроки во вторник?"\n'
        "Если есть несколько учеников, добавьте имя:\n"
        '"Какое расписание у Миши послезавтра?"\n'
        "Теперь вы знаете как узнать расписание учеников."
        "Хотите расскажу как узнать какие были оценки?"
    )

    tts = (
        "С помощью этого навыка вы сможете узнать расписание в школе.\n"
        "Чтобы узнать расписание скажите:\n"
        'sil<[100]>"Подскажи расписание?"\n'
        "Или, если хотите на определенный день:\n"
        'sil<[100]>"Какие уроки во вторник?"\n'
        "Если есть несколько учеников, добавьте имя:\n"
        'sil<[100]>"Какое расписание у Миши послезавтра?"\n'
        "Теперь вы знаете как узнать расписание учеников."
        "Хотите расскажу как узнать какие были оценки?"
    )

    return text, tts


def help_menu_marks():
    text = (
        "Так же можно узнать оценки или замечания.\n"
        "Оценки за сегодня выводятся при запуске навыка.\n"
        "Но можно узнать в любой момент.\n"
        "Скажите\n"
        '"Какие сегодня оценки?"\n'
        "Или"
        '"Какие записи в журнале были у Миши вчера?"\n'
        "Тогда я скажу какие оценки были по предметам. И были ли замечания\n"
        "А еще у меня есть специальные возможности.\n"
        "Хотите расскажу?"
    )

    tts = (
        "Так же можно узнать оценки или замечания.\n"
        "Оценки за сегодня выводятся при запуске навыка.\n"
        "Но можно узнать в любой момент.\n"
        "Скажите\n"
        'sil<[100]>"Какие сегодня оценки?"\n'
        "Или"
        'sil<[100]>"Какие записи в журнале были у Миши вчера?"\n'
        "Тогда я скажу какие оценки были по предметам. И были ли замечания\n"
        "А еще у меня есть специальные возможности.\n"
        "Хотите расскажу?"
    )

    return text, tts


def help_menu_spec():
    text = (
        "У меня есть несколько режимов запуска:\n"
        "Можете сказать:\n"
        '"Алиса, запусти навык Дневник ученика Питера"\n'
        "И попадете в это приложение:\n"
        "А можете сказать:\n"
        '"Алиса, спроси у Дневника ученика Питера какие уроки завтра?"\n'
        "Тогда я сразу отвечу на ваш вопрос.\n"
        "Теперь вы знаете как пользоваться навыком. \n"
    )
    tts = (
        "У меня есть несколько режимов запуска:\n"
        "Можете сказать:\n"
        "sil<[100]>Алиса, запусти навык Дневник ученика Питера\n"
        "И попадете в это приложение:\n"
        "А можете сказать:\n"
        "sil<[100]>Алиса, спроси у Дневника ученика Питера какие уроки завтра?\n"
        "Тогда я сразу отвечу на ваш вопрос.\n"
        "Дату можете указать любую.\n"
        "Теперь вы знаете как пользоваться навыком. \n"
        "Скажите Главное меню или Расписание уроков."
    )

    return text, tts


def what_can_i_do():
    text = (
        "Этот навык помогает работать с дневником в школе.\n"
        "Я могу подсказать расписание уроков на любой день.\n"
        'Спросите, например, "Какие уроки завтра?"\n'
        "Рассказать подробнее, что я умею?"
    )

    tts = (
        "Этот навык помогает работать с дневником в школе.\n"
        "Я могу подсказать расписание уроков на любой день.\n"
        "sil<[100]>Спросите, например. Какие уроки завтра?"
        "Рассказать подробнее, что я умею?"
    )

    return text, tts


# endregion


def welcome_start():
    text = "Дневник ученика Петербурга"
    tts = "Привет! Это дневник ученика Петербурга! Давайте заглянем в журнал."
    return text, tts


def welcome_end():
    text = ""
    tts = "Хотите узнать расписание уроков?"

    return text, tts


def goodbye():
    text = "До свидания.\n Возвращайтесь в любое время."
    tts = "До свидания! sil<[100]> Возвращайтесь скорее."
    return text, tts


# region Вспомогательные


def title_date(req_date):
    if req_date is None:
        str_date = "сегодня"
    elif req_date.date() in KNOWN_DATES:
        str_date = KNOWN_DATES[req_date.date()]
    else:
        str_date = (
            f"{req_date.date().day} {text_constants.MONTH_NAME[req_date.date().month]}"
        )

    return f"На {str_date}"


def nothing_to_repeat():
    text = "Нечего повторять"
    tts = "Простите! Но я не знаю, что надо повторить."
    "sil<[100]>Скажите помощь и я расскажу что умею"

    return text, tts


def __how_many_lessons(n: int) -> str:
    if n == 0:
        return "Нет уроков."
    first = n % 10
    second = n % 100

    if (2 <= first <= 4) and not (12 <= second <= 14):
        last = "урока"
    elif first == 1 and not second == 11:
        last = "урок"
    else:
        last = "уроков"

    return f"{str(n)} {last}"


def __how_many_tasks(n: int) -> str:
    if n == 0:
        return "Нет домашнего задания."
    first = n % 10
    second = n % 100

    if (2 <= first <= 4) and not (12 <= second <= 14):
        last = "задания."
    elif first == 1 and not second == 11:
        last = "задание."
    else:
        last = "заданий."

    return f"{str(n)} {last}"


# endregion


def unknown_student():
    text = (
        "Прошу прощения. Но у меня нет данных.\n" "Возможно ошиблись в имени ученика?"
    )
    tts = (
        '<speaker audio="alice-sounds-human-crowd-2.opus">'
        "Прошу прощения. Но у меня нет данных.\n"
        "sil<[100]>Возможно ошиблись в имени ученика?"
    )

    return text, tts


# region Расписание уроков


def schedule_title(req_date):
    title = title_date(req_date)
    text = f"Расписание уроков. {title}"
    tts = f"Расписание на {title}"

    return text, tts


def homework_title(req_date):
    title = title_date(req_date)
    text = f"Домашнее задание. {title}"
    tts = f"Домашнее задание на {title}"

    return text, tts


def schedule_for_student(student: Student, schedule: Schedule):
    count = len(schedule.lessons)
    count_str = __how_many_lessons(count)

    text = [f"{student.name}. {count_str}"]
    tts = [f"У {student.inflect['родительный']} {count_str}"]
    if schedule.no_lessons:
        return text[0], tts[0]

    first_lesson = schedule.lessons[0]
    if first_lesson.num != 1:
        tts.append(
            f"К {text_constants.ORDINAL_NUMBERS_DATIVE[first_lesson.num]} уроку в {first_lesson.start_time}"
        )
    else:
        tts.append(f"Уроки начинаются в {first_lesson.start_time}")

    # Расписание
    repeat_lessons_count = 1
    for i in range(len(schedule.lessons)):
        lesson = schedule.lessons[i]
        text.append(f"{lesson.num}. {lesson} {lesson.duration}")
        if i == 0:
            tts.append(lesson.name)
        else:
            if schedule.lessons[i - 1] == lesson:
                repeat_lessons_count += 1
            elif repeat_lessons_count > 1:
                tts[-1] += " " + __how_many_lessons(repeat_lessons_count)
                repeat_lessons_count = 1
                tts.append(lesson.name)
            else:
                tts.append(lesson.name)

    if repeat_lessons_count > 1:
        tts[-1] += " " + __how_many_lessons(repeat_lessons_count)

    tts.append(f"Уроки закончатся в {schedule.lessons[-1].end_time}")

    return "\n".join(text), "sil<[100]>".join(tts)


def homework_for_student(student: Student, homework: List):
    count = len(homework)
    count_str = __how_many_tasks(count)

    text = [f"{student.name}. {count_str}"]
    tts = [f"У {student.inflect['родительный']} {count_str}"]
    if not homework:
        return text[0], tts[0]

    # Домашка
    for lesson, task in homework:
        text.append(f"{lesson}. {task}")
        tts.append(__tell_about_task(lesson, task))

    return "\n".join(text), "sil<[100]>".join(tts)


def __tell_about_task(lesson: str, task: str):
    tell_task = (
        task.replace("§", "параграф ")
        .replace("№№", "номера ")
        .replace("№", "номер ")
        .replace("стр.", "страница ")
        .replace("с.", "страница ")
        .replace("упр.", "упражнение ")
        .replace("у.", "упражнение ")
        .replace("ур.", "урок ")
    )
    return f"sil<[200]> {lesson} sil<[300]> {tell_task}"


def lesson_num_title(num: int, req_date):
    title = title_date(req_date)
    text = f"{title}. {num} урок:"
    tts = f"{title} {text_constants.ORDINAL_NUMBERS_NOMINATIVE[num]} урок"
    return text, tts


def no_lesson(student: Student, num: int):
    text = f"{student.name}. Нет урока."
    tts = f"У {student.inflect['родительный']} нет {text_constants.ORDINAL_NUMBERS_DATIVE[num]} урока."
    return text, tts


def num_lesson(student: Student, lesson: PlannedLesson):
    text = f"{student.name} - {lesson.name}: {lesson.duration}"
    tts = (
        f"У {student.inflect['родительный']} будет {lesson.name}. "
        f"Начнется в {lesson.start_time}, закончится в {lesson.end_time}"
    )
    return text, tts


# endregion

# region Записи в журнале


def journal_title(req_date):
    title = title_date(req_date)
    text = f"Записи в журнале. {title}"
    tts = f"Записи в журнале на {title}"

    return text, tts


def no_marks(student: Student):
    text = f"{student.name}. Нет записей"
    tts = f"По {student.inflect['дательный']} нет записей в журнале"
    return text, tts


def marks_for_student(student: Student, journal: Journal):
    text = []
    tts = []

    text.append(student.name)
    tts.append(f"У {student.inflect['родительный']}")

    for lesson, records in journal.records:
        text_record = [lesson]
        tts_record = [lesson]
        all_works: Dict[str, List[str]] = {}
        for rec in records:
            if rec.is_legal_skip:
                pass
            elif rec.is_illegal_skip or rec.is_late:
                text_record.append(str(rec))
                tts_record.append(str(rec))
            else:
                all_works.setdefault(rec.work, []).append(rec.mark)
        if all_works:
            temp_text = "; ".join(
                [work + " " + ", ".join(marks) for work, marks in all_works.items()]
            )
            temp_tts = "sil<[200]> ".join(
                [work + " " + " и ".join(marks) for work, marks in all_works.items()]
            )
            text_record.append(temp_text)
            tts_record.append(temp_tts)
        if len(text_record) > 1:
            text.append(". ".join(text_record))
            tts.append(". ".join(tts_record))

    return "\n".join(text), " sil<[200]>".join(tts)


# endregion


KNOWN_DATES = {
    datetime.date.today(): "Сегодня",
    datetime.date.today() + datetime.timedelta(days=1): "Завтра",
    datetime.date.today() + datetime.timedelta(days=2): "Послезавтра",
    datetime.date.today() + datetime.timedelta(days=-1): "Вчера",
    datetime.date.today() + datetime.timedelta(days=-2): "Позавчера",
}
