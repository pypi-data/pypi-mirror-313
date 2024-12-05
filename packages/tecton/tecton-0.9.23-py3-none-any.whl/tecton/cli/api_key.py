import json
import sys

import click

from tecton.cli import printer
from tecton.cli.cli_utils import pprint_dict
from tecton.cli.command import TectonGroup
from tecton.identities import api_keys
from tecton_core.id_helper import IdHelper


@click.command("api-key", cls=TectonGroup)
def api_key():
    """Introspect API key. To create, delete, or list API keys see `tecton service-account` commands"""


def introspect(api_key):
    response = api_keys.introspect(api_key)
    if not response:
        printer.safe_print(
            "API key cannot be found. Ensure you have the correct API Key. The key's secret value is different from the key's ID.",
            file=sys.stderr,
        )
        sys.exit(1)
    return {
        "API Key ID": IdHelper.to_string(response.id),
        "Description": response.description,
        "Created by": response.created_by,
        "Active": response.active,
    }


@api_key.command("introspect")
@click.argument("api-key", required=True)
@click.option(
    "--json-output",
    is_flag=True,
    default=False,
    help="Whether the output is displayed in machine readable json format. Defaults to false.",
)
def introspect_command(api_key, json_output):
    """Introspect an API Key"""
    api_key_details = introspect(api_key)
    if json_output:
        for key in api_key_details.copy():
            snake_case = key.replace(" ", "_").lower()
            api_key_details[snake_case] = api_key_details.pop(key)
        printer.safe_print(f"{json.dumps(api_key_details)}")
    else:
        pprint_dict(api_key_details, colwidth=16)
