import skill.texts as texts


class TestMarks:
    def test_full(self, studentDmitry, full_journal):
        text, tts = texts.marks_for_student(studentDmitry, full_journal)
        assert (
            text
            == "Дмитрий\nРусский язык. Изложение 2, 4\nМатематика. Опоздание. Работа на уроке 3\nХимия. Прогул"
        )
        assert (
            tts
            == "У дмитрия sil<[200]>Русский язык. Изложение 2, 4 sil<[200]>Математика. Опоздание. Работа на уроке 3 sil<[200]>Химия. Прогул"
        )

    def test_empty(self, studentDmitry):
        text, tts = texts.no_marks(studentDmitry)
        assert text == "Дмитрий. Нет записей"
        assert tts == "По дмитрию нет записей в журнале"
