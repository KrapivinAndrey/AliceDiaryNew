from typing import List


def find_synonym(name: str) -> List[str]:
    if not isinstance(name, str):
        name = str(name)
    # TODO тут нужна оптимизация, функция вызывается в больше 1 раза
    # не нужно каждый раз читать файл
    # вообще со всеми файлами можно так сделать
    with open("diary/skill/tools/synonym_names.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(name):
                result = [
                    x.strip().lower() for x in line.strip().split(" - ")[1].split(",")
                ]
                return result
    return []
