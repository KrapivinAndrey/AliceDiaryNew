def reset_settings():

    with open(
        "diary/skill/files/grammars/reset_settings.grammar", "r", encoding="utf-8"
    ) as f:
        data = f.readlines()
    return parseGrammar(data)


def help():
    with open("diary/skill/files/grammars/help.grammar", "r", encoding="utf-8") as f:
        data = f.readlines()
    return parseGrammar(data)


def whatCanYouDo():
    with open(
        "diary/skill/files/grammars/what_can_you_do.grammar", "r", encoding="utf-8"
    ) as f:
        data = f.readlines()
    return parseGrammar(data)


def parseGrammar(data):
    result = []
    for i in range(len(data)):
        if data[i].find("root") > -1:
            root = data[i + 1].split()
            data.pop(i + 1)
            break

    for word in root:
        for i in range(len(data)):
            if data[i].find(word) > -1:
                word_list = [x.strip() for x in data[i + 2].split("|")]
                result.append(word_list)
                break
    return result


if __name__ == "__main__":
    reset_settings()
