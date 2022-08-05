from flask import Flask, request
from flask_cors import CORS


from ..models import RequestModel, ResponseModel, ValidationError
from ..adapter import MarusiaAdapter
from skill.main import handler

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_marusia():
    return "<p>Hello, Marusia!</p>"


@app.route("/marusia", methods=["POST"])
def marusia_202208() -> ResponseModel:

    try:
        marusia_request = RequestModel.parse_raw(request.data)
    except ValidationError as e:
        print(e.json())
        return e.json(), 400

    adapter = MarusiaAdapter()

    event = adapter.event(marusia_request)
    event_result = handler(event)

    marusia_response = adapter.response(event_result)
    return marusia_response.json(exclude_none=True), 200
