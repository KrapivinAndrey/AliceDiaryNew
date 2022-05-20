from skill.tools.synonym_names import find_synonym


def test_synonym_exists():
    test_name = "Вадим"
    result = find_synonym(test_name)
    check = "Вадимка, Дима, Вадя, Вадиша, Вадюша".split(", ")
    assert result == check


def test_synonym_not_exists():
    test_name = "Арчибальд"
    result = find_synonym(test_name)
    check = []
    assert result == check
