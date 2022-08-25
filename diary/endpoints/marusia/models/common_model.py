from typing import Any, Union

from pydantic import BaseModel

# не стал разбираться что относится к состоянию сессии, что к состоянию пользователя
# TODO разобраться и почистить модельки
# TODO выразить типы


class UserState(BaseModel):
    # эти точно тут
    students: Union[Any, None] = None
    auth_token: Union[str, None] = None
    # эти хз
    fallback: Union[Any, None] = None
    save_entities: Union[Any, None] = None
    save_intents: Union[Any, None] = None
    save_text: Union[Any, None] = None
    save_tts: Union[Any, None] = None
    previous_state: Union[Any, None] = None
    next_button: Union[Any, None] = None


class SessionState(BaseModel):
    # эти точно тут
    scene: Union[Any, None] = None
    prev_moves: Union[Any, None] = None
    # эти хз
    fallback: Union[Any, None] = None
    save_entities: Union[Any, None] = None
    save_intents: Union[Any, None] = None
    save_text: Union[Any, None] = None
    save_tts: Union[Any, None] = None
    previous_state: Union[Any, None] = None
    next_button: Union[Any, None] = None
