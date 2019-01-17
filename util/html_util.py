from urllib.parse import urlparse


def element_has_css_class(element):
    return 'class' in element.attrs


def url_not_from_other_domain(url, base_domain):
    if "http" not in url:
        return True
    extracted_domain = urlparse(url)[1]
    extracted_base_domain = urlparse(base_domain)[1]
    return extracted_domain == extracted_base_domain


def build_link(domain, link):
    new_link = domain + link
    try:
        extracted_domain = urlparse(link)[1]
        extracted_base_domain = urlparse(domain)[1]
        if extracted_domain == extracted_base_domain:
            new_link = link
    except BaseException as e:
        pass

    return new_link


def is_url_valid(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False



