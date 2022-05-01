STATE_REQUEST_KEY = "session"
STATE_RESPONSE_KEY = {
    "session": "session_state",
    "user": "user_state_update",
    "application": "application_state",
}

# Отладочная информация
# Последние фразы пользователя
PREVIOUS_MOVES = "prev_moves"

# признак уточнения после того, как не смогли разобрать фразу.
# Если снова не разобрали - выходим
NEED_FALLBACK = "fallback"


# region State of dialog

STUDENTS = "students"

# endregion

# help menu
PREVIOUS_STATE = "previous_state"
NEXT_BUTTON = "next_button"

# Эти состояния будут сохранены в fallback
MUST_BE_SAVE = {PREVIOUS_STATE, NEXT_BUTTON}

# Эти состояния сохраняются на каждый ход
PERMANENT_VALUES = {STUDENTS}
