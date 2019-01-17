import bs4
from w3lib.html import remove_tags


def contents_to_plain_text(contents):
    without_tags = list(filter(lambda x: type(x) is bs4.element.NavigableString, contents))
    without_tags = list(map(lambda x: str(x), without_tags))
    without_tags = list(filter(lambda x: x != '\n', without_tags))
    effect =  "".join(without_tags)
    if effect != "":
        return effect

    return try_to_delete_only_tags(contents)


def try_to_delete_only_tags(contents):
    without = list(map(lambda x: str(x), contents))
    without = list(map(lambda x: remove_tags(x), without))
    without = list(filter(lambda x: x != '\n', without))
    return "".join(without)