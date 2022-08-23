from typing import ItemsView, List


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
        self.is_legal_skip = type_code == "30000" and value_code in ("494", "496")
        self.is_illegal_skip = type_code == "30000" and value_code not in ("494", "496")

        self.work = type_name
        self.value = value_name
        self.value_type = value_code
        self.comment = "" if comment is None else comment

    def __str__(self):
        if self.is_late:
            return "Опоздание"

        if self.is_legal_skip:
            return "Пропуск"

        if self.is_illegal_skip:
            return "Прогул"

        result = [self.work, self.value, self.comment]

        return " ".join(result).strip()

    def __repr__(self):
        return str(self)

    @property
    def mark(self) -> str:
        if self.is_late or self.is_illegal_skip or self.is_legal_skip:
            return str(self)
        elif self.value_type[-2:] == "/5":
            return self.value
        elif "/" in self.value_type:
            return f"{self.value} из {self.value[:self.value_type.find('/')+1:]}"
        else:
            return self.value_type


class Journal:
    # Это журнал оценок. Хранит данные по урокам
    def __init__(self):
        self.__journal = {}

    def add(self, lesson: str, rec: Record):
        self.__journal.setdefault(lesson, []).append(rec)

    @property
    def len(self) -> int:
        return len(self.__journal)

    @property
    def records(self) -> ItemsView[str, List[Record]]:
        return self.__journal.items()

    def __str__(self) -> str:
        result = []
        for lesson, records in self.__journal.items():
            result.append(f"{lesson}: {', '.join([str(x) for x in records])}")

        return "\n".join(result)

    def __repr__(self) -> str:
        return str(self)
