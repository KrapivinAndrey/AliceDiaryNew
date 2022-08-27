from datetime import time

from diary.skill.dataclasses.lessons import Schedule


class TestLessons:
    def test_create(self, algebra):
        assert algebra.name == "Алгебра"
        assert algebra.start == time(8, 0)
        assert algebra.end == time(8, 40)

    def test_repr(self, algebra):
        assert str(algebra.name) == "Алгебра"

    def test_compare(self, algebra, russian, geometry):
        assert algebra < russian
        assert geometry > russian

    def test_start(self, algebra):
        assert algebra.start_time == "08:00"

    def test_end(self, algebra):
        assert algebra.end_time == "08:40"

    def test_duration(self, algebra):
        assert algebra.duration == "08:00 - 08:40"


class TestSchedule:
    def test_create(self):
        schedule = Schedule()
        assert schedule is not None
        assert len(schedule.lessons) == 0

    def test_get_num_in_list(self, schedule):
        assert str(schedule.find_by_num(2)) == "Русский язык"

    def test_get_num_not_in_list(self, schedule):
        assert schedule.find_by_num(5) is None

    def test_get_by_time(self, schedule):
        test_time = time(10, 30)
        assert str(schedule.find_by_time(test_time)) == "Русский язык"

    def test_get_by_time_none(self, schedule):
        test_time = time(17, 30)
        assert schedule.find_by_time(test_time) is None

    def test_list(self, schedule):
        assert schedule.list_of_lessons == ["Алгебра", "Русский язык", "Геометрия"]
