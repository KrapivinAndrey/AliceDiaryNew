from skill.dataclasses.marks import Record, Journal


class TestRecord:
    def test_create(self):
        rec = Record("123", "Взятка", "5/5", "5", "Хороший коньяк")
        assert str(rec) == "Взятка 5 Хороший коньяк"

    def test_is_late(self):
        rec = Record("30000", "Опоздал", "", "")
        assert rec.is_late
        assert str(rec) == "Опоздание"

    def test_is_late(self):
        rec = Record("30000", "Болел", "123", "")
        assert rec.is_legal_skip
        assert str(rec) == "Пропуск"

    def test_is_late(self):
        rec = Record("30000", "Курил за гаражом", "493", "")
        assert rec.is_illegal_skip
        assert str(rec) == "Прогул"

