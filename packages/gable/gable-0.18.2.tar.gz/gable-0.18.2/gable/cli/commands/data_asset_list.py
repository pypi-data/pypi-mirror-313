import json

import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.options import global_options
from loguru import logger
from rich.console import Console
from rich.table import Table

console = Console()


@click.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="list",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Format of the output. Options are: table (default) or json",
)
@click.option(
    "--full",
    is_flag=True,
    help="Return full data asset details including domain and path",
)
@global_options()
@click.pass_context
def list_data_assets(ctx: ClickContext, output: str, full: bool) -> None:
    """List all data assets"""
    # Get the data
    client: GableAPIClient = ctx.obj.client
    response, success, status_code = client.get_data_assets()
    if isinstance(response, dict):
        data_assets = response.get(
            "data", []
        )  # assets inside object when paginated request
    else:
        data_assets = response
    if not data_assets:
        raise click.ClickException("No data assets found.")

    # Format the output
    if output == "json":
        data_asset_list = []
        for data_asset in data_assets:
            domain: str = data_asset.get("namespace") or data_asset.get("domain")
            path: str = data_asset.get("name") or data_asset.get("path")
            row = {"resourceName": f"{domain}:{path}"}
            if full:
                # Filter out invalid data assets...
                if "://" in domain:
                    row["type"] = domain.split("://", 1)[0]
                    row["dataSource"] = domain.split("://", 1)[1]
                    row["path"] = path
            data_asset_list.append(row)
        logger.info(json.dumps(data_asset_list))
    else:
        table = Table(show_header=True, title="Data Assets")
        table.add_column("resourceName")
        if full:
            table.add_column("type")
            table.add_column("dataSource")
            table.add_column("path")
        for data_asset in data_assets:
            domain: str = data_asset.get("namespace") or data_asset.get("domain")
            path: str = data_asset.get("name") or data_asset.get("path")
            if not full:
                table.add_row(f"{domain}:{path}")
            else:
                # Filter out invalid data assets...
                if "://" in domain:
                    table.add_row(
                        f"{domain}:{path}",
                        domain.split("://", 1)[0],
                        domain.split("://", 1)[1],
                        path,
                    )
        console.print(table)
