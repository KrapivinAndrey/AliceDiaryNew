from .alice import handler as alice_handler
from .marusia import handler as marusia_handler


def create_app():

    from flask import Flask, request
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def hello():
        return "<p>Hello!</p>"

    @app.route("/alice", methods=["POST"])
    def alice():
        event = {"body": request.data.decode("utf-8")}
        resp = alice_handler(event=event)
        return resp.get("body"), resp.get("statusCode")

    @app.route("/marusia", methods=["POST"])
    def marusia():
        event = {"body": request.data.decode("utf-8")}
        resp = marusia_handler(event=event)
        return resp.get("body"), resp.get("statusCode")

    return app


__all__ = ["alice_handler", "marusia_handler", "create_app"]
