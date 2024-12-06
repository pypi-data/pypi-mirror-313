from typing import Optional, Union, cast

import click
from click.core import Context as ClickContext
from gable.cli.helpers.check import post_data_assets_check_requests
from gable.cli.helpers.data_asset import (
    determine_should_block,
    format_check_data_assets_json_output,
    format_check_data_assets_text_output,
    gather_python_asset_data,
    get_schema_contents,
    get_source_names,
    is_empty_schema_contents,
)
from gable.cli.helpers.data_asset_pyspark import (
    check_compliance_pyspark_data_asset,
    read_config_file,
)
from gable.cli.helpers.data_asset_typescript import (
    check_compliance_typescript_data_asset,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.options import (
    file_source_type_options,
    global_options,
    proxy_database_options,
    pyspark_project_options,
    python_project_options,
    s3_project_options,
    typescript_project_options,
)
from gable.common_types import ALL_SOURCE_TYPES, FILE_SOURCE_TYPES, SCHEMA_SOURCE_TYPES
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetResponse,
    ErrorResponse,
    ResponseType,
    SourceType,
)
from loguru import logger


@click.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="check",
    epilog="""Example:

gable data-asset check --source-type protobuf --files ./**/*.proto""",
)
@click.option(
    "--source-type",
    required=True,
    type=click.Choice(
        [source_type.value for source_type in ALL_SOURCE_TYPES], case_sensitive=True
    ),
    help="""The type of data asset.
    
    For databases (postgres, mysql, mssql) the check will be performed for all tables within the database.

    For protobuf/avro/json_schema the check will be performed for all file(s)
    """,
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["text", "json", "markdown"]),
    default="text",
    help="Format of the output. Options are: text (default), json, or markdown which is intended to be used as a PR comment",
)
@proxy_database_options(
    option_group_help_text="""Options for checking contract compliance for tables in a relational database. The check will be performed
    for any tables that have a contract associated with them.
    
    Gable relies on having a proxy database that mirrors your production database, and will connect to the proxy database
    to perform the check in order to perform the check as part of the CI/CD process before potential changes in the PR are
    merged.
    """,
    action="check",
)
@file_source_type_options(
    option_group_help_text="""Options for checking Protobuf message(s), Avro record(s), or JSON schema object(s) for contract violations.""",
    action="check",
)
@python_project_options(
    option_group_help_text="""
    Options for checking contract compliance for assets emitted in Python project code. This set of options mirrors the registration options, and will
    perform a check for any assets that have a contract associated with them.
    """,
    action="check",
)
@typescript_project_options(
    option_group_help_text="""
    Options for verifying contract compliance for assets emitted from TypeScript project code. 
    These options reflect those available during asset registration and will perform validation 
    checks for any assets linked to an existing contract.
    """,
    action="check",
)
@pyspark_project_options(
    option_group_help_text="""
    Options for checking contract compliance of data assets from Pyspark tables. 

    When checking a Pyspark table, it's important to specify the project root and the entrypoint of the job. This allows Gable to correctly
    identify the project for analysis.

    The Pyspark project options include:
    - Specifying the project's entrypoint along with necessary arguments.
    - Identifying the path to the Python executable to be able to run the Pyspark script.
    """,
    action="check",
)
@s3_project_options(
    option_group_help_text="""
    Options for checking S3 contract compliance of s3 files from a bucket.

    When registering S3 files, it's important to specify the AWS bucket containing the files that are intended to be registered as data assets.
    Other options are:
    - S3 bucket name
    - The number of days to look back to expand the history depth of files to check (default is 0)
    - The list of prefixes to include in the check (default None to include everything)
    """,
    action="check",
)
@global_options()
@click.pass_context
def check_data_asset(
    ctx: ClickContext,
    source_type: SourceType,
    output: str,
    host: str,
    port: int,
    db: str,
    schema: str,
    table: str,
    proxy_host: str,
    proxy_port: int,
    proxy_db: str,
    proxy_schema: str,
    proxy_user: str,
    proxy_password: str,
    files: tuple,
    project_root: str,
    emitter_function: str,
    emitter_payload_parameter: str,
    emitter_name_parameter: str,
    event_name_key: str,
    emitter_file_path: str,
    library: Optional[str],
    spark_job_entrypoint: Optional[str],
    connection_string: Optional[str],
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    exclude: Optional[str],
    bucket: Optional[str],
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    lookback_days: int,
    history: Optional[bool],
    skip_profiling: bool,
    row_sample_count: int,
    recent_file_count: int,
    config_file: Optional[click.File],
    config_entrypoint_path: Optional[str],
    config_args_path: Optional[str],
) -> None:
    """Checks data asset(s) against a contract"""
    # Standardize the source type
    tables: Union[list[str], None] = (
        [t.strip() for t in table.split(",")] if table else None
    )
    response_type: ResponseType = (
        ResponseType.COMMENT_MARKDOWN if output == "markdown" else ResponseType.DETAILED
    )

    schema_contents = []
    source_names = []
    if source_type == SourceType.python:
        # Click options should enforce these being required, but to make pyright happy check anyways
        if (
            not project_root
            or not emitter_function
            or not emitter_payload_parameter
            or not emitter_file_path
            or not event_name_key
        ):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required options for Python project registration. You can use the --debug or --trace flags for more details."
            )
        source_names, schema_contents = gather_python_asset_data(
            project_root,
            emitter_file_path,
            emitter_function,
            emitter_payload_parameter,
            event_name_key,
            exclude,
            ctx.obj.client,
        )
        if is_empty_schema_contents(source_type, schema_contents):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to check! You can use the --debug or --trace flags for more details."
            )
        results = post_data_assets_check_requests(
            ctx.obj.client,
            response_type,
            source_type,
            source_names,
            db,
            schema,
            schema_contents,
        )
    elif source_type in SCHEMA_SOURCE_TYPES or source_type in FILE_SOURCE_TYPES:
        schema_contents = get_schema_contents(
            source_type=source_type,
            dbuser=proxy_user,
            dbpassword=proxy_password,
            db=proxy_db or db,
            dbhost=proxy_host,
            dbport=proxy_port,
            schema=proxy_schema or schema,
            tables=tables,
            files=[] if files is None else list(files),
        )
        source_names = get_source_names(
            ctx=ctx,
            source_type=source_type,
            dbhost=host,
            dbport=port,
            files=[] if files is None else list(files),
        )
        if is_empty_schema_contents(source_type, schema_contents):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to check! You can use the --debug or --trace flags for more details."
            )
        results = post_data_assets_check_requests(
            ctx.obj.client,
            response_type,
            source_type,
            source_names,
            db,
            schema,
            schema_contents,
        )
    elif source_type == SourceType.typescript:
        if not library and (
            not emitter_function
            or not emitter_payload_parameter
            or not emitter_file_path
            or (not event_name_key and not emitter_name_parameter)
        ):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required options for Typescript project registration. You can use the --help option for more details."
            )
        if not project_root:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required option '--project-root' for Typescript project registration. You can use the --debug or --trace flags for more details."
            )
        results = check_compliance_typescript_data_asset(
            ctx,
            library,
            project_root,
            emitter_file_path,
            emitter_function,
            emitter_payload_parameter,
            emitter_name_parameter,
            event_name_key,
            response_type,
        )
    elif source_type == SourceType.pyspark:
        if not project_root or not (connection_string or csv_schema_file):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required options for Spark project registration. You can use the --debug or --trace flags for more details."
            )
        if not spark_job_entrypoint:
            if not config_file or not config_entrypoint_path:
                raise click.ClickException(
                    f"{EMOJI.RED_X.value} Missing required options for Spark project registration: --config-entrypoint-path is required when using --config-file."
                )
            spark_job_entrypoint = read_config_file(
                config_file, config_entrypoint_path, config_args_path
            )
        results = check_compliance_pyspark_data_asset(
            ctx,
            spark_job_entrypoint,
            project_root,
            connection_string,
            csv_schema_file,
            csv_path_to_table_file,
            response_type,  # type: ignore
        )
    elif source_type == SourceType.s3:
        from gable.cli.helpers.data_asset_s3 import check_compliance_s3_data_assets
        from gable.cli.helpers.data_asset_s3 import validate_input as validate_s3_input

        validate_s3_input(
            "check", bucket, lookback_days, include_prefix, exclude_prefix, history
        )

        results = check_compliance_s3_data_assets(
            ctx,
            response_type,
            bucket,  # type: ignore (input validation ensures bucket is not None, this quashes linter)
            lookback_days,
            row_sample_count,
            recent_file_count,
            include_prefix,
            exclude_prefix,
            skip_profiling,
        )
    else:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Source type {source_type} is not supported."
        )

    format_compliance_check_response_for_cli(results, output)


def format_compliance_check_response_for_cli(results, output: str) -> None:
    if isinstance(results, ErrorResponse):
        raise click.ClickException(
            f"Error checking data asset(s): {results.title} ({results.id})\n\t{results.message}"
        )
    # If the output was text, or json
    if output == "text" or output == "json":
        # Cast to list of detailed responses
        results = cast(
            list[CheckDataAssetResponse],
            results,
        )
        # Determine if we should block (non-zero exit code) or not
        should_block = determine_should_block(results)
        if output == "text":
            # Format the results
            output_string = format_check_data_assets_text_output(results)
        else:
            output_string = format_check_data_assets_json_output(results)

        if should_block:
            logger.info(output_string)
            raise click.ClickException("Contract violation(s) found")
        else:
            logger.info(output_string)
    else:
        # If the output was markdown
        results = cast(CheckDataAssetCommentMarkdownResponse, results)
        # Only print the markdown if it's not None or empty, otherwise the stdout will contain a newline. Print markdown
        # to stdout, so we can read it separately from the error output to determine if we should comment on a PR
        if results.markdown and results.markdown != "":
            logger.info(results.markdown)
        # Decide if we should comment on or block the PR based on whether or not there were any contract violations, and the
        # enforcement level of the contacts that had the violations. In either case, write something to stderr so there's
        # a record logged in the CI/CD output
        if results.shouldBlock:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Contract violations found, maximum enforcement level was 'BLOCK'"
            )
        elif results.shouldAlert:
            logger.error(
                f"{EMOJI.YELLOW_WARNING.value} Contract violations found, maximum enforcement level was 'ALERT'"
            )
        # If there were errors
        if results.errors:
            errors_string = "\n".join([error.json() for error in results.errors])
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Contract checking failed for some data assets:\n{errors_string}"
            )
