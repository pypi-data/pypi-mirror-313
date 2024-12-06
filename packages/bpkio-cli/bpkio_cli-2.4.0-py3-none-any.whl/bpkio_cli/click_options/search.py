import functools

import click
from bpkio_api.helpers.search import SearchMethod
from cloup import argument, option, option_group


def search_options(fn):
    @argument(
        "single_term",
        required=False,
        help="Search term (quickhand, for search through all fields, equivalent to `--for TEXT`)",
    )
    @option_group(
        "Search Options",
        option(
            "--for",
            "search_terms",
            multiple=True,
            required=False,
            default=(),
            help="Search term",
        ),
        option(
            "--in",
            "search_fields",
            multiple=True,
            required=False,
            default=(None,),
            help="Field in which to search for the term. Not specifying it will search all fields",
        ),
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def validate_search_options(single_term, search_terms, search_fields):
    # compile the search terms

    if single_term:
        # prepend the single term
        search_terms = (single_term,) + search_terms

    if len(search_terms) != len(search_fields):
        raise click.UsageError(
            "The number of search terms and search fields must match"
        )

    # create an array of tuples with (field, term)
    return [
        e
        for e in zip(
            search_terms, search_fields, [SearchMethod.STRING_SUB] * len(search_fields)
        )
    ]
