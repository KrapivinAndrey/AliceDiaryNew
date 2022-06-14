class Record:
    def __init__(
        self,
        type_code: str,
        type_name: str,
        value_code: str,
        value_name: str,
        comment=None,
    ):
        self.is_late = type_code == "30000" and not value_code
        self.is_legal_skip = type_code == "30000" and value_code != "493"
        self.is_illegal_skip = type_code == "30000" and value_code == "493"

        self.work = type_name
        self.mark = value_name
        self.mark_type = value_code
        self.comment = comment

    def __str__(self):
        if self.is_late:
            return "Опоздание"

        if self.is_legal_skip:
            return "Пропуск"

        if self.is_illegal_skip:
            return "Прогул"

        result = [self.work, self.mark, self.comment]

        return " ".join(result)

    def __repr__(self):
        return str(self)


class Journal:
    # Это журнал оценок. Хранит данные по урокам
    def __init__(self):
        self.__journal = {}

    def add(self, lesson: str, rec: Record):
        self.__journal.setdefault(lesson, []).append(rec)

    def __str__(self):
        result = []
        for lesson, record in self.__journal.values():
            result.append(f"{lesson} {str(record)}")

        return '\n'.join(result)

    def __repr__(self):
        return str(self)
