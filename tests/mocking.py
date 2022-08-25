from requests_mock import Mocker
from datetime import datetime
from diary.skill.dairy_api import schedule_url, students_url, journal_url

true = True
false = False
null = None


def json_students():
    return {
        "data": {
            "items": [
                {
                    "educations": [
                        {
                            "push_subscribe": False,
                            "education_id": 1,
                            "group_id": 273411,
                            "group_name": "7 д",
                            "institution_id": 236,
                            "institution_name": "Первая школа",
                            "jurisdiction_id": 19,
                            "jurisdiction_name": "Комитет по образованию",
                            "is_active": None,
                            "distance_education": None,
                            "distance_education_updated_at": None,
                            "parent_firstname": None,
                            "parent_surname": None,
                            "parent_middlename": None,
                            "parent_email": None,
                        }
                    ],
                    "action_payload": {
                        "can_apply_for_distance": True,
                        "can_print": None,
                    },
                    "identity": {"id": 1595357},
                    "firstname": "Алиса",
                    "surname": "Гребенщикова",
                    "middlename": "Борисовна",
                    "hash_uid": None,
                },
                {
                    "educations": [
                        {
                            "push_subscribe": False,
                            "education_id": 100,
                            "group_id": 273411,
                            "group_name": "7 д",
                            "institution_id": 236,
                            "institution_name": "Вторая школа",
                            "jurisdiction_id": 19,
                            "jurisdiction_name": "Комитет по образованию",
                            "is_active": None,
                            "distance_education": None,
                            "distance_education_updated_at": None,
                            "parent_firstname": None,
                            "parent_surname": None,
                            "parent_middlename": None,
                            "parent_email": None,
                        }
                    ],
                    "action_payload": {
                        "can_apply_for_distance": True,
                        "can_print": None,
                    },
                    "identity": {"id": 1595357},
                    "firstname": "Дмитрий",
                    "surname": "Менделеев",
                    "middlename": "Иванович",
                    "hash_uid": None,
                },
            ],
            "before": 1,
            "current": 1,
            "last": 1,
            "next": 1,
            "total_pages": 1,
            "total_items": 1,
        },
        "validations": [],
        "messages": [],
        "debug": [],
    }


def json_schedule_from_first_lesson():
    return {
        "data": {
            "items": [
                {
                    "number": 6,
                    "datetime_from": "25.04.2022 13:31:00",
                    "datetime_to": "25.04.2022 13:55:00",
                    "subject_id": 172516,
                    "subject_name": "География",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 5,
                    "datetime_from": "25.04.2022 14:31:00",
                    "datetime_to": "25.04.2022 14:40:00",
                    "subject_id": 172516,
                    "subject_name": "География",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 4,
                    "datetime_from": "25.04.2022 11:31:00",
                    "datetime_to": "25.04.2022 12:10:00",
                    "subject_id": 172533,
                    "subject_name": "Информатика",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 3,
                    "datetime_from": "25.04.2022 12:31:00",
                    "datetime_to": "25.04.2022 12:55:00",
                    "subject_id": 172533,
                    "subject_name": "Информатика",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 1,
                    "datetime_from": "25.04.2022 09:45:00",
                    "datetime_to": "25.04.2022 10:25:00",
                    "subject_id": 172476,
                    "subject_name": "Алгебра",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 2,
                    "datetime_from": "25.04.2022 10:31:00",
                    "datetime_to": "25.04.2022 11:10:00",
                    "subject_id": 172476,
                    "subject_name": "Алгебра",
                    "priority": 0,
                    "override_by_priority": true,
                },
            ],
            "before": 1,
            "current": 0,
            "last": 0,
            "next": 0,
            "total_pages": 0,
            "total_items": 0,
        },
        "validations": [],
        "messages": [],
        "debug": [],
    }


def json_schedule_from_third_lesson():
    return {
        "data": {
            "items": [
                {
                    "number": 7,
                    "datetime_from": "25.04.2022 13:31:00",
                    "datetime_to": "25.04.2022 13:55:00",
                    "subject_id": 172516,
                    "subject_name": "География",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 8,
                    "datetime_from": "25.04.2022 14:31:00",
                    "datetime_to": "25.04.2022 14:40:00",
                    "subject_id": 172516,
                    "subject_name": "География",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 5,
                    "datetime_from": "25.04.2022 11:31:00",
                    "datetime_to": "25.04.2022 12:10:00",
                    "subject_id": 172533,
                    "subject_name": "Информатика",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 6,
                    "datetime_from": "25.04.2022 12:31:00",
                    "datetime_to": "25.04.2022 12:55:00",
                    "subject_id": 172533,
                    "subject_name": "Информатика",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 3,
                    "datetime_from": "25.04.2022 09:45:00",
                    "datetime_to": "25.04.2022 10:25:00",
                    "subject_id": 172476,
                    "subject_name": "Алгебра",
                    "priority": 0,
                    "override_by_priority": true,
                },
                {
                    "number": 4,
                    "datetime_from": "25.04.2022 10:31:00",
                    "datetime_to": "25.04.2022 11:10:00",
                    "subject_id": 172476,
                    "subject_name": "Алгебра",
                    "priority": 0,
                    "override_by_priority": true,
                },
            ],
            "before": 1,
            "current": 0,
            "last": 0,
            "next": 0,
            "total_pages": 0,
            "total_items": 0,
        },
        "validations": [],
        "messages": [],
        "debug": [],
    }


def json_empty():
    return {
        "data": {
            "items": [],
            "before": 1,
            "current": 0,
            "last": 0,
            "next": 0,
            "total_pages": 0,
            "total_items": 0,
        },
        "validations": [],
        "messages": [],
        "debug": [],
    }


def json_journal():
    return {
        "data": {
            "items": [
                {
                    "identity": {"id": 105078234, "uid": null},
                    "number": 7,
                    "datetime_from": "11.04.2022 14:20:00",
                    "datetime_to": "11.04.2022 15:05:00",
                    "subject_id": 76413,
                    "subject_name": "Иностранный язык (английский)",
                    "content_name": "УУД и речевые умения",
                    "content_description": null,
                    "content_additional_material": null,
                    "tasks": [
                        {
                            "task_name": "с.100 у.1,2.",
                            "task_code": null,
                            "task_kind_code": "homework",
                            "task_kind_name": "Домашнее задание",
                            "files": [],
                        }
                    ],
                    "estimates": [],
                    "action_payload": {"can_add_homework": true},
                },
                {
                    "identity": {"id": 105078251, "uid": null},
                    "number": 6,
                    "datetime_from": "11.04.2022 13:25:00",
                    "datetime_to": "11.04.2022 14:10:00",
                    "subject_id": 76414,
                    "subject_name": "Второй иностранный язык (испанский)",
                    "content_name": "Вводное аудирование и первичное закрепление лексики.",
                    "content_description": null,
                    "content_additional_material": null,
                    "tasks": [
                        {
                            "task_name": "РНО (письмо), стр. 65 - читать, работа со словарем",
                            "task_code": null,
                            "task_kind_code": "homework",
                            "task_kind_name": "Домашнее задание",
                            "files": [],
                        }
                    ],
                    "estimates": [],
                    "action_payload": {"can_add_homework": true},
                },
                {
                    "identity": {"id": 105054251, "uid": null},
                    "number": 5,
                    "datetime_from": "11.04.2022 12:30:00",
                    "datetime_to": "11.04.2022 13:15:00",
                    "subject_id": 75262,
                    "subject_name": "Изобразительное искусство",
                    "content_name": "Мода, культура и ты. Композиционно-конструктивные принципы дизайна одежды.",
                    "content_description": null,
                    "content_additional_material": null,
                    "tasks": [],
                    "estimates": [
                        {
                            "estimate_type_code": "1058",
                            "estimate_type_name": "Работа на уроке",
                            "estimate_value_code": "5/5",
                            "estimate_value_name": "5",
                            "estimate_comment": null,
                        }
                    ],
                    "action_payload": {"can_add_homework": true},
                },
                {
                    "identity": {"id": 105101864, "uid": null},
                    "number": 4,
                    "datetime_from": "11.04.2022 11:29:00",
                    "datetime_to": "11.04.2022 12:20:00",
                    "subject_id": 75249,
                    "subject_name": "Литература",
                    "content_name": "Д.С. Лихачев. Главы из книги «Земля родная» как духовное напутствие молодежи.",
                    "content_description": null,
                    "content_additional_material": null,
                    "tasks": [
                        {
                            "task_name": "Прочитать с.186-201, вопросы на с.201 (устно), рассказ о Яшке (подобрать цитаты).",
                            "task_code": null,
                            "task_kind_code": "homework",
                            "task_kind_name": "Домашнее задание",
                            "files": [],
                        }
                    ],
                    "estimates": [
                        {
                            "estimate_type_code": "1065",
                            "estimate_type_name": "Самостоятельная работа",
                            "estimate_value_code": "4/5",
                            "estimate_value_name": "4",
                            "estimate_comment": null,
                        }
                    ],
                    "action_payload": {"can_add_homework": true},
                },
                {
                    "identity": {"id": 105098782, "uid": null},
                    "number": 3,
                    "datetime_from": "11.04.2022 10:30:00",
                    "datetime_to": "11.04.2022 11:15:00",
                    "subject_id": 75247,
                    "subject_name": "Русский язык",
                    "content_name": "Подчинительные союзы.",
                    "content_description": null,
                    "content_additional_material": null,
                    "tasks": [
                        {
                            "task_name": "Упр. 382 (№1, 3: морфологический разбор союзов).",
                            "task_code": null,
                            "task_kind_code": "homework",
                            "task_kind_name": "Домашнее задание",
                            "files": [],
                        }
                    ],
                    "estimates": [
                        {
                            "estimate_type_code": "1058",
                            "estimate_type_name": "Работа на уроке",
                            "estimate_value_code": "4/5",
                            "estimate_value_name": "4",
                            "estimate_comment": null,
                        }
                    ],
                    "action_payload": {"can_add_homework": true},
                },
                {
                    "identity": {"id": 105078243, "uid": null},
                    "number": 2,
                    "datetime_from": "11.04.2022 09:25:00",
                    "datetime_to": "11.04.2022 10:10:00",
                    "subject_id": 75239,
                    "subject_name": "Алгебра",
                    "content_name": "Линейная функция и ее график.  Проверочная  работа.",
                    "content_description": null,
                    "content_additional_material": null,
                    "tasks": [
                        {
                            "task_name": "№627",
                            "task_code": null,
                            "task_kind_code": "homework",
                            "task_kind_name": "Домашнее задание",
                            "files": [],
                        }
                    ],
                    "estimates": [
                        {
                            "estimate_type_code": "30000",
                            "estimate_type_name": "Посещаемость",
                            "estimate_value_code": "496",
                            "estimate_value_name": "по болезни",
                            "estimate_comment": null,
                        },
                        {
                            "estimate_type_code": "1058",
                            "estimate_type_name": "Работа на уроке",
                            "estimate_value_code": "5/5",
                            "estimate_value_name": "5",
                            "estimate_comment": null,
                        },
                    ],
                    "action_payload": {"can_add_homework": true},
                },
            ],
            "before": 1,
            "current": 1,
            "last": 1,
            "next": 1,
            "total_pages": 1,
            "total_items": 6,
        },
        "validations": [],
        "messages": [],
        "debug": [],
    }


def setup_mock_children(m: Mocker):
    m.get(f"{students_url()}", json=json_students())


def setup_mock_schedule_no_auth(m: Mocker):
    setup_mock_schedule_with_params(
        m, edu_id="1", ask_day=datetime(2021, 1, 1), token="222", num=1
    )

    m.get(f"{students_url()}", json=json_students())

    m.get(
        f"{schedule_url()}",
        text="Need authenticate",
        status_code=403,
    )


def setup_mock_schedule_auth(m: Mocker):
    setup_mock_schedule_with_params(
        m, edu_id="1", ask_day=datetime(2021, 1, 1), token="222", num=1
    )

    m.get(f"{students_url()}", json=json_students())


def setup_mock_schedule_with_params(
    m: Mocker, *, edu_id=None, ask_day=None, token: str, num: int
):
    if num == 0:
        json = json_empty()
    elif num == 1:
        json = json_schedule_from_first_lesson()
    elif num == 3:
        json = json_schedule_from_third_lesson()

    headers = {}
    if token:
        headers = {"Cookie": f"X-JWT-Token={token}"}
    url = schedule_url()
    if edu_id is not None:
        url += f"?p_educations%5B%5D={edu_id}"
    if ask_day is not None:
        url += f"&p_datetime_from={datetime.strftime(ask_day, '%d.%m.%Y')}+00%3A00%3A00&p_datetime_to={datetime.strftime(ask_day, '%d.%m.%Y')}+23%3A59%3A59"

    m.get(
        url,
        request_headers=headers,
        json=json,
        status_code=200,
    )


def setup_mock_journal(m: Mocker):
    setup_mock_journal_with_params(m, token="")


def setup_mock_journal_with_params(
    m: Mocker, *, edu_id=None, ask_day=None, token: str, empty=False
):
    headers = {}
    if token:
        headers = {"Cookie": f"X-JWT-Token={token}"}
    url = journal_url()
    json = json_journal() if not empty else json_empty()
    if edu_id is not None:
        url += f"?p_educations%5B%5D={edu_id}"
    if ask_day is not None:
        url += f"&p_datetime_from={datetime.strftime(ask_day, '%d.%m.%Y')}+00%3A00%3A00&p_datetime_to={datetime.strftime(ask_day, '%d.%m.%Y')}+23%3A59%3A59"

    m.get(
        url,
        request_headers=headers,
        json=json,
        status_code=200,
    )
