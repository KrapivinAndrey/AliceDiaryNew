import base64

from skill.main import handler as alice_handler, set_config

from .adapter import MarusiaAdapter
from .models import request_model, ValidationError


def handler(event, context=None):

    is_b64 = event.get("isBase64Encoded", False)
    if is_b64:
        body = base64.b64decode(event["body"])
    else:
        body = event["body"]

    try:
        marusia_request = request_model.Model.parse_raw(body)
    except ValidationError as e:
        print(e.json())
        return e.json(), 400

    adapter = MarusiaAdapter()
    set_config({"auth_service": adapter})

    event_alice = adapter.parse_request(marusia_request)
    alice_result = alice_handler(event_alice)

    marusia_response = adapter.parse_response(alice_result)
    return {
        "statusCode": 200,
        "body": marusia_response.json(exclude_none=True),
    }
