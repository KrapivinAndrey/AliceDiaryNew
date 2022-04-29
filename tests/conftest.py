import pytest
from skill.dataclasses.students import Student, Students
from skill.dairy_api import students_url


@pytest.fixture
def studentAlice():
    test = Student("Алиса", "1")
    return test


@pytest.fixture
def studentAnotherAlice():
    test = Student("Алиса", "2")
    return test


@pytest.fixture
def studentDmitry():
    test = Student("Дмитрий", "100")
    return test


@pytest.fixture
def student_dump():
    return {
        "name": "Алиса",
        "id": "1",
        "inflect": {"родительный": "алисы", "дательный": "алисе"},
    }


@pytest.fixture
def students_Alice_and_Dmitry(studentAlice, studentDmitry):
    test = Students()
    test.add_student(studentAlice)
    test.add_student(studentDmitry)

    return test


@pytest.fixture
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
