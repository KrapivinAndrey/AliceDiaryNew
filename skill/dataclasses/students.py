class Student:
    def __init__(self, name: str, id: str):
        import pymorphy2
        import locale

        locale.setlocale(locale.LC_TIME, ("RU", "UTF8"))  # the ru locale is installed
        morph = pymorphy2.MorphAnalyzer()
        parse_name = morph.parse(name)[0]

        self.name = name
        self.id = id
        self.inflect = {}

        self.inflect["родительный"] = parse_name.inflect({"sing", "gent"}).word
        self.inflect["дательный"] = parse_name.inflect({"sing", "datv"}).word

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Student):
            return self.name == other.name and self.id == other.id

        raise Exception("Сравнивать можно только со Student или Строкой")

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(f"{self.name}-{self.id}")

    def dump(self):
        result = {"name": self.name, "id": self.id}
        return result


class Students:
    def __init__(self):
        pass
