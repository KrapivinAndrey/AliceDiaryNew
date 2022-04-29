import os
from datetime import date, datetime, time
from typing import List

import requests

from skill.dataclasses import PlannedLesson, Student, Students


class NotFoundError(Exception):
    pass


class NeedAuth(Exception):
    pass


def base_url():
    url = os.environ.get("DIARY_URL", "https://journal.bpo.edu.n3demo.ru/api/journal")
    assert url, "Не заполнен url для запросов"

    return url
