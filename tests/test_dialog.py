import pytest
from alicefluentcheck import AliceAnswer, AliceIntent, AliceRequest

import skill.main as main
import skill.texts as texts
from skill.scenes import SCENES
from skill.tools.mocking import setup_mock_children


class TestHello:
    # Тесты начала диалога
    def test_start_dialog(self, start_skill):
        result = AliceAnswer(main.handler(start_skill, None))
        assert result.text == texts.need_auth("Welcome")[0]

    def test_start_dialog_auth(self, start_skill_auth, students_dump, requests_mock):
        setup_mock_children(requests_mock)
        result = AliceAnswer(main.handler(start_skill_auth, None))
        assert result.text == texts.hello(None)[0]
        assert result.user_state["students"] == students_dump


class TestFallback:
    # Реакция на неизвестные/ошибочные команды
    @pytest.mark.parametrize("scene_id", SCENES)
    def test_first_fallback(self, scene_id):
        test = (
            AliceRequest().command("рамамба хару мамбуру").from_scene(scene_id).build()
        )
        result = AliceAnswer(main.handler(test, None))
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
        result = AliceAnswer(main.handler(test, None))
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
        result = AliceAnswer(main.handler(test, None))
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
        result = AliceAnswer(main.handler(test, None))
        assert result.text == texts.help_menu_start()[0]
        assert len(result.response.get("buttons")) == 2
