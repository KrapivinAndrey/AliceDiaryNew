import skill.dairy_api as dairy_api
from tests.mocking import (
    setup_mock_children,
    setup_mock_schedule_with_params,
    setup_mock_journal_with_params,
)


def test_get_url():
    assert dairy_api.base_url()


def test_get_students(requests_mock, students_dump):
    #setup_mock_children(requests_mock)
    students = dairy_api.get_students("111")
    assert students.dump() == students_dump


def test_get_schedule(requests_mock):
    setup_mock_schedule_with_params(requests_mock, token="111", num=1)
    schedule = dairy_api.get_schedule("111", "111")

    assert len(schedule.lessons) == 6
    assert str(schedule.lessons[0]) == "Алгебра"


def test_get_journal(requests_mock):
    setup_mock_journal_with_params(requests_mock, edu_id="111", token="111")
    journal = dairy_api.get_marks("111", "111")

    assert journal.len == 4


def test_get_journal_empty(requests_mock):
    setup_mock_journal_with_params(requests_mock, edu_id="111", token="111", empty=True)
    journal = dairy_api.get_marks("111", "111")

    assert journal.len == 0
