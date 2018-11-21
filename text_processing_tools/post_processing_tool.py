import bs4

def contents_to_plain_text(contents):
    without_tags = list(filter(lambda x: type(x) is bs4.element.NavigableString, contents))
    without_tags = list(map(lambda x: str(x), without_tags))
    without_tags = list(filter(lambda x: x != '\n', without_tags))
    return "".join(without_tags)
