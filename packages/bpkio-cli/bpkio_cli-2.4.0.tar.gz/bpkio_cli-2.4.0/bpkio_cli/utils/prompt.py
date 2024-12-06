from typing import Optional

import click
from InquirerPy import inquirer
from InquirerPy.base.control import (
    Choice,  # necessary to allow import from other modules
)
from InquirerPy.utils import get_style, patched_print


def select_markers(level: Optional[int] = None):
    standard_markers = markers(level)
    standard_markers["pointer"] = _indent("> ", level + 1 if level else 1)
    standard_markers["marker_pl"] = _indent("◯ ", level)
    standard_markers["marker"] = _indent("◉ ", level)

    return standard_markers


def markers(level: Optional[int] = None):
    return {
        "qmark": _indent("❔", level),
        "amark": _indent("➡️", level),
    }


def _indent(s: str, level: Optional[int] = None):
    if not level:
        level = 0

    return "  " * level + s


# Keybindings


def _add_keybindings_instructions(delete=False, skip_all=False, **kwargs):
    keys = {}

    if delete:
        keys["d"] = "delete the selected value"
    if skip_all:
        keys["ctrl-s"] = "skip all prompts, using last or default value"

    if keys:
        existing_instructions = kwargs.pop("long_instruction", "")
        out = ""
        if existing_instructions:
            out += f"{existing_instructions}\n\n"
        if keys:
            out += "Keyboard: \n"
            out += "\n".join([f" - '{k}' = {v}" for k, v in keys.items()])

        kwargs["long_instruction"] = out

    return kwargs


def _add_keybindings(inquirer_object, delete=None, skip=False):
    if delete:
        fn = delete

        @inquirer_object.register_kb("d")
        def _handle_delete(event):
            selected_value = inquirer_object.result_value
            result = fn(selected_value)
            event.app.exit(result=result)

    if skip:

        @inquirer_object.register_kb("c-s")
        def _handle_skip_all(event):
            obj = click.get_current_context().obj
            obj.config.set_temporary("use_prompts", False)

            try:
                # For prompt objects that allow selections
                selected_value = inquirer_object.result_value
                click.secho(selected_value, fg="bright_blue")
                event.app.exit(result=selected_value)
            except:
                event.app.exit(result="")

    return inquirer_object


# Shortcut methods
def _normalize_question_prompt(
    **kwargs,
):
    msg = kwargs["message"].strip()
    if not msg.endswith(("?", ":")):
        msg += ":"

    kwargs["message"] = msg
    return kwargs


def confirm(*args, **kwargs):
    return inquirer.confirm(
        *args, **kwargs, style=get_style(inquirer_styles, style_override=False)
    ).execute()


def secret(*args, **kwargs):
    _normalize_question_prompt(**kwargs)
    return inquirer.secret(
        *args, **kwargs, style=get_style({"long_instruction": "yellow"})
    ).execute()


def text(*args, level=0, keybinding_skip_all_prompts=False, **kwargs):
    kwargs = _normalize_question_prompt(**kwargs)
    kwargs = _add_keybindings_instructions(
        skip_all=keybinding_skip_all_prompts, **kwargs
    )

    p = inquirer.text(
        *args,
        **kwargs,
        style=get_style(inquirer_styles, style_override=False),
        **markers(level),
    )

    return p.execute()


def number(*args, level=0, **kwargs):
    kwargs = _normalize_question_prompt(**kwargs)

    p = inquirer.number(
        *args,
        **kwargs,
        style=get_style(inquirer_styles, style_override=False),
        **markers(level),
    )

    return p.execute()


def select(
    *args,
    level=0,
    keybinding_delete=False,
    keybinding_skip_all_prompts=False,
    **kwargs,
):
    kwargs = _normalize_question_prompt(**kwargs)
    kwargs = _add_keybindings_instructions(
        delete=keybinding_delete, skip_all=keybinding_skip_all_prompts, **kwargs
    )

    p = inquirer.select(
        *args,
        **kwargs,
        style=get_style(inquirer_styles, style_override=False),
        border=True,
        **select_markers(level),
    )

    _add_keybindings(p, delete=keybinding_delete, skip=keybinding_skip_all_prompts)

    return p.execute()


def fuzzy(
    *args,
    level=0,
    **kwargs,
):
    kwargs = _normalize_question_prompt(**kwargs)
    return inquirer.fuzzy(
        *args,
        **kwargs,
        style=get_style(inquirer_styles, style_override=False),
        border=True,
        **select_markers(level),
    ).execute()


def fuzzy_build_list(
    *args,
    level=0,
    **kwargs,
):
    kwargs = _normalize_question_prompt(**kwargs)

    selected = []

    p = inquirer.fuzzy(
        *args,
        **kwargs,
        style=get_style(inquirer_styles, style_override=False),
        long_instruction="Press `space` to add the selected item to the list. Press `enter` to stop adding.",
        border=True,
        transformer=lambda x: f"{len(selected)} assets",
        **select_markers(level),
    )

    @p.register_kb("space")
    def _handle_add(event):
        selected_value = p.result_value
        if p.result_value is None:
            event.app.exit(result=None)
        else:
            selected.append(selected_value)
            patched_print(f" {len(selected)}. {p.result_name}")

    _ = p.execute()

    return selected


def checkbox(*args, **kwargs):
    return inquirer.checkbox(*args, **kwargs, style=get_style(inquirer_styles, style_override=False)).execute()

# Styles
inquirer_styles = {
    "questionmark": "#e5c07b bold",
    "answermark": "#e5c07b",
    "answer": "#61afef",
    "input": "#98c379",
    "question": "",
    "answered_question": "",
    "instruction": "#abb2bf",
    "long_instruction": "yellow",
    "pointer": "#61afef bold",
    "checkbox": "#98c379",
    "separator": "",
    "skipped": "#5c6370",
    "validator": "",
    "marker": "#e5c07b",
    "fuzzy_prompt": "#c678dd",
    "fuzzy_info": "#abb2bf",
    "fuzzy_border": "#4b5263",
    "fuzzy_match": "#c678dd",
    "spinner_pattern": "#e5c07b",
    "spinner_text": "",
}
