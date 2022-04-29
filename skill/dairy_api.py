import os
from datetime import date, datetime, time
from typing import Dict, List

import requests
import requests_mock

from skill.dataclasses import PlannedLesson, Student, Students


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
    response = requests.get(students_url(), cookies={"X-JWT-Token": token})

    if response.status_code == 401:
        raise NeedAuth()

    for student in response.json().get("data", {}).get("items", []):
        name = student.get("firstname", "")
        id = student.get("educations", [])[0].get("education_id", "")
        new_student = Student(name, id)
        result.add_student(new_student)

    return result
