from datetime import time

from alicefluentcheck import AliceEntity, AliceIntent, AliceIntentSlot, AliceRequest
from pytest import fixture

from skill.dataclasses import (
    PlannedLesson,
    Schedule,
    Student,
    Students,
    Record,
    Journal,
)


# region Студенты


@fixture
def studentAlice():
    test = Student("Алиса", "1")
    return test


@fixture
def studentAnotherAlice():
    test = Student("Алиса", "2")
    return test


@fixture
def studentDmitry():
    test = Student("Дмитрий", "100")
    return test


@fixture
def students_Alice_and_Dmitry(studentAlice, studentDmitry):
    test = Students()
    test.add_student(studentAlice)
    test.add_student(studentDmitry)

    return test


# endregion

# region Дампы студентов


@fixture
def student_dump():
    return {
        "name": "Алиса",
        "id": "1",
        "inflect": {"родительный": "алисы", "дательный": "алисе"},
    }


@fixture
def students_dump():
    return [
        {
            "name": "Алиса",
            "id": "1",
            "inflect": {"родительный": "алисы", "дательный": "алисе"},
        },
        {
            "name": "Дмитрий",
            "id": "100",
            "inflect": {"родительный": "дмитрия", "дательный": "дмитрию"},
        },
    ]


# endregion


# region Предметы


@fixture
def algebra():
    return PlannedLesson(1, "Алгебра", time(8, 0), time(8, 40))


@fixture
def russian():
    return PlannedLesson(2, "Русский язык", time(9, 50), time(10, 30))


@fixture
def geometry():
    return PlannedLesson(3, "Геометрия", time(16, 30), time(17, 10))


@fixture
def schedule(algebra, russian, geometry):
    result = Schedule()
    result.lessons.append(algebra)
    result.lessons.append(russian)
    result.lessons.append(geometry)

    result.lessons.sort()

    return result


@fixture
def schedule_short(russian, geometry):
    result = Schedule()
    result.lessons.append(russian)
    result.lessons.append(geometry)

    result.lessons.sort()

    return result


# endregion

# region Оценки и журнал


@fixture
def narration4():
    return Record("123", "Изложение", "4/5", "4")


@fixture
def narration2():
    return Record("123", "Изложение", "2/5", "2")


@fixture
def lesson3():
    return Record("123", "Работа на уроке", "3/5", "3")


@fixture
def late():
    return Record("30000", "Опоздал", "", "")


@fixture
def missing():
    return Record("30000", "Не был на уроке", "493", "")


@fixture
def sport():
    return Record("30000", "Участие в олимпиаде", "494", "")


@fixture
def full_journal(narration2, narration4, lesson3, late, missing, sport):
    journal = Journal()
    journal.add("Русский язык", narration2)
    journal.add("Русский язык", narration4)
    journal.add("Математика", lesson3)
    journal.add("Математика", late)
    journal.add("Физкультура", sport)
    journal.add("Химия", missing)
    return journal


@fixture
def empty_journal():
    journal = Journal()
    return journal


# endregion

# region Базовое поведение

# region Начало диалога


@fixture
def start_skill():
    return AliceRequest().command("").build()


@fixture
def start_skill_auth():
    req = AliceRequest().command("").access_token("111").build()

    return req


# endregion

# region Некорректные команды


# endregion

# endregion
