from datetime import datetime
from typing import List


class Homework:
    def __init__(self):
        self.__tasks = {}
        self.__last_date = {}

    def add(self, date, lesson: str, task: str):
        new_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        if self.__last_date.get(lesson) is None or self.__last_date[lesson] < new_date:

            self.__tasks[lesson] = task
            self.__last_date[lesson] = new_date

    def filter_by_lessons(self, lessons: List[str]):
        # TODO: добавить нечеткое сравнение строк
        return [(lesson, task) for lesson, task in self.__tasks.items() if lesson in lessons]

    @property
    def len(self) -> int:
        return len(self.__tasks)
