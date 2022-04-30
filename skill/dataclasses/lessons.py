from datetime import time

from skill.constants.entities import image_ids, subjects
from typing import Union


class PlannedLesson:
    def __init__(self, name: str, start: time, end: time):
        self.name = name
        self.start = start
        self.end = end

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    @property
    def start_time(self):
        if self.start is not None:
            return time.strftime(self.start, "%H:%M")
        else:
            return ""

    @property
    def end_time(self):
        if self.end is not None:
            return time.strftime(self.end, "%H:%M")
        else:
            return ""

    @property
    def duration(self):
        result = ""
        if self.start and self.end:
            result = f"{self.start_time} - {self.end_time}"
        return result

    @property
    def link_url(self):
        result = ""
        for key, value in subjects.items():
            name_subject = ""
            if self.name.lower() in value:
                name_subject = key
            if not image_ids.get(name_subject) is None:
                result = image_ids[name_subject]


class Schedule:
    def __init__(self):
        self.lessons = []

    def find_by_num(self, num: int) -> Union[None, PlannedLesson]:
        if num > len(self.lessons):
            return None
        else:
            return self.lessons[num - 1]

    def find_by_time(self, find: time) -> Union[None, PlannedLesson]:
        return next(
            (
                lesson
                for lesson in self.lessons
                if lesson.start <= find <= lesson.end
            ),
            None,
        )
