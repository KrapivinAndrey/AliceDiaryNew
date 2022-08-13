import os
from datetime import date, datetime, time

import requests

from skill.constants.exceptions import NeedAuth
from skill.dataclasses import (
    Journal,
    PlannedLesson,
    Record,
    Schedule,
    Student,
    Students,
)
from skill.loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger(__name__, log_level="DEBUG")
# region URLs


def base_url():
    url = os.environ.get("DIARY_URL", "https://dnevnik2.petersburgedu.ru/api/journal")
    assert url, "Не заполнен url для запросов"

    return url


def schedule_url():
    return f"{base_url()}/schedule/list-by-education"


def students_url():
    return f"{base_url()}/person/related-child-list"


def journal_url():
    return f"{base_url()}/lesson/list-by-education"


def refresh_url():
    return f"{base_url()}/user/token-refresh"


# endregion


def get_students(token: str) -> Students:
    result = Students()
    response = requests.get(
        students_url(),
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()
    try:
        api_students = response.json().get("data", {}).get("items", [])
    except (Exception,):
        logger.exception(
            f"Не удалось разобрать тело ответа", extra={"body": response.text}
        )
        raise

    for student in api_students:
        name = student.get("firstname", "")
        education_id = student.get("educations", [])[0].get("education_id", "")
        new_student = Student(name, education_id)
        result.add_student(new_student)

    return result


def get_schedule(token: str, student_id: str, day=None) -> Schedule:
    if day is None:
        day = date.today()
    start_time = datetime.combine(day, time.min)
    finish_time = datetime.combine(day, time.max)

    response = requests.get(
        schedule_url(),
        params={
            "p_educations[]": student_id,
            "p_datetime_from": datetime.strftime(start_time, "%d.%m.%Y %H:%M:%S"),
            "p_datetime_to": datetime.strftime(finish_time, "%d.%m.%Y %H:%M:%S"),
        },
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()

    result = Schedule()
    try:
        api_lessons = response.json().get("data", {}).get("items", [])
    except (Exception,):
        logger.exception(
            f"Не удалось разобрать тело ответа", extra={"body": response.text}
        )
        raise

    for lesson in api_lessons:
        template = "%d.%m.%Y %H:%M:%S"
        time_from = datetime.strptime(lesson["datetime_from"], template).time()
        time_to = datetime.strptime(lesson["datetime_to"], template).time()
        result.lessons.append(
            PlannedLesson(lesson["number"], lesson["subject_name"], time_from, time_to),
        )

    result.lessons.sort()
    return result


def get_marks(token: str, student_id: str, day=None):
    if day is None:
        day = date.today()
    start_time = datetime.combine(day, time.min)
    finish_time = datetime.combine(day, time.max)

    response = requests.get(
        journal_url(),
        params={
            "p_educations[]": student_id,
            "p_datetime_from": datetime.strftime(start_time, "%d.%m.%Y %H:%M:%S"),
            "p_datetime_to": datetime.strftime(finish_time, "%d.%m.%Y %H:%M:%S"),
        },
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()

    result = Journal()

    try:
        api_journal = response.json().get("data", {}).get("items", [])
    except (Exception,):
        logger.exception(
            f"Не удалось разобрать тело ответа", extra={"body": response.text}
        )
        raise

    for item in api_journal:
        for rec in item.get("estimates", []):
            record = Record(
                rec.get("estimate_type_code"),
                rec.get("estimate_type_name"),
                rec.get("estimate_value_code"),
                rec.get("estimate_value_name"),
                rec.get("estimate_comment"),
            )
            result.add(item.get("subject_name"), record)

    return result


def refresh_token(token: str):
    response = requests.post(
        refresh_url(),
        params={},
        data={"grant_type": "refresh_token", "refresh_token": token},
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()

    try:
        api_refresh = response.json().get["refresh_token"]
    except (Exception,):
        logger.exception(
            f"Не удалось разобрать тело ответа", extra={"body": response.text}
        )
        raise

    return api_refresh
