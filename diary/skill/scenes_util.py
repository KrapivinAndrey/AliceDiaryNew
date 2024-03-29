import json
from abc import ABC, abstractmethod
from typing import Optional

from diary.logger_factory import LoggerFactory

from ..skill.alice import Request
from ..skill.constants.states import PERMANENT_VALUES, PREVIOUS_MOVES, StateResponseKey


class Scene(ABC):
    @classmethod
    def id(cls):
        return cls.__name__

    """Генерация ответа сцены"""

    @abstractmethod
    def reply(self, request):
        raise NotImplementedError()

    """Проверка перехода к новой сцене"""

    def move(self, request: Request):
        if request.authorization_complete:
            return self
        else:
            next_scene = self.handle_local_intents(request)
            if next_scene is None:
                next_scene = self.handle_global_intents(request)
        return next_scene

    @abstractmethod
    def handle_global_intents(self, request):
        raise NotImplementedError()

    @abstractmethod
    def handle_local_intents(self, request: Request) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def fallback(self, request: Request):
        raise NotImplementedError()

    def make_response(
        self,
        request: Request,
        text,
        tts=None,
        card=None,
        state=None,
        user_state=None,
        application_state=None,
        buttons=None,
        directives=None,
        end_session=False,
    ):
        response = {
            "text": text[:1024],
            "tts": tts[:1024] if tts is not None else text[:1024],
        }
        if card:
            response["card"] = card
        if buttons:
            response["buttons"] = buttons
        if directives is not None:
            response["directives"] = directives
        if end_session:
            response["end_session"] = end_session

        webhook_response: dict = {
            "response": response,
            "version": "1.0",
            StateResponseKey.SESSION: {
                "scene": self.id(),
            },
        }

        for key, value in request.session.items():
            if key in PERMANENT_VALUES:
                webhook_response[StateResponseKey.SESSION][key] = value
        if state is not None:
            webhook_response[StateResponseKey.SESSION].update(state)
        if user_state is not None:
            webhook_response[StateResponseKey.USER] = user_state
        if application_state is not None:
            webhook_response[StateResponseKey.APPLICATION] = application_state

        prev_moves = request.session.get(PREVIOUS_MOVES, [])
        prev_moves.append(request.command)
        webhook_response[StateResponseKey.SESSION][PREVIOUS_MOVES] = prev_moves[-10:]
        logger = LoggerFactory.get_logger(__name__)
        logger.debug(f"RESPONSE {json.dumps(webhook_response, ensure_ascii=False)}")

        return webhook_response
