import skill.dairy_api as dairy_api
from skill.tools.mocking import setup_mock_children, setup_mock_schedule


def test_get_url():
    assert dairy_api.base_url()


def test_get_students(requests_mock, students_dump):
    setup_mock_children(requests_mock)
    students = dairy_api.get_students("111")
    assert students.dump() == students_dump


def test_get_schedule(requests_mock):
    setup_mock_schedule(requests_mock)
    schedule = dairy_api.get_schedule("111", "111")

    assert len(schedule.lessons) == 6
    assert str(schedule.lessons[0]) == "Алгебра"
