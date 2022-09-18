from diary.skill.dataclasses import Homework
from datetime import datetime


class TestHomework:
    def test_create(self):
        homework = Homework()
        assert homework.len == 0

    def test_add_one(self):
        homework = Homework()
        homework.add("01.01.2001 00:00:00", "География", "Найти глобус")

        assert homework.len == 1

    def test_add_two_different(self):
        homework = Homework()
        homework.add("01.01.2001 00:00:00", "География", "Найти глобус")
        homework.add("02.01.2001 00:00:00", "Литература", "Выучить стих")

        assert homework.len == 2

    def test_add_two_same(self):
        homework = Homework()
        homework.add("01.01.2001 00:00:00", "География", "Найти глобус")
        homework.add("02.01.2001 00:00:00", "География", "Заполнить контурные карты")

        assert homework.len == 1

    def test_add_three(self):
        homework = Homework()
        homework.add("01.01.2001 00:00:00", "География", "Найти глобус")
        homework.add("02.01.2001 00:00:00", "География", "Заполнить контурные карты")
        homework.add("02.01.2001 00:00:00", "Литература", "Выучить стих")

        assert homework.len == 2

    def test_filter(self):
        homework = Homework()
        homework.add("01.01.2001 00:00:00", "География", "Найти глобус")
        homework.add("02.01.2001 00:00:00", "География", "Заполнить контурные карты")
        homework.add("02.01.2001 00:00:00", "Литература", "Выучить стих")

        assert homework.filter_by_lessons(["География"]) == [
            ("География", "Заполнить контурные карты")
        ]

    def test_big_filter(self):
        homework = Homework()
        homework.add("01.01.2001 00:00:00", "География", "Найти глобус")
        homework.add("02.01.2001 00:00:00", "География", "Заполнить контурные карты")
        homework.add("02.01.2001 00:00:00", "Литература", "Выучить стих")
        homework.add("01.01.2001 00:00:00", "Русский язык", "Подготовить диктант")
        homework.add("01.01.2001 00:00:00", "Физкультура", "Взять лыжи")

        assert homework.filter_by_lessons(["География", "Физкультура", "ИЗО"]) == [
            ("География", "Заполнить контурные карты"),
            ("Физкультура", "Взять лыжи"),
        ]
