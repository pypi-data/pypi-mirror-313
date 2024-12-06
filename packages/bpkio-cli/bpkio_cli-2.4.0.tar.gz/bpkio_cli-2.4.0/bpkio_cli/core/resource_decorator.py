from typing import List

import click


def add_category_info(slots: List | object):
    ctx = click.get_current_context()
    categories = ctx.obj.api.categories.list()

    if isinstance(slots, list):
        for slot in slots:
            add_category_info(slot)
    else:
        if slots.category and slots.category.id:
            try:
                slots.category = next(
                    c for c in categories if c.id == slots.category.id
                )
            except StopIteration:
                pass
        return slots
