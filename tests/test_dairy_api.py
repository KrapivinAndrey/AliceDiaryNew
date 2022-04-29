import skill.dairy_api as dairy_api
from skill.tools.mocking import setup_mock_children


def test_get_url():
    assert dairy_api.base_url()


def test_get_students(requests_mock, students_dump):
    setup_mock_children(requests_mock)
    students = dairy_api.get_students("111")
    assert students.dump() == students_dump
