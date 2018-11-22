def element_has_css_class(element):
    return 'class' in element.attrs


def url_not_from_other_domain(url):
    if "http" in url:
        return False
    else:
        return True
