from skill.dataclasses.students import Student, Students
from pytest import fixture


@fixture
def studentAlice():
    test = Student()
    test.create("Алиса", "1")
    return test


@fixture
def studentAnotherAlice():
    test = Student()
    test.create("Алиса", "2")
    return test


@fixture
def studentDmitry():
    test = Student()
    test.create("Дмитрий", "100")
    return test


@fixture
def student_dump():
    return {
        "name": "Алиса",
        "id": "1",
        "inflect": {"родительный": "алисы", "дательный": "алисе"},
    }


@fixture
def students_Alice_and_Dmitry(studentAlice, studentDmitry):
    test = Students()
    test.add_student(studentAlice)
    test.add_student(studentDmitry)

    return test


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
        }
    ]


class Test_Student:
    def test_create(self, studentAlice):
        assert studentAlice.name == "Алиса"
        assert studentAlice.id == "1"

    def test_repr(self, studentAlice):
        assert str(studentAlice) == "Алиса"

    def test_inflect_woman(self, studentAlice):
        assert studentAlice.inflect["родительный"] == "алисы"
        assert studentAlice.inflect["дательный"] == "алисе"

    def test_inflect_man(self, studentDmitry):
        assert studentDmitry.inflect["родительный"] == "дмитрия"
        assert studentDmitry.inflect["дательный"] == "дмитрию"

    def test_compare(self, studentAlice, studentAnotherAlice):
        assert studentAlice == "Алиса"
        assert studentAlice != studentAnotherAlice

    def test_hash(self, studentAlice):
        assert isinstance(hash(studentAlice), int)

    def test_dump(self, studentAlice, student_dump):
        assert studentAlice.dump() == student_dump

    def test_restore(self, studentAlice, student_dump):
        test = Student()
        test.restore(student_dump)

        assert test == studentAlice


class Test_Students:
    def test_empty(self):
        test = Students()
        assert test.students == {}

    def test_create(self, students_Alice_and_Dmitry, studentAlice):
        assert len(students_Alice_and_Dmitry.students) == 2
        assert students_Alice_and_Dmitry.students["1"] == studentAlice

    def test_dump(self, students_Alice_and_Dmitry, students_dump):
        assert students_Alice_and_Dmitry.dump() == students_dump

    def test_restore(self, students_dump, studentAlice):
        test = Students()
        test.restore(students_dump)
        assert len(test.students) == 2
        assert test.students["1"] == studentAlice
