from flask import Flask, request

from ..models import RequestModel, ResponseModel, ValidationError

app = Flask(__name__)


@app.route("/")
def hello_marusia():
    return "<p>Hello, Marusia!</p>"


@app.route("/marusia/202208", methods=["POST"])
def marusia_202208():

    try:
        request_data = RequestModel.parse_raw(request.data)
    except ValidationError as e:
        print(e.json())
        return e.json(), 400

    response_data = ResponseModel(session=request_data.session)
    response_data.response.text = "понг"

    return response_data.json(), 200
