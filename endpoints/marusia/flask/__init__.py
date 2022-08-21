from flask import Flask, request
from flask_cors import CORS

from skill.main import handler, set_config, get_perfmon

from ..adapter import MarusiaAdapter
from ..models import ValidationError, request_model

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_marusia():
    return "<p>Hello, Marusia!</p>"


@app.route("/marusia", methods=["POST"])
def marusia_202208():

    try:
        marusia_request = request_model.Model.parse_raw(request.data)
    except ValidationError as e:
        print(e.json())
        return e.json(), 400

    adapter = MarusiaAdapter()
    set_config({"auth_service": adapter, "perfmon": True})

    event = adapter.parse_request(marusia_request)
    event_result = handler(event)

    get_perfmon().print_report()

    marusia_response = adapter.parse_response(event_result)
    return marusia_response.json(exclude_none=True), 200
