from requests_mock import Mocker

from skill.dairy_api import schedule_url, students_url

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


def setup_mock_children(m: Mocker):
    m.get(f"{students_url()}", json=json_students())


def setup_mock_schedule(m: Mocker, from_first_lesson=True):
    if from_first_lesson:
        m.get(
            f"{schedule_url()}",
            request_headers={"Cookie": "X-JWT-Token=111"},
            json=json_schedule_from_first_lesson(),
        )
    else:
        m.get(
            f"{schedule_url()}",
            request_headers={"Cookie": "X-JWT-Token=111"},
            json=json_schedule_from_third_lesson(),
        )


def setup_mock_schedule_reauth(m: Mocker):
    m.get(
        f"{schedule_url()}/?p_educations%5B%5D=453000&p_datetime_from=01.01.2021+00%3A00%3A00&p_datetime_to=01.01.2021+23%3A59%3A59",
        request_headers={"Cookie": "X-JWT-Token=222"},
        text="work",
        status_code=200,
    )

    m.get(f"{students_url()}", json=json_students())

    m.get(
        f"{schedule_url()}",
        text="Need authenticate",
        status_code=403,
    )

