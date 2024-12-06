import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def add_query_parameters_from_dict(url: str, new_params: dict):
    parsed_url = urlparse(url)

    # Parse the existing query parameters
    query_params = parse_qs(parsed_url.query)

    # Add the new query parameter
    for key, value in new_params.items():
        query_params[key] = value

    # Reconstruct the query string
    new_query = urlencode(query_params, doseq=True)

    # Reconstruct the full URL with the new query string
    new_url = urlunparse(parsed_url._replace(query=new_query))

    return new_url


def add_query_parameters_from_list(url: str, new_params: list):
    params_dict = {}
    for param in new_params:
        k, _, v = param.partition("=")
        params_dict[k] = v or None

    return add_query_parameters_from_dict(url, params_dict)


def validate_ipv4_or_domain(domain):
    # remove protocol if any
    domain = domain.split("://", 1)[-1]

    ipv4_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    domain_pattern = r"^([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}$"

    if re.match(ipv4_pattern, domain) or re.match(domain_pattern, domain):
        return True
    else:
        return False
