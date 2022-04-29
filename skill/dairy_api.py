import os
from datetime import date, datetime, time
from typing import List, Dict

import requests

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

def get_schedule_on_date(token: str, ids: List[str], day=None) -> Dict[Student, List[PlannedLesson]]:
    if day is None:
        day = date.today()

    start_time = datetime.combine(day, time.min)
    finish_time = datetime.combine(day, time.max)

    response = requests.get(
        schedule_url(),
        params={
            "p_educations[]": ",".join(ids),
            "p_datetime_from": datetime.strftime(start_time, "%d.%m.%Y %H:%M:%S"),
            "p_datetime_to": datetime.strftime(finish_time, "%d.%m.%Y %H:%M:%S"),
        },
        cookies={"X-JWT-Token": token},
    )