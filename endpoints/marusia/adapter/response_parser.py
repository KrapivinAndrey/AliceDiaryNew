from ..models.response_model import (
    Button,
    Model,
    Response,
    SessionStateUpdate,
    UserStateUpdate,
)


def parse(event: dict) -> Model:

    version = "1.0"
    response = parse_response(event)
    user_state_update = parse_user_state_update(event)
    session_state = parse_session_state(event)

    result = Model(
        version=version,
        session=None,
        response=response,
        user_state_update=user_state_update,
        session_state=session_state,
    )

    return result


def parse_response(event: dict) -> Response:

    result = Response()
    result.text = event["response"]["text"]
    result.tts = event["response"].get("tts", None)
    result.end_session = event["response"].get("end_session", False)

    # buttons

    buttons_data = event["response"].get("buttons", [])
    for button_data in buttons_data:
        button = Button(title=button_data["title"])
        result.buttons.append(button)

    return result


def parse_user_state_update(event: dict) -> UserStateUpdate:
    value = event.get("user_state_update", None)
    if value is not None:
        user_state_update = UserStateUpdate.parse_obj(value)
    else:
        user_state_update = None
    return user_state_update


def parse_session_state(event: dict) -> SessionStateUpdate:
    value = event.get("session_state", None)
    if value is not None:
        session_state = SessionStateUpdate.parse_obj(value)
    else:
        session_state = None
    return session_state
