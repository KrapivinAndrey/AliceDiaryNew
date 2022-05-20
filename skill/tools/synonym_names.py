import os
from typing import List


def find_synonym(name: str) -> List[str]:
    if not isinstance(name, str):
        name = str(name)
    with open(
        os.path.abspath("./skill/tools/synonym_names.txt"), "r", encoding="utf-8"
    ) as f:
        for line in f:
            if line.startswith(name):
                result = [
                    x.strip().lower()
                    for x in line.strip().split(" - ")[1].split(",")
                ]
                return result

    return []
