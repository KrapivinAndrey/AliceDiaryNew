from diary import context as app_context
from diary.logger_factory import LoggerFactory
from diary.skill.alice import Request
from diary.skill.constants.states import PREVIOUS_MOVES
from diary.skill.scenes import DEFAULT_SCENE, SCENES, global_scene_from_request

from .tools.perfmon import PerfMonitor

logger = LoggerFactory.get_logger(__name__)


@app_context.perfmon
def handler(event, context=None):

    request = Request(event)

    current_scene_id = get_id_scene(request)
    logger.info(f"Current scene: {current_scene_id}")
    logger.debug(f"Current event: {event}")
    moves = request.session.get(PREVIOUS_MOVES, [])
    try:

        if current_scene_id is None:
            return DEFAULT_SCENE().reply(request)

        current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
        next_scene = current_scene.move(request)

        if next_scene is not None:
            logger.info(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
            return next_scene.reply(request)
        else:
            logger.warning(
                f"Не смогли обработать запрос {request.command}. Сцена: {current_scene.id()}",
                extra={"moves": moves, "alice_request": event},
            )
            return current_scene.fallback(request)

    except Exception as e:
        logger.exception(
            e,
            extra={"moves": moves, "alice_request": event},
        )
        message = SCENES.get("HaveMistake")()
        return message.reply(request)


def get_id_scene(request: Request):
    res = request.session.get("scene")
    if res is None:
        res = global_scene_from_request(request)
        if res is not None:
            return res.id()

    return res


def set_config(config):
    app_context.auth_service = config.get("auth_service")
    if config.get("perfmon", False) is True:
        app_context.perf_monitor = PerfMonitor()


def get_perfmon():
    return app_context.perf_monitor
