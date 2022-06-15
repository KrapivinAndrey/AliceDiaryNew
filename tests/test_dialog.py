import pytest
import datetime
from alicefluentcheck import AliceAnswer, AliceEntity, AliceIntent, AliceRequest

import skill.main as main
import skill.texts as texts
from skill.scenes import SCENES
import skill.constants.states as states
from tests.mocking import (
    setup_mock_children,
    setup_mock_schedule_no_auth,
    setup_mock_schedule_auth,
    setup_mock_schedule_with_params,
    setup_mock_journal,
    setup_mock_journal_with_params,
)


class TestHello:
    # Тесты начала диалога
    def test_start_dialog(self, start_skill):
        result = AliceAnswer(main.handler(start_skill))
        assert result.text == texts.need_auth("Welcome")[0]

    def test_start_dialog_auth(self, start_skill_auth, students_dump, requests_mock):
        setup_mock_children(requests_mock)
        setup_mock_journal(requests_mock)
        result = AliceAnswer(main.handler(start_skill_auth))
        assert "Изобразительное искусство. Работа на уроке 5" in result.text
        assert result.user_state["students"] == students_dump


class Goodbye:
    @pytest.mark.parametrize("scene_id", SCENES)
    def test_goodbye(self, scene_id):
        intent = AliceIntent("exit")
        test = (
            AliceRequest()
            .command("До свидания")
            .from_scene(scene_id)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.goodbye()[0]
        assert result.is_end_of_session


class TestFallback:
    # Реакция на неизвестные/ошибочные команды
    @pytest.mark.parametrize("scene_id", SCENES)
    def test_first_fallback(self, scene_id):
        test = (
            AliceRequest().command("рамамба хару мамбуру").from_scene(scene_id).build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.fallback()[0]
        assert not result.is_end_of_session

    @pytest.mark.parametrize("scene_id", SCENES)
    def test_second_fallback(self, scene_id):
        test = (
            AliceRequest()
            .command("рамамба хару мамбуру")
            .from_scene(scene_id)
            .add_to_state_session("fallback", True)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.sorry_and_goodbye()[0]
        assert result.is_end_of_session


class TestHelp:
    # Вызов помощи
    @pytest.mark.parametrize("scene_id", SCENES)
    def test_what_can_i_do(self, scene_id):
        test = (
            AliceRequest()
            .command("Что ты умеешь")
            .from_scene(scene_id)
            .add_intent(AliceIntent().what_can_you_do())
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.what_can_i_do()[0]
        assert result.has_button("Да")
        assert result.has_button("Нет")

    @pytest.mark.parametrize("scene_id", SCENES)
    def test_helpme(self, scene_id):
        test = (
            AliceRequest()
            .command("Па-ма-ги-тееее!")
            .from_scene(scene_id)
            .add_intent(AliceIntent().help())
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.help_menu_start()[0]
        assert len(result.response.get("buttons")) == 2


class TestSchedule:
    # проверим только один раз Глобально
    @pytest.mark.parametrize("scene_id", SCENES)
    def test_wrong_student(self, scene_id, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", num=1)
        fio = AliceEntity().fio(first_name="Георгий")
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Расписание на завтра для Гоши")
            .from_scene(scene_id)
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_entity(fio)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.unknown_student()[0]

    def test_name_of_student(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="1", num=3)
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="100", num=0)

        fio = AliceEntity().fio(first_name="алиса").tokens(4, 5)
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Расписание уроков для Алисы")
            .from_scene("Welcome")
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_entity(fio)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert "Алиса. 6 уроков" in result.text
        assert "Дмитрий. 6 уроков" not in result.text

        # в ттс дополнительная информация
        assert "К третьему уроку в 09:45" in result.tts
        assert "Уроки закончатся в 14:40" in result.tts
        assert "Информатика 2 урока" in result.tts

    def test_synonym_of_student(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="100", num=3)
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="1", num=0)

        fio = AliceEntity().fio(first_name="дима").tokens(4, 5)
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Расписание уроков у Димы")
            .from_scene("Welcome")
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_entity(fio)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert "Дмитрий. 6 уроков" in result.text

    def test_all_students(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", num=1)
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Расписание на завтра")
            .from_scene("Welcome")
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert "Алиса. 6 уроков" in result.text
        assert "Дмитрий. 6 уроков" in result.text
        for i in range(1, 9):
            assert f"К {i} уроку" not in result.text

    def test_no_schedule(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", num=0)
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Расписание на завтра")
            .from_scene("Welcome")
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert (
            "Расписание уроков. Сегодня\n"
            "Алиса. Нет уроков.\n"
            "Дмитрий. Нет уроков." == result.text
        )

    def test_what_lesson_both(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="1", num=1)
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="100", num=3)

        intent = AliceIntent("what_lesson_num")

        num = AliceEntity().number(4)
        req_date = AliceEntity().datetime(day=1, month=1, year=2021)

        test = (
            AliceRequest()
            .command("Какой урок 4 01.01.2021")
            .from_scene("Welcome")
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_entity(num)
            .add_entity(req_date)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert (
            "1 Января. 4 урок:\n"
            "Алиса - Информатика: 12:31 - 12:55\n"
            "Дмитрий - Информатика: 12:31 - 12:55" == result.text
        )

    def test_what_lesson_one(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="1", num=1)
        setup_mock_schedule_with_params(requests_mock, token="111", edu_id="100", num=0)

        intent = AliceIntent("what_lesson_num")

        num = AliceEntity().number(4)
        req_date = AliceEntity().datetime(day=1, month=1, year=2021)

        test = (
            AliceRequest()
            .command("Какой урок четвертый 01.01.2021")
            .from_scene("Welcome")
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_entity(num)
            .add_entity(req_date)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert (
            "1 Января. 4 урок:\n"
            "Алиса - Информатика: 12:31 - 12:55\n"
            "Дмитрий. Нет урока." == result.text
        )


class TestNeedAuthForScene:
    # Запрос конкретного расписания -> Авторизация -> Возврат в ту же сцену
    def test_scene_need_auth_return(self, students_dump, requests_mock):
        setup_mock_schedule_no_auth(requests_mock)

        fio = AliceEntity().fio(first_name="алиса").tokens(5, 6)
        req_date = AliceEntity().datetime(day=1, month=1, year=2021)
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Какие уроки будут у Алисы 01.01.2021")
            .add_to_state_user("students", students_dump)
            .add_entity(fio)
            .add_entity(req_date)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))

        assert "Сеанс устарел" in result.text
        assert result.get_state_session(states.INTENTS) is not None
        assert result.get_state_session(states.ENTITIES) is not None

        requests_mock.reset_mock()
        setup_mock_schedule_auth(requests_mock)

        test = (
            AliceRequest()
            .command("")
            .account_linking_complete()
            .access_token("222")
            .from_scene("GetSchedule")
            .add_to_state_session(
                states.INTENTS, result.get_state_session(states.INTENTS)
            )
            .add_to_state_session(
                states.ENTITIES, result.get_state_session(states.ENTITIES)
            )
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert "Сеанс устарел" not in result.text
        assert "Алиса. 6 уроков" in result.text


class TestIssue:
    # Тесты на всякие найденные баги

    def test_say_alice_first(self, students_dump, requests_mock):
        setup_mock_schedule_with_params(
            requests_mock,
            edu_id="100",
            ask_day=datetime.datetime(2021, 1, 1),
            token="222",
            num=1,
        )

        say_alice = AliceEntity().fio(first_name="алиса").tokens(0, 1)
        fio = AliceEntity().fio(first_name="дмитрий").tokens(4, 5)
        req_date = AliceEntity().datetime(day=1, month=1, year=2021)
        intent = AliceIntent("get_schedule")
        test = (
            AliceRequest()
            .command("Алиса какие занятия у Дмитрия 01.01.2021")
            .access_token("222")
            .add_to_state_user("students", students_dump)
            .add_entity(say_alice)
            .add_entity(fio)
            .add_entity(req_date)
            .add_intent(intent)
            .build()
        )

        result = AliceAnswer(main.handler(test))
        assert "Дмитрий. 6 уроков" in result.text


class TestMarks:
    @pytest.mark.parametrize("scene_id", SCENES)
    def test_wrong_student(self, scene_id, students_dump, requests_mock):
        setup_mock_journal_with_params(requests_mock, token="111")
        fio = AliceEntity().fio(first_name="Георгий")
        intent = AliceIntent("get_journal")
        test = (
            AliceRequest()
            .command("Какие оценки у Гоши")
            .from_scene(scene_id)
            .access_token("111")
            .add_to_state_user("students", students_dump)
            .add_entity(fio)
            .add_intent(intent)
            .build()
        )
        result = AliceAnswer(main.handler(test))
        assert result.text == texts.unknown_student()[0]
