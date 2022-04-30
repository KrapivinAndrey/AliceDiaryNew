import os
from datetime import date, datetime, time
from typing import Dict, List

import requests

from skill.dataclasses import PlannedLesson, Schedule, Student, Students


class NotFoundError(Exception):
    pass


class NeedAuth(Exception):
    pass


# region URLs


def base_url():
    url = os.environ.get("DIARY_URL", "https://journal.bpo.edu.n3demo.ru/api/journal")
    assert url, "Не заполнен url для запросов"

    return url


def schedule_url():
    return f"{base_url()}/schedule/list-by-education"


def students_url():
    return f"{base_url()}/person/related-child-list"


# endregion


def get_students(token: str) -> List[Student]:
    result = Students()
    response = requests.get(
        students_url(),
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()

    for student in response.json().get("data", {}).get("items", []):
        name = student.get("firstname", "")
        education_id = student.get("educations", [])[0].get("education_id", "")
        new_student = Student(name, education_id)
        result.add_student(new_student)

    return result


def get_schedule(token: str, student_id: str, day=date.today()) -> List[PlannedLesson]:
    start_time = datetime.combine(day, time.min)
    finish_time = datetime.combine(day, time.max)

    response = requests.get(
        schedule_url(),
        params={
            "p_educations[]": id,
            "p_datetime_from": datetime.strftime(start_time, "%d.%m.%Y %H:%M:%S"),
            "p_datetime_to": datetime.strftime(finish_time, "%d.%m.%Y %H:%M:%S"),
        },
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()

    result = Schedule()
    for lesson in response.json().get("data", {}).get("items", []):
        template = "%d.%m.%Y %H:%M:%S"
        time_from = datetime.strptime(lesson["datetime_from"], template).time()
        time_to = datetime.strptime(lesson["datetime_to"], template).time()
        result.lessons.append(
            PlannedLesson(lesson["subject_name"], time_from, time_to),
        )

    result.lessons.sort()
    return result
