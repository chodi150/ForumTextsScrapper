def date_after_ref(ref_date, date):
    if ref_date is None:
        return True
    if date is None:
        return False
    return date > ref_date


def date_before_ref(ref_date,date):
    if ref_date is None:
        return True
    if date is None:
        return False
    return date < ref_date


def is_keyword_in_string(keywords, content):
    if keywords is None:
        return True
    if content is None:
        return False
    for keyword in keywords:
        if keyword in content:
            return True
    return False
