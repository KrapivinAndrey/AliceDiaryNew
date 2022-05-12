STATE_REQUEST_KEY = "session"


class StateResponseKey:
    SESSION = "session_state"
    USER = "user_state_update"
    APPLICATION = "application_state"


# Отладочная информация
# Последние фразы пользователя
PREVIOUS_MOVES = "prev_moves"

# Признак уточнения после того, как не смогли разобрать фразу.
# Если снова не разобрали - выходим
NEED_FALLBACK = "fallback"

# Сохраняем сущности для авторизации
ENTITIES = "save_entities"
INTENTS = "save_intents"

STUDENTS = "students"

# help menu
PREVIOUS_STATE = "previous_state"
NEXT_BUTTON = "next_button"

# Эти состояния будут сохранены в fallback
MUST_BE_SAVE = {PREVIOUS_STATE, NEXT_BUTTON}

# Эти состояния сохраняются на каждый ход
PERMANENT_VALUES = {STUDENTS}
