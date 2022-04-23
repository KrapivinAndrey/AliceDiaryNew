from skill.dataclasses.students import Student, Students
from pytest import fixture


@fixture
def studetnAlice():
    test = Student()
    test.create("Алиса", "1")
    return test


@fixture
def studetnAnotherAlice():
    test = Student()
    test.create("Алиса", "2")
    return test


@fixture
def studetnDmitry():
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


class Test_Student:
    def test_create(self, studetnAlice):
        assert studetnAlice.name == "Алиса"
        assert studetnAlice.id == "1"

    def test_repr(self, studetnAlice):
        assert str(studetnAlice) == "Алиса"

    def test_inflect(self, studetnAlice):
        assert studetnAlice.inflect["родительный"] == "алисы"
        assert studetnAlice.inflect["дательный"] == "алисе"

    def test_compare(self, studetnAlice, studetnAnotherAlice):
        assert studetnAlice == "Алиса"
        assert studetnAlice != studetnAnotherAlice

    def test_hash(self, studetnAlice):
        assert isinstance(hash(studetnAlice), int)

    def test_dump(self, studetnAlice, student_dump):
        assert studetnAlice.dump() == student_dump

    def test_restore(self, studetnAlice, student_dump):
        test = Student()
        test.restore(student_dump)

        assert test == studetnAlice
