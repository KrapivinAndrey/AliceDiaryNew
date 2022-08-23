from diary.skill.dataclasses.students import Student, Students


class TestStudent:
    def test_create(self, studentAlice):
        assert studentAlice.name == "Алиса"
        assert studentAlice.id == "1"

    def test_repr(self, studentAlice):
        assert str(studentAlice) == "Алиса"

    def test_inflect_woman(self, studentAlice):
        assert studentAlice.inflect["родительный"] == "алисы"
        assert studentAlice.inflect["дательный"] == "алисе"

    def test_inflect_man(self, studentDmitry):
        assert studentDmitry.inflect["родительный"] == "дмитрия"
        assert studentDmitry.inflect["дательный"] == "дмитрию"

    def test_compare(self, studentAlice, studentAnotherAlice):
        assert studentAlice == "Алиса"
        assert studentAlice != studentAnotherAlice

    def test_hash(self, studentAlice):
        assert isinstance(hash(studentAlice), int)

    def test_dump(self, studentAlice, student_dump):
        assert studentAlice.dump() == student_dump

    def test_restore(self, studentAlice, student_dump):
        test = Student()
        test.restore(student_dump)

        assert test == studentAlice


class TestStudents:
    def test_empty(self):
        test = Students()
        assert test.students == {}

    def test_create(self, students_Alice_and_Dmitry, studentAlice):
        assert len(students_Alice_and_Dmitry.students) == 2
        assert students_Alice_and_Dmitry.students["1"] == studentAlice

    def test_dump(self, students_Alice_and_Dmitry, students_dump):
        assert students_Alice_and_Dmitry.dump() == students_dump

    def test_restore(self, students_dump, studentAlice):
        test = Students()
        test.restore(students_dump)
        assert len(test.students) == 2
        assert test.students["1"] == studentAlice

    def test_ids(self, students_Alice_and_Dmitry):
        assert students_Alice_and_Dmitry.ids == ["1", "100"]

    def test_search_name(self, students_Alice_and_Dmitry, studentAlice):
        assert students_Alice_and_Dmitry.by_name("Алиса") == studentAlice
        assert students_Alice_and_Dmitry.by_name("Гриша") is None
