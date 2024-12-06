import json
from typing import List
from urllib.parse import quote

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.commands.asset_plugins.kotlin import KotlinAssetPlugin
from gable.cli.commands.asset_plugins.typescript import TypescriptAssetPlugin
from gable.cli.helpers.data_asset import darn_to_string
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.repo_interactions import get_pr_link
from gable.cli.helpers.shell_output import shell_linkify_if_not_in_ci
from gable.cli.options import global_options
from gable.openapi import (
    ErrorResponse,
    RegisterDataAssetsRequest,
    ResolvedDataAsset,
    SourceType,
)
from loguru import logger

asset_plugins: List[AssetPluginAbstract] = [
    TypescriptAssetPlugin(),
    KotlinAssetPlugin(),
]


def extracted_asset_to_register_asset_request(
    source_type: SourceType,
    extracted_assets: List[ExtractedAsset],
) -> RegisterDataAssetsRequest:
    return RegisterDataAssetsRequest(
        assets=[
            ResolvedDataAsset(
                source_type=source_type,
                data_asset_resource_name=asset.darn,
                schema={
                    "type": "struct",
                    "fields": asset.fields,
                },
            )
            for asset in extracted_assets
        ],
        prLink=get_pr_link(),
    )


def generic_register_implementation(asset_plugin: AssetPluginAbstract):
    @click.command(
        name=asset_plugin.source_type(),
        help=f"Register a new {asset_plugin.source_type()} data asset",
        short_help=f"Register a new {asset_plugin.source_type()} data asset",
    )
    @global_options()
    @click.pass_context
    @asset_plugin.click_options_decorator()
    def implementation(ctx: click.Context, *args, **kwargs):
        total_assets = 0
        registered_assets = 0
        try:
            allowed_args = set(asset_plugin.click_options_keys())
            received_args = set(kwargs.keys())
            if not received_args.issubset(allowed_args):
                raise ValueError(f"Extra fields found: {received_args - allowed_args}")

            asset_plugin.pre_validation(kwargs)
            extracted_assets = asset_plugin.extract_assets(ctx.obj.client, kwargs)
            if not extracted_assets:
                raise click.ClickException(
                    f"Error registering data assets: No data assets found to register! You can use the --debug or --trace flags for more details."
                )
            click.echo(
                f"Found {len(extracted_assets)} {asset_plugin.source_type()} data asset(s):"
            )
            for asset in extracted_assets:
                darn_str = darn_to_string(asset.darn)
                click.echo(f"- {darn_str}")
                logger.trace(
                    f"- {darn_str} schema: {json.dumps([field.json() for field in asset.fields], indent=2)}"
                )

            total_assets = len(extracted_assets)
            register_asset_request = extracted_asset_to_register_asset_request(
                asset_plugin.source_type(), extracted_assets
            )
            client: GableAPIClient = ctx.obj.client

            response = client.post_register_data_assets(register_asset_request)

            if isinstance(response, ErrorResponse):
                raise click.ClickException(
                    f"Error registering data assets: {response.title}: {response.message}"
                )
            for assetOutcome in response.asset_registration_outcomes:
                if assetOutcome.error:
                    click.echo(
                        f"{EMOJI.RED_X.value} Error registering data asset {darn_to_string(assetOutcome.data_asset_resource_name)}: {assetOutcome.error}"
                    )
                else:
                    darn_string = darn_to_string(assetOutcome.data_asset_resource_name)
                    maybe_linkified_darn = shell_linkify_if_not_in_ci(
                        f"{client.ui_endpoint}/assets/{quote(darn_string, safe='')}",
                        darn_string,
                    )
                    registered_assets += 1
                    click.echo(
                        f"{EMOJI.GREEN_CHECK.value} Data asset {maybe_linkified_darn} registered successfully"
                    )
            if registered_assets > 0:
                click.echo(
                    f"{registered_assets}/{total_assets} assets registered successfully"
                )

            if asset_plugin.checked_when_registered():
                pass  # TODO once implementing assets that get checked on register
        except Exception as e:
            raise click.ClickException(f"{EMOJI.RED_X.value} {str(e)}")

    return implementation
