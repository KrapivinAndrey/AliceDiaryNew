from pytest import fixture

from datetime import time
from skill.dataclasses.lessons import PlannedLesson


@fixture
def algebra():
    return PlannedLesson("Алгебра", time(8, 0), time(8, 40))


@fixture
def russian():
    return PlannedLesson("Русский язык", time(9, 50), time(10, 30))


@fixture
def geometry():
    return PlannedLesson("Геометрия", time(16, 30), time(17, 10))


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
