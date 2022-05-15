import datetime
import locale

from skill.dataclasses import Schedule, Student

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


def goodbye():
    text = "Возвращайтесь в любое время. До свидания!"
    tts = "<speaker audio='alice-sounds-game-loss-3.opus'>" + text
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
        "Хотите расскажу о моих специальных возможностях?"
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
        "Хотите расскажу о моих специальных возможностях?"
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


def hello(students):
    text = tts = "Здесь будет todo"
    return text, tts


# region Вспомогательные


def title(start: str, req_date):
    if req_date is None:
        str_date = "Сегодня"
    elif req_date.date() in KNOWN_DATES:
        str_date = KNOWN_DATES[req_date.date()]
    else:
        str_date = datetime.date.strftime(req_date.date(), "%d %B")

    text = f"{start} на {str_date}"

    return text, text


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


def schedule_for_student(student: Student, schedule: Schedule):
    count = len(schedule.lessons)
    count_str = __how_many_lessons(count)

    text = [f"{student.name}. {count_str}"]
    tts = [f"У {student.inflect['родительный']} {count_str}"]
    if schedule.no_lessons:
        return text[0], tts[0]

    if schedule.lessons[0].num != 1:
        tts.append(
            f"К {ORDINAL_NUMBERS[schedule.lessons[0].num]} уроку в {schedule.lessons[0].start_time}"
        )
    else:
        tts.append(f"Уроки начинаются в {schedule.lessons[0].start_time}")

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


locale.setlocale(locale.LC_TIME, ("RU", "UTF8"))  # the ru locale is installed

KNOWN_DATES = {
    datetime.date.today(): "Сегодня",
    datetime.date.today() + datetime.timedelta(days=1): "Завтра",
    datetime.date.today() + datetime.timedelta(days=2): "Послезавтра",
    datetime.date.today() + datetime.timedelta(days=-1): "Вчера",
    datetime.date.today() + datetime.timedelta(days=-2): "Позавчера",
}

ORDINAL_NUMBERS = [
    "",
    "первому",
    "второму",
    "третьему",
    "четвертому",
    "пятому",
    "шестому",
    "седьмому",
    "восьмому",
    "девятому",
    "десятому",
]
