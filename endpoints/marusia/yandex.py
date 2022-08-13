import base64

from skill.main import handler as alice_handler

from .adapter import MarusiaAdapter
from .models import RequestModel, ValidationError


def handler(event, context=None):

    is_b64 = event.get("isBase64Encoded", False)
    if is_b64:
        body = base64.b64decode(event["body"])
    else:
        body = event["body"]

    try:
        marusia_request = RequestModel.parse_raw(body)
    except ValidationError as e:
        print(e.json())
        return e.json(), 400

    adapter = MarusiaAdapter()

    event_alice = adapter.event(marusia_request)
    alice_result = alice_handler(event_alice)

    marusia_response = adapter.response(alice_result)
    return {
        "statusCode": 200,
        "body": marusia_response.json(exclude_none=True),
    }
