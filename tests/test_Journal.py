from skill.dataclasses.marks import Record, Journal
from pytest import fixture


@fixture
def narration4():
    return Record("123", "Изложение", "4/5", "4")


@fixture
def narration2():
    return Record("123", "Изложение", "2/5", "2")


@fixture
def lesson3():
    return Record("123", "Работа на уроке", "3/5", "3")


class TestRecord:
    def test_create(self):
        rec = Record("123", "Взятка", "5/5", "5", "Хороший коньяк")
        assert str(rec) == "Взятка 5 Хороший коньяк"

    def test_is_late(self):
        rec = Record("30000", "Опоздал", "", "")
        assert rec.is_late
        assert str(rec) == "Опоздание"

    def test_is_legal(self):
        rec = Record("30000", "Болел", "123", "")
        assert rec.is_legal_skip
        assert str(rec) == "Пропуск"

    def test_is_illegal(self):
        rec = Record("30000", "Курил за гаражом", "493", "")
        assert rec.is_illegal_skip
        assert str(rec) == "Прогул"


class TestJournal:
    def test_create(self):
        journal = Journal()
        assert str(journal) == ""

    def test_one_record(self, narration2):
        journal = Journal()
        journal.add("Русский язык", narration2)

        assert journal.len == 1
        assert str(journal) == "Русский язык: Изложение 2"

    def test_two_lesson(self, narration2, lesson3):
        journal = Journal()
        journal.add("Русский язык", narration2)
        journal.add("Математика", lesson3)

        assert journal.len == 2
        assert str(journal) == "Русский язык: Изложение 2\nМатематика: Работа на уроке 3"

    def test_two_records(self, narration2, narration4):
        journal = Journal()
        journal.add("Русский язык", narration2)
        journal.add("Русский язык", narration4)

        assert journal.len == 1
        assert str(journal) == "Русский язык: Изложение 2, Изложение 4"