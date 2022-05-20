
from typing import Union

import pymorphy2

from skill.tools.synonym_names import find_synonym


class Student:
    def __init__(self, name=None, student_id=None):
        self.name = name
        self.id = str(student_id)
        self.inflect = {}
        if name is not None:
            morph = pymorphy2.MorphAnalyzer()
            parse_name = morph.parse(name)[0]

            self.inflect["родительный"] = parse_name.inflect({"sing", "gent"}).word
            self.inflect["дательный"] = parse_name.inflect({"sing", "datv"}).word

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name.lower() == other.lower()
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

    def __str__(self):
        return ", ".join([str(x) for x in self.students])

    def __repr__(self):
        return str(self)

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

    @property
    def ids(self):
        return [x for x in self.students.keys()]

    def by_name(self, search_name: str) -> Union[Student, None]:
        for name in self.students.values():
            if name == search_name or search_name in find_synonym(name):
                return name

        return None

    def name_by_id(self, search_id: str):
        return str(self.students[search_id])

    def to_list(self):
        return [x for x in self.students.values()]
