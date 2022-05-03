import pytest
from alicefluentcheck import AliceAnswer, AliceRequest, AliceIntent

import skill.main as main
import skill.texts as texts
from skill.scenes import SCENES


class TestHello:
    # Тесты начала диалога
    def test_start_dialog(self, start_skill):
        result = AliceAnswer(main.handler(start_skill, None))
        assert result.text == "Здесь будет todo"


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
            .add_to_state_session("fallback", True)
            .build()
        )
        result = AliceAnswer(main.handler(test, None))
        assert result.text == texts.what_can_i_do()[0]
        assert len(result.response.get("buttons")) == 2
