from datetime import time
from typing import List, Union

from ..constants.entities import image_ids, subjects


class PlannedLesson:
    def __init__(self, num: int, name: str, start: time, end: time):
        self.num = num
        self.name = name
        self.start = start
        self.end = end

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

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
        result = image_ids["default"]
        for key, value in subjects.items():
            name_subject = ""
            if self.name.lower() in value:
                name_subject = key
            if image_ids.get(name_subject) is not None:
                result = image_ids[name_subject]

        return result


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
            (lesson for lesson in self.lessons if lesson.start <= find <= lesson.end),
            None,
        )

    @property
    def no_lessons(self):
        return len(self.lessons) == 0

    @property
    def list_of_lessons(self) -> List[str]:
        return [x.name for x in self.lessons]
