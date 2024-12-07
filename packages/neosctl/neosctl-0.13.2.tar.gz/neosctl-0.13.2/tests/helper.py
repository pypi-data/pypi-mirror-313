from __future__ import annotations

from neosctl.util import dumps_formatted_json


def render_cmd_output(payload: dict | list[dict], *, sort_keys: bool = True):
    return f"{dumps_formatted_json(payload, sort_keys=sort_keys)}\n\n"
