import json
import os

from diary.skill import main

true = True
false = False

with open(
    os.path.dirname(__file__) + "\\emulate_response.json", encoding="utf8"
) as json_file:
    REQUEST = json.load(json_file)


def alice():
    main.handler(REQUEST, None)


if __name__ == "__main__":
    alice()
