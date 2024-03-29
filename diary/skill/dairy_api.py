# mypy: ignore-errors

import os
from datetime import date, datetime, time, timedelta

import requests

from diary import context as app_context
from diary.logger_factory import LoggerFactory

from .constants.exceptions import NeedAuth
from .dataclasses import (
    Homework,
    Journal,
    PlannedLesson,
    Record,
    Schedule,
    Student,
    Students,
)

logger = LoggerFactory.get_logger(__name__)
# region URLs


def base_url():
    url = os.environ.get("DIARY_URL", "https://journal.bpo.edu.n3demo.ru/api/journal")
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


def permissions_url():
    return f"{base_url()}/user/permission/get"


# endregion


@app_context.perfmon
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


@app_context.perfmon
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


@app_context.perfmon
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


@app_context.perfmon
def get_homework(token, student_id: str, day=None) -> Homework:
    if day is None:
        day = date.today()
    start_time = datetime.combine(day - timedelta(days=7), time.min)
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

    result = Homework()

    try:
        api_homework = response.json().get("data", {}).get("items", [])
    except (Exception,):
        logger.exception(
            f"Не удалось разобрать тело ответа", extra={"body": response.text}
        )
        raise

    for item in api_homework:
        for task in item.get("tasks", []):
            if task["task_kind_code"] == "homework":
                result.add(
                    item.get("datetime_from"),
                    item.get("subject_name"),
                    task["task_name"],
                )

    return result


@app_context.perfmon
def get_permissions(token: str) -> None:
    response = requests.get(
        permissions_url(),
        cookies={"X-JWT-Token": token},
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )

    if response.status_code == 401:
        raise NeedAuth()
    return None


@app_context.perfmon
def refresh_token(token: str):

    if app_context.auth_service is not None:
        return app_context.auth_service.refresh_token()

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
