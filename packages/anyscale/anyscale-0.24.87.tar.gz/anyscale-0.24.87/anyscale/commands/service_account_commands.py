from typing import Optional

import click

from anyscale.cli_logger import BlockLogger
from anyscale.controllers.service_account_controller import ServiceAccountController
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group(
    "service-account",
    short_help="Manage service accounts for your anyscale workloads.",
)
def service_account_cli() -> None:
    pass


@service_account_cli.command(name="create", help="Create a service account.")
@click.option(
    "--name", "-n", help="Name for the service account.", type=str, required=True
)
def create(name: str) -> None:
    ServiceAccountController().create_service_account(name)


@service_account_cli.command(
    name="create-api-key", help="Create a new API key for a service account."
)
@click.option(
    "--email", help="Email of the service account to create the new key for.", type=str
)
@click.option(
    "--name", help="Name of the service account to create the new key for.", type=str
)
def create_api_key(email: Optional[str], name: Optional[str]) -> None:
    ServiceAccountController().create_new_service_account_api_key(email, name)


@service_account_cli.command(name="list", help="List all service accounts.")
@click.option(
    "--max-items",
    required=False,
    default=20,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list_service_accounts(max_items: int) -> None:
    ServiceAccountController().list_service_accounts(max_items)


@service_account_cli.command(name="delete", help="Delete a service account.")
@click.option("--email", help="Email of the service account to delete.", type=str)
@click.option("--name", help="Name of the service account to delete.", type=str)
def delete(email: Optional[str], name: Optional[str]) -> None:
    ServiceAccountController().delete_service_account(email, name)


@service_account_cli.command(
    name="rotate-api-keys", help="Rotate all api keys of a service account."
)
@click.option(
    "--email", help="Rotate API keys for the service account with this email.", type=str
)
@click.option(
    "--name", help="Rotate API keys for the service account with this name.", type=str
)
def rotate_api_keys(email: Optional[str], name: Optional[str]) -> None:
    ServiceAccountController().rotate_service_account_api_keys(email, name)
