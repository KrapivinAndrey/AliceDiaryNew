import base64

from ...skill.main import get_perfmon
from ...skill.main import handler as main_handler
from ...skill.main import set_config
from .adapter import MarusiaAdapter
from .models import ValidationError, request_model


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
    set_config({"auth_service": adapter, "perfmon": True})

    event_alice = adapter.parse_request(marusia_request)
    alice_result = main_handler(event_alice)

    get_perfmon().print_report()
    marusia_response = adapter.parse_response(alice_result)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": marusia_response.json(exclude_none=True),
    }
