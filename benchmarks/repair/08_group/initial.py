def group_by_initial(words: list[str]) -> dict[str, list[str]]:
    result = {}
    for word in words:
        result[word[0]] = [word]
    return result
