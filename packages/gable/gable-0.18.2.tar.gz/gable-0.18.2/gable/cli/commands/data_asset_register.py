from typing import List, Optional, Union
from urllib.parse import quote

import click
from click.core import Context as ClickContext
from gable.cli.client import GableAPIClient
from gable.cli.commands.data_asset_check import format_compliance_check_response_for_cli
from gable.cli.helpers.data_asset import (
    gather_python_asset_data,
    get_abs_project_root_path,
    get_schema_contents,
    get_source_names,
    is_empty_schema_contents,
)
from gable.cli.helpers.data_asset_pyspark import (
    read_config_file,
    register_pyspark_data_assets,
)
from gable.cli.helpers.data_asset_typescript import register_typescript_data_assets
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.repo_interactions import get_pr_link
from gable.cli.helpers.shell_output import shell_linkify_if_not_in_ci
from gable.cli.helpers.util import chunk_list
from gable.cli.options import (
    file_source_type_options,
    global_options,
    proxy_database_options,
    pyspark_project_options,
    python_project_options,
    required_option_callback,
    s3_project_options,
    typescript_project_options,
)
from gable.common_types import (
    ALL_SOURCE_TYPES,
    DATABASE_SOURCE_TYPES,
    SCHEMA_SOURCE_TYPES,
    STATIC_CODE_ANALYSIS_SOURCE_TYPES,
)
from gable.openapi import SourceType
from loguru import logger

DATA_ASSET_REGISTER_CHUNK_SIZE = 20


@click.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="register",
    epilog="""Example:

gable data-asset register --source-type postgres \\
    --host prod.pg.db.host --port 5432 --db transit --schema public --table routes \\
    --proxy-host localhost --proxy-port 5432 --proxy-user root --proxy-password password""",
)
@click.option(
    "--source-type",
    callback=required_option_callback,
    is_eager=True,
    type=click.Choice(
        [source_type.value for source_type in ALL_SOURCE_TYPES], case_sensitive=True
    ),
    help="""The type of data asset.
    
    For databases (postgres, mysql, mssql) a data asset is a table within the database.

    For protobuf/avro/json_schema a data asset is message/record/schema within a file.
    """,
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Perform a dry run without actually registering the data asset.",
    default=False,
)
@proxy_database_options(
    option_group_help_text="""Options for registering database tables as data assets. Gable relies on having a proxy database that mirrors your 
    production database, and will connect to the proxy database to register tables as data assets. This is to ensure that 
    Gable does not have access to your production data, or impact the performance of your production database in any way. 
    The proxy database can be a local Docker container, a Docker container that is spun up in your CI/CD workflow, or a
    database instance in a test/staging environment. The tables in the proxy database must have the same schema as your 
    production database for all tables to be correctly registered. The proxy database must be accessible from the 
    machine that you are running the gable CLI from.

    If you're registering tables in your CI/CD workflow, it's important to only register from the main branch, otherwise 
    you may end up registering tables that do not end up in production.
    """,
    action="register",
)
@file_source_type_options(
    option_group_help_text="""Options for registering a Protobuf message, Avro record, or JSON schema object as data assets. These objects 
    represent data your production services produce, regardless of the transport mechanism. 

    If you're registering Protobuf messages, Avro records, or JSON schema objects in your CI/CD workflow, it's important 
    to only register from the main branch, otherwise you may end up registering records that do not end up in production.
    """,
    action="register",
)
@python_project_options(
    option_group_help_text="""
    Options for registering Python projects as data assets. This set of options is designed to handle the registration of Python-based projects, 
    enabling Gable to track and manage Python codebases as part of its data asset inventory.

    When registering a Python project, it's important to specify the project's entry point, which is the root directory of your project. 
    This allows Gable to correctly identify the project for analysis. Additionally, specifying the emitter function and event name key 
    helps Gable understand how your project interacts with and emits data, ensuring accurate tracking and management.

    The Python project options include:
    - Specifying the project's entry point.
    - Identifying the emitter function to track how the project emits data.
    - Defining the event name key for targeted event handling and listening.

    It's crucial to ensure that the information provided reflects the actual state of your project in your production environment. 
    When using these options as part of your CI/CD workflow, make sure to register your Python projects from the main branch. 
    Registering from feature or development branches may lead to inconsistencies and inaccuracies in the data asset registry, 
    as these branches may contain code that is not yet, or may never be, deployed to production.
    """,
    action="register",
)
@pyspark_project_options(
    option_group_help_text="""
    Options for registering Pyspark tables as data assets. This set of options is designed to handle the registration of Pyspark-based projects, 
    enabling Gable to track and manage Pyspark scripts as part of its data asset inventory.

    When registering a Pyspark table, it's important to specify the project root and the entrypoint of the job. This allows Gable to correctly
    identify the project for analysis. Additionally, .....

    The Pyspark project options include:
    - Specifying the project's entrypoint along with necessary arguments.
    - Identifying the path to the Python executable to be able to run the Pyspark script.

    It's crucial to ensure that the information provided reflects the actual state of your project in your production environment. 
    When using these options as part of your CI/CD workflow, make sure to register your Pyspark scripts from the main branch. 
    Registering from feature or development branches may lead to inconsistencies and inaccuracies in the data asset registry, 
    as these branches may contain code that is not yet, or may never be, deployed to production.
    """,
    action="register",
)
@typescript_project_options(
    option_group_help_text="""
    Options for registering Typescript projects as data assets. This set of options is designed to handle the registration of Typescript-based projects, 
    enabling Gable to track and manage Typescript codebases as part of its data asset inventory.

    When registering a Typescript project, it's important to specify the library emitting the events that are intended to be registered as data assets.

    It's crucial to ensure that the information provided reflects the actual state of your project in your production environment. 
    When using these options as part of your CI/CD workflow, make sure to register your Typescript projects from the main branch. 
    Registering from feature or development branches may lead to inconsistencies and inaccuracies in the data asset registry, 
    as these branches may contain code that is not yet, or may never be, deployed to production.
    """,
    action="register",
)
@s3_project_options(
    option_group_help_text="""
    Options for registering S3 files as data assets. This set of options is designed to handle the registration of S3 files, 
    enabling Gable to track and manage them as part of its data asset inventory.

    When registering S3 files, it's important to specify the AWS bucket containing the files that are intended to be registered as data assets.
    """,
    action="register",
)
@global_options()
@click.pass_context
def register_data_asset(
    ctx: ClickContext,
    source_type: SourceType,
    dry_run: bool,
    host: str,
    port: int,
    db: str,
    schema: str,
    table: Union[str, None],
    proxy_host: str,
    proxy_port: int,
    proxy_db: str,
    proxy_schema: str,
    proxy_user: str,
    proxy_password: str,
    files: tuple,
    project_root: Optional[str],
    emitter_function: Optional[str],
    emitter_payload_parameter: Optional[str],
    emitter_name_parameter: Optional[str],
    event_name_key: Optional[str],
    emitter_file_path: Optional[str],
    spark_job_entrypoint: Optional[str],
    connection_string: Optional[str],
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    library: Optional[str],
    exclude: Optional[str],
    bucket: Optional[str],
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    lookback_days: int,
    history: Optional[bool],
    row_sample_count: int,
    recent_file_count: int,
    skip_profiling: bool,
    config_file: Optional[click.File],
    config_entrypoint_path: Optional[str],
    config_args_path: Optional[str],
) -> None:
    """Registers a data asset with Gable"""
    tables: Union[list[str], None] = (
        [t.strip() for t in table.split(",")] if table else None
    )
    if source_type in DATABASE_SOURCE_TYPES:
        proxy_db = proxy_db if proxy_db else db
        proxy_schema = proxy_schema if proxy_schema else schema
        files_list: list[str] = []
        database_schema = f"{db}.{schema}"
    elif source_type in STATIC_CODE_ANALYSIS_SOURCE_TYPES:
        files_list: list[str] = []
        database_schema = ""
    else:
        # Turn the files tuple into a list
        files_list: list[str] = list(files)
        # This won't be set for file-based data assets, but we need to pass through
        # the real db.schema value in case the proxy database has different names
        database_schema = ""

    source_names: list[str] = []
    schema_contents: list[str] = []
    client: GableAPIClient = ctx.obj.client
    check_response_pydantic = None
    if source_type in SCHEMA_SOURCE_TYPES:
        schema_contents = get_schema_contents(
            source_type=source_type,
            dbuser=proxy_user,
            dbpassword=proxy_password,
            db=proxy_db,
            dbhost=proxy_host,
            dbport=proxy_port,
            schema=proxy_schema if proxy_schema else schema,
            tables=tables,
            files=files_list,
        )
        source_names = get_source_names(
            ctx=ctx,
            source_type=source_type,
            dbhost=host,
            dbport=port,
            files=files_list,
        )
        if is_empty_schema_contents(source_type, schema_contents):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
            )
        if dry_run:
            logger.info("Dry run mode. Data asset registration not performed.")
        request = {
            "sourceType": source_type,
            "sourceNames": source_names,
            "databaseSchema": database_schema,
            "schema": schema_contents,
            "dryRun": dry_run,
            "prLink": get_pr_link(),
        }
        # Break up the request into smaller chunks to avoid timeout issues
        registered_asset_ids: List[str] = []
        most_recent_registration_message = ""
        for schema_chunk in chunk_list(schema_contents, DATA_ASSET_REGISTER_CHUNK_SIZE):
            request["schema"] = schema_chunk
            register_response, success, _status_code = client.post_data_asset_ingest(
                request
            )
            if not success:
                raise click.ClickException(
                    f"{EMOJI.RED_X.value} Registration failed for some data assets: {str(register_response)}"
                )
            registered_asset_ids.extend(register_response["registered"])
            most_recent_registration_message = register_response["message"]

        # Create a register response so we can use the same response handling below
        register_response = {
            "registered": registered_asset_ids,
            "message": most_recent_registration_message,
        }
        success = True
    elif source_type == SourceType.python:
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
            get_abs_project_root_path(project_root),
            emitter_file_path,
            emitter_function,
            emitter_payload_parameter,
            event_name_key,
            exclude,
            ctx.obj.client,
        )

        if is_empty_schema_contents(source_type, schema_contents):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
            )
        if dry_run:
            logger.info("Dry run mode. Data asset registration not performed.")
        request = {
            "sourceType": source_type,
            "sourceNames": source_names,
            "databaseSchema": database_schema,
            "schema": schema_contents,
            "dryRun": dry_run,
            "prLink": get_pr_link(),
        }
        register_response, success, _status_code = client.post_data_asset_ingest(
            request
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

        response_pydantic, success, _status_code = register_pyspark_data_assets(
            ctx,
            spark_job_entrypoint,
            project_root,
            connection_string,
            csv_schema_file,
            csv_path_to_table_file,
            dry_run,
        )

        register_response = (
            response_pydantic.dict()
        )  # shim so we can use the same response handling below
    elif source_type == SourceType.typescript:
        if not library and not emitter_function:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required options for Typescript project registration. Either --library or --emitter-function must be specified. You can use the --help option for more details."
            )
        if library and emitter_function:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Only one of --library or --emitter-function may be specified. You can use the --help option for more details."
            )
        if emitter_function and (
            not emitter_payload_parameter
            or not emitter_file_path
            or (not event_name_key and not emitter_name_parameter)
        ):
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required options for Typescript project registration when using --emitter-function. Options --emitter-payload-parameter, --emitter-file-path, and either --event-name-key or --event-name-parameter are required. You can use the --help option for more details."
            )
        if not project_root:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Missing required option --project-root for Typescript project registration. You can use the --debug or --trace flags for more details."
            )
        response_pydantic, success, _status_code = register_typescript_data_assets(
            ctx,
            library,
            project_root,
            emitter_file_path,
            emitter_function,
            emitter_payload_parameter,
            emitter_name_parameter,
            event_name_key,
            dry_run,
        )
        register_response = (
            response_pydantic.dict()
        )  # shim so we can use the same response handling below
    elif source_type == SourceType.s3:
        from gable.cli.helpers.data_asset_s3 import (
            detect_s3_data_assets_history,
            register_and_check_s3_data_assets,
            validate_input,
        )

        validate_input(
            "register", bucket, lookback_days, include_prefix, exclude_prefix, history
        )

        if history:
            detect_s3_data_assets_history(
                bucket,  # type: ignore (input validation ensures bucket is not None, this quashes linter)
                include,  # type: ignore (input validation ensures include is not None or empty, this quashes linter)
            )
            return

        # We want to both register and check S3 data assets since customers will be using the register command
        # in live change detection.
        register_response_pydantic, check_response_pydantic = (
            register_and_check_s3_data_assets(
                ctx,
                bucket,  # type: ignore (input validation ensures bucket is not None, this quashes linter)
                lookback_days,
                row_sample_count,
                recent_file_count,
                include_prefix,
                exclude_prefix,
                dry_run,
                skip_profiling,
            )
        )
        register_response = register_response_pydantic[
            0
        ].dict()  # shim so we can use the same response handling below
        success = register_response_pydantic[1]
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")

    if not success:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Registration failed for some data assets: {str(register_response)}"
        )
    registered_assets = register_response["registered"]
    registered_output = ", ".join(
        shell_linkify_if_not_in_ci(
            f"{client.ui_endpoint}/assets/{quote(asset, safe='')}",
            asset,
        )
        for asset in registered_assets
    )
    logger.info(
        f"{EMOJI.GREEN_CHECK.value} Registration successful:\n{registered_output}"
    )
    if not dry_run:
        logger.info(register_response["message"])
    else:
        logger.info("Dry run mode. Data asset registration not performed.")

    # Only for S3 data asset registration
    if check_response_pydantic is not None:
        format_compliance_check_response_for_cli(check_response_pydantic, "text")
