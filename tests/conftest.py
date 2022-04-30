from datetime import time

from pytest import fixture

from skill.dataclasses.lessons import PlannedLesson
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
    return PlannedLesson("Алгебра", time(8, 0), time(8, 40))


@fixture
def russian():
    return PlannedLesson("Русский язык", time(9, 50), time(10, 30))


@fixture
def geometry():
    return PlannedLesson("Геометрия", time(16, 30), time(17, 10))


# endregion
