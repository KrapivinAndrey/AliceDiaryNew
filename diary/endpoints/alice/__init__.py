from ...skill.main import handler as main_handler


def handler(event, context=None):
    return main_handler(event, context)
