from datetime import time

from alicefluentcheck import AliceEntity, AliceIntent, AliceIntentSlot, AliceRequest
from pytest import fixture

from skill.dataclasses.lessons import PlannedLesson, Schedule
from skill.dataclasses.students import Student, Students

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
