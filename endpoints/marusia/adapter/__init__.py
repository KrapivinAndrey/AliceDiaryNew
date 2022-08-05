from ..models import RequestModel, ResponseModel, ResponseButton


class MarusiaAdapter:
    def __init__(self) -> None:
        self._last_request = None
        self._last_response = None
        pass

    def event(self, data: RequestModel):
        self._last_request = data
        return {}

    def response(self, data) -> ResponseModel:
        resp = ResponseModel(session=self._last_request.session)
        resp.response.text = data["response"]["text"]
        resp.response.tts = data["response"]["tts"]
        for button_data in data["response"]["buttons"]:
            button = ResponseButton(title=button_data["title"])
            resp.response.buttons.append(button)
        # TODO сессии
        self._last_response = resp
        return self._last_response
