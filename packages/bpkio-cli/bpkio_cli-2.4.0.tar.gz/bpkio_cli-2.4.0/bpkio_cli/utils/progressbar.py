import click
from progressbar import ETA, Bar, Counter, Percentage, Variable


def widgets_slots(title):
    return [
        f"{title}: ",
        Counter(),
        " (",
        Variable(
            name="success",
            format=click.style("{formatted_value}", fg="green"),
            width=1,
        ),
        "/",
        Variable(
            name="error", format=click.style("{formatted_value}", fg="red"), width=1
        ),
        ") ",
        Bar(left="[", right="]"),
        " ",
        Percentage(),
        " - ",
        ETA(),
    ]
