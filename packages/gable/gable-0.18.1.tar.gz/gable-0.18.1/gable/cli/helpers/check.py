import json
from typing import Any, List, Optional, Union

from gable.api.client import GableAPIClient, del_none, parse_check_data_asset_response
from gable.cli.helpers.repo_interactions import get_pr_link
from gable.common_types import DATABASE_SOURCE_TYPES, FILE_SOURCE_TYPES
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetResponse,
    ErrorResponse,
    Input,
    ResponseType,
    SourceType,
)
from pydantic import parse_obj_as


def post_data_assets_check_requests(
    client: GableAPIClient,
    responseType: ResponseType,
    source_type: SourceType,
    source_names: List[str],
    realDbName: str,
    realDbSchema: str,
    schema_contents: List[str],
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[CheckDataAssetResponse],
]:
    requests = build_check_data_asset_inputs(
        source_type=source_type,
        source_names=source_names,
        schema_contents=schema_contents,
        realDbName=realDbName,
        realDbSchema=realDbSchema,
    )

    inputs = [del_none(input.dict()) for input in requests.values()]
    request = {
        "responseType": responseType.value,
        "inputs": inputs,
        "prLink": get_pr_link(),
    }

    result = client.post_data_assets_check(request)
    if responseType == ResponseType.DETAILED:
        if isinstance(result, list):
            return [parse_check_data_asset_response(r) for r in result]
        else:
            return ErrorResponse.parse_obj(result)
    if responseType == ResponseType.COMMENT_MARKDOWN:
        if isinstance(result, dict):
            if "responseType" in result:
                return parse_obj_as(CheckDataAssetCommentMarkdownResponse, result)
            else:
                return ErrorResponse.parse_obj(result)
    raise ValueError(f"Unknown response type: {responseType}, cannot parse result")


def build_check_data_asset_inputs(
    source_type: SourceType,
    source_names: list[str],
    schema_contents: list[str],
    realDbName: Optional[str] = None,
    realDbSchema: Optional[str] = None,
) -> dict[str, Input]:
    requests: dict[str, Input] = {}
    # If this is a database, there might be multiple table's schemas within the information schema
    # returned from the DbApi reader. In that case, we need to post each table's schema separately.
    if source_type in DATABASE_SOURCE_TYPES:
        schema_contents_str = schema_contents[0]
        source_name = source_names[0]
        information_schema = json.loads(schema_contents_str)
        grouped_table_schemas: dict[str, List[Any]] = {}
        for information_schema_row in information_schema:
            if information_schema_row["TABLE_NAME"] not in grouped_table_schemas:
                grouped_table_schemas[information_schema_row["TABLE_NAME"]] = []
            grouped_table_schemas[information_schema_row["TABLE_NAME"]].append(
                information_schema_row
            )
        for table_name, table_schema in grouped_table_schemas.items():
            requests[f"{realDbName}.{realDbSchema}.{table_name}"] = Input(
                sourceType=source_type,
                sourceName=source_name,
                realDbName=realDbName,
                realDbSchema=realDbSchema,
                schemaContents=json.dumps(table_schema),
            )
    elif source_type in FILE_SOURCE_TYPES:
        for source_name, schema in zip(source_names, schema_contents):
            requests[source_name] = Input(
                sourceType=source_type,
                sourceName=source_name,
                schemaContents=schema,
            )
    else:  # source_type in PYTHON_SOURCE_TYPE_VALUES
        for source_name, schema in zip(source_names, schema_contents):
            requests[source_name] = Input(
                sourceType=source_type,
                sourceName=source_name,
                schemaContents=schema,
            )
    return requests
