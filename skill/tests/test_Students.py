from skill.dataclasses.students import Student, Students
from pytest import fixture


@fixture
def studetnAlice():
    test = Student("Алиса", "1")
    return test


@fixture
def studetnAnotherAlice():
    test = Student("Алиса", "2")
    return test


@fixture
def studetnDmitry():
    test = Student("Дмитрий", "100")
    return test


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

    def test_dump(self, studetnAlice):
        assert (studetnAlice.dump() == {"name": "Алиса", "id": "1"})
