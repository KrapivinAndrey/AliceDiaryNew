from diary.skill.dataclasses import Record, Journal


class TestRecord:
    def test_mark(self):
        rec = Record("123", "Оценка", "5/5", "5", "Работа на уроке")
        assert str(rec) == "Оценка 5 Работа на уроке"

    def test_is_late(self):
        rec = Record("30000", "Опоздал", "", "")
        assert rec.is_late
        assert str(rec) == "Опоздание"

    def test_is_legal(self):
        rec = Record("30000", "Болел", "496", "")
        assert rec.is_legal_skip
        assert str(rec) == "Пропуск"

    def test_is_illegal(self):
        rec = Record("30000", "Отсутствие на уроке", "493", "")
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
        assert (
            str(journal) == "Русский язык: Изложение 2\nМатематика: Работа на уроке 3"
        )

    def test_two_records(self, narration2, narration4):
        journal = Journal()
        journal.add("Русский язык", narration2)
        journal.add("Русский язык", narration4)

        assert journal.len == 1
        assert str(journal) == "Русский язык: Изложение 2, Изложение 4"
