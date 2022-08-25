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

# Сохраняем токен авторизации для автообновления
AUTH_TOKEN = "auth_token"

# Сохраняем сущности для авторизации
ENTITIES = "save_entities"
INTENTS = "save_intents"

# Ученики
STUDENTS = "students"

# Текст и произношение для команды Повтори
SAVE_TEXT = "save_text"
SAVE_TTS = "save_tts"

# help menu
PREVIOUS_STATE = "previous_state"
NEXT_BUTTON = "next_button"

# Эти состояния будут сохранены в fallback
MUST_BE_SAVE = {PREVIOUS_STATE, NEXT_BUTTON}

# Эти состояния сохраняются на каждый ход
PERMANENT_VALUES = {STUDENTS}
