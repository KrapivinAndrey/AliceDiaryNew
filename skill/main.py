import logging
import os
import sys

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from skill.alice import Request
from skill.constants.intents import GET_SCHEDULE
from skill.constants.states import PREVIOUS_MOVES
from skill.scenes import DEFAULT_SCENE, SCENES

logging.basicConfig()

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)

root_handler = logging.getLogger().handlers[0]
root_handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(name)s\t%(message)s\n"))


def handler(event, context):

    # если контекст пустой - это отладка или тесты
    if context is not None:
        sentry_logging = LoggingIntegration(
            level=logging.INFO, event_level=logging.WARN
        )
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_DSN"),
            integrations=[sentry_logging],
            environment=os.environ.get("ENVIRONMENT", "TEST"),
        )

    request = Request(event)

    current_scene_id = get_id_scene(request)
    logging.info(f"Current scene: {current_scene_id}")
    logging.debug(f"Current event: {event}")
    moves = request.session.get(PREVIOUS_MOVES, [])
    try:

        if current_scene_id is None:
            return DEFAULT_SCENE().reply(request)

        current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
        next_scene = current_scene.move(request)

        if next_scene is not None:
            logging.info(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
            return next_scene.reply(request)
        else:
            logging.warning(
                f"Не смогли обработать запрос {request.command}. Сцена: {current_scene.id()}",
                extra={"moves": moves, "alice_request": event},
            )
            return current_scene.fallback(request)

    except Exception as e:
        logging.exception(
            e,
            extra={"moves": moves, "alice_request": event},
        )
        message = SCENES.get("HaveMistake")()
        return message.reply(request)


def get_id_scene(request: Request):
    res = request.session.get("scene")
    if res is None and GET_SCHEDULE in request.intents:
        res = "get_schedule"

    return res
