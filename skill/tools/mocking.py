from requests_mock import Mocker
from skill.dairy_api import students_url


def text_students():
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
                }
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


def setup_mock_children(m: Mocker):
    m.get(f"{students_url()}", json=text_students())
