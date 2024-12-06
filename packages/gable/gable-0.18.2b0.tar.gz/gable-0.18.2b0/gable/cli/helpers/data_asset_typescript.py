import json
from typing import Optional, Tuple, Union

import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.data_asset import (
    gather_typescript_asset_data,
    get_relative_project_path,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.repo_interactions import get_pr_link
from gable.openapi import (
    CheckComplianceDataAssetsTypeScriptRequest,
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetResponse,
    ErrorResponse,
    ErrorResponseDeprecated,
    IngestDataAssetResponse,
)
from gable.openapi import Library as TypeScriptLibrary
from gable.openapi import (
    RegisterDataAssetTypeScriptRequest,
    ResponseType,
    TypeScriptAsset,
)
from loguru import logger


def register_typescript_data_assets(
    ctx: ClickContext,
    library: Optional[str],
    project_root: str,
    emitter_file_path: Optional[str],
    emitter_function: Optional[str],
    emitter_payload_parameter: Optional[str],
    emitter_name_parameter: Optional[str],
    event_name_key: Optional[str],
    dry_run: bool,
) -> Tuple[Union[IngestDataAssetResponse, ErrorResponseDeprecated], bool, int]:
    git_ssh_repo, sca_results_dict = gather_typescript_asset_data(
        library,
        project_root,
        emitter_file_path,
        emitter_function,
        emitter_payload_parameter,
        emitter_name_parameter,
        event_name_key,
        ctx.obj.client,
    )
    if sca_results_dict is {}:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
        )
    logger.info(
        f"{EMOJI.GREEN_CHECK.value} TypeScript data asset(s) found:\n{json.dumps(sca_results_dict, indent=4)}"
    )

    lib: TypeScriptLibrary = (
        TypeScriptLibrary[library] if library else TypeScriptLibrary.udf
    )

    _, relative_typescript_project_root = get_relative_project_path(project_root)
    assets = [
        TypeScriptAsset(
            schema=event_schema,
            event_name=event_name,
            git_host=git_ssh_repo,
            library=lib,
            project_root=relative_typescript_project_root,
        )
        for event_name, event_schema in sca_results_dict.items()
    ]
    if dry_run:
        logger.info("Dry run mode. Data asset registration not performed.")
        return (
            IngestDataAssetResponse(message="", registered=[], success=True),
            True,
            200,
        )
    else:
        request = RegisterDataAssetTypeScriptRequest(
            assets=assets,
            dry_run=dry_run,
            prLink=get_pr_link(),
        )
        # click doesn't let us specify the type of ctx.obj.client in the Context:
        client: GableAPIClient = ctx.obj.client
        return client.post_data_asset_register_typescript(request)


def check_compliance_typescript_data_asset(
    ctx: ClickContext,
    library: Optional[str],
    project_root: str,
    emitter_file_path: Optional[str],
    emitter_function: Optional[str],
    emitter_payload_parameter: Optional[str],
    emitter_name_parameter: Optional[str],
    event_name_key: Optional[str],
    response_type: ResponseType,
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[CheckDataAssetResponse],
]:
    git_ssh_repo, sca_results_dict = gather_typescript_asset_data(
        library,
        project_root,
        emitter_file_path,
        emitter_function,
        emitter_payload_parameter,
        emitter_name_parameter,
        event_name_key,
        ctx.obj.client,
    )
    if sca_results_dict is {}:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to check! You can use the --debug or --trace flags for more details.",
        )
    lib: TypeScriptLibrary = (
        TypeScriptLibrary[library] if library else TypeScriptLibrary.udf
    )
    _, relative_typescript_project_root = get_relative_project_path(project_root)
    assets = [
        TypeScriptAsset(
            schema=event_schema,
            event_name=event_name,
            git_host=git_ssh_repo,
            library=lib,
            project_root=relative_typescript_project_root,
        )
        for event_name, event_schema in sca_results_dict.items()
    ]
    request = CheckComplianceDataAssetsTypeScriptRequest(
        assets=assets,
        responseType=response_type,
        prLink=get_pr_link(),
    )
    # click doesn't let us specify the type of ctx.obj.client in the Context:
    client: GableAPIClient = ctx.obj.client
    return client.post_check_compliance_data_assets_typescript(request)
