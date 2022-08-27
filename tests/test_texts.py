from diary.skill import texts


class TestMarks:
    def test_full(self, studentDmitry, full_journal):
        text, tts = texts.marks_for_student(studentDmitry, full_journal)
        assert (
            text
            == "Дмитрий\nРусский язык. Изложение 2, 4\nМатематика. Опоздание. Работа на уроке 3\nХимия. Прогул"
        )
        assert (
            tts
            == "У дмитрия sil<[200]>Русский язык. Изложение 2 и 4 sil<[200]>Математика. Опоздание. Работа на уроке 3 sil<[200]>Химия. Прогул"
        )

    def test_empty(self, studentDmitry):
        text, tts = texts.no_marks(studentDmitry)
        assert text == "Дмитрий. Нет записей"
        assert tts == "По дмитрию нет записей в журнале"


class TestHomework:
    def test_no_homework(self, studentDmitry):
        text, tts = texts.homework_for_student(studentDmitry, [])

        assert text == "Дмитрий. Нет домашнего задания."
        assert tts.lower() == "у дмитрия нет домашнего задания."

    def test_some_homework(self, studentDmitry):
        homework = [("География", "стр. 45")]

        text, tts = texts.homework_for_student(studentDmitry, homework)

        assert "Дмитрий. 1 задание." in text
        assert "у дмитрия 1 задание." in tts.lower()

        assert "География. стр. 45" in text
        assert "страница  45" in tts.lower()
