import locale

import pymorphy2


class Student:
    def __init__(self):
        self.name = None
        self.id = None
        self.inflect = {}

    def create(self, name: str, id: str):

        self.name = name
        self.id = id

        locale.setlocale(locale.LC_TIME, ("RU", "UTF8"))  # the ru locale is installed
        morph = pymorphy2.MorphAnalyzer()
        parse_name = morph.parse(name)[0]

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
        result = {"name": self.name, "id": self.id, "inflect": self.inflect}
        return result

    def restore(self, dump):
        self.name = dump["name"]
        self.id = dump["id"]
        for k, v in dump["inflect"].items():
            self.inflect[k] = v


class Students:
    def __init__(self):
        self.students = {}

    def add_student(self, student: Student):
        self.students[student.id] = student

    def dump(self):
        return [x.dump() for x in self.students.values()]

    def restore(self, dump):
        self.students = {}
        for x in dump:
            new_student = Student()
            new_student.restore(x)
            self.add_student(new_student)
