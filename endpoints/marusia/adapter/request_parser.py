from ..models.request_model import Model


def parse(data: Model) -> dict:

    meta = parse_meta(data)
    request = parse_request(data)
    session = parse_session(data)
    state = parse_state(data)

    event = {
        "meta": meta,
        "state": state,
        "request": request,
        "session": session,
        "version": "1.0",
    }

    # хз чё это но в коде так надо, в доке алисы нету такого свойства
    # event.setdefault("account_linking_complete_event", "")

    return event


def parse_meta(data: Model) -> dict:
    # TODO если если есть особенности
    result = data.meta.dict(exclude_none=True)
    return result


def parse_state(data: Model) -> dict:
    # TODO если если есть особенности
    result = data.state.dict(exclude_none=True)
    result.setdefault("session", {})
    result.setdefault("user", {})
    result.setdefault("application", {})
    return result


def parse_request(data: Model) -> dict:
    # TODO если если есть особенности
    result = data.request.dict(exclude_none=True)
    return result


def parse_session(data: Model) -> dict:
    result = data.session.dict(exclude_none=True)
    if data.state.user.auth_token:
        # закидываем auth_token из состояния в access_token сессии
        if result.get("user") is None:
            result["user"] = {}
        result["user"].setdefault("access_token", data.state.user.auth_token)
    return result
