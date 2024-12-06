import json
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Optional, Union

import boto3
import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.data_asset_s3.pattern_discovery import (
    discover_patterns_from_s3_bucket,
)
from gable.cli.helpers.data_asset_s3.schema_detection import (
    S3DetectionResult,
    get_schema_from_s3_files,
    strip_s3_bucket_prefix,
)
from gable.cli.helpers.emoji import EMOJI
from gable.openapi import (
    CheckComplianceDataAssetsS3Request,
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetResponse,
    ErrorResponse,
    ErrorResponseDeprecated,
    IngestDataAssetResponse,
    RegisterDataAssetS3Request,
    ResponseType,
    S3Asset,
)
from loguru import logger
from mypy_boto3_s3 import S3Client

RegisterS3Response = tuple[
    Union[IngestDataAssetResponse, ErrorResponseDeprecated], bool, int
]
CheckComplianceS3Response = Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[CheckDataAssetResponse],
]


def get_s3_client() -> S3Client:
    return boto3.client("s3")


def register_and_check_s3_data_assets(
    ctx: ClickContext,
    bucket_name: str,
    lookback_days: int,
    row_sample_count: int,
    recent_file_count: int,
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    dry_run: bool = False,
    skip_profiling: bool = False,
) -> tuple[RegisterS3Response, CheckComplianceS3Response]:
    with warnings.catch_warnings():
        # Ignore FutureWarnings from pandas
        warnings.simplefilter(action="ignore", category=FutureWarning)

        results = _process_s3_data_assets(
            ctx.obj.client,
            bucket_name,
            skip_profiling,
            lookback_days,
            row_sample_count,
            recent_file_count,
            include_prefix,
            exclude_prefix,
            dry_run,
        )
    if not results:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No S3 data assets found to register or check!"
        )

    register_results = [response[0] for response in results]
    check_results = [response[1] for response in results]
    return aggregate_register_s3_results(
        register_results
    ), aggregate_check_compliance_s3_results(check_results)


def check_compliance_s3_data_assets(
    ctx: ClickContext,
    response_type: ResponseType,
    bucket_name: str,
    lookback_days: int,
    row_sample_count: int,
    recent_file_count: int,
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    skip_profiling: bool,
) -> CheckComplianceS3Response:
    results = _detect_and_check_compliance_s3_data_assets(
        ctx.obj.client,
        bucket_name,
        skip_profiling,
        lookback_days,
        response_type,
        row_sample_count,
        recent_file_count,
        include_prefix,
        exclude_prefix,
    )
    if not results:
        return ErrorResponse(
            message=f"No S3 data assets found to check!",
        )
    return aggregate_check_compliance_s3_results(results)


def aggregate_check_compliance_s3_results(results: list[CheckComplianceS3Response]):
    if not results:
        return ErrorResponse(
            message=f"No S3 data assets found to check!",
        )
    aggregated_result = results[0]
    for result in results[1:]:
        if isinstance(result, ErrorResponse):
            return result
        elif isinstance(result, CheckDataAssetCommentMarkdownResponse) and isinstance(
            aggregated_result, CheckDataAssetCommentMarkdownResponse
        ):
            aggregated_result = CheckDataAssetCommentMarkdownResponse(
                markdown=((aggregated_result.markdown or "") + (result.markdown or ""))
                or None,
                shouldAlert=aggregated_result.shouldAlert or result.shouldAlert,
                shouldBlock=aggregated_result.shouldBlock or result.shouldBlock,
                responseType="COMMENT_MARKDOWN",
                errors=((result.errors or []) + (aggregated_result.errors or []))
                or None,
            )
        elif isinstance(result, list) and isinstance(aggregated_result, list):
            aggregated_result = aggregated_result + result
    return aggregated_result


def aggregate_register_s3_results(results: list[RegisterS3Response]):
    aggregated_register_result = (
        results[0][0].dict(),
        results[0][1],
        results[0][2],
    )
    for response_pydantic, success, status_code in results[1:]:
        new_response = {**aggregated_register_result[0], **response_pydantic.dict()}
        new_success = aggregated_register_result[1] and success
        new_status_code = max(aggregated_register_result[2], status_code)
        aggregated_register_result = (new_response, new_success, new_status_code)
    return (
        IngestDataAssetResponse(**aggregated_register_result[0]),
        aggregated_register_result[1],
        aggregated_register_result[2],
    )


def _process_s3_data_assets(
    client: GableAPIClient,
    bucket_name: str,
    skip_profiling: bool,
    lookback_days: int,
    row_sample_count: int,
    recent_file_count: int,
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    dry_run: bool = False,
) -> list[tuple[RegisterS3Response, CheckComplianceS3Response]]:
    """
    Detect data assets in S3 bucket. Register and check compliance of assets.
    Args:
        bucket (str): S3 bucket name.
        lookback_days (int): Lookback days.
        row_sample_count (int): Number of rows to sample per S3 file.
        lookback_days: (int), number of days to look back from the latest day in the list of paths. For example
                if the latest path is 2024/01/02, and lookback_days is 3, then the paths return will have
                2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30.
        skip_profiling (bool): Whether to compute data profiles.
    Returns:
        list[tuple[RegisterS3Response, CheckComplianceS3Response]]: Register and check API responses.
    """
    patterns_to_urls = discover_patterns_from_s3_bucket(
        get_s3_client(),
        strip_s3_bucket_prefix(bucket_name),
        recent_file_count,
        start_date=datetime.now() - timedelta(days=lookback_days),
        include_prefix=include_prefix,
        exclude_prefix=exclude_prefix,
        ignore_timeframe_bounds=False,
    )
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda entry: _register_and_check_s3_files(
                client,
                strip_s3_bucket_prefix(bucket_name),
                entry[0],
                set([url for _, url in entry[1]]),
                row_sample_count,
                recent_file_count,
                skip_profiling,
                dry_run,
            ),
            patterns_to_urls.items(),
        )
        return list(results)


def _detect_and_check_compliance_s3_data_assets(
    client: GableAPIClient,
    bucket_name: str,
    skip_profiling: bool,
    lookback_days: int,
    response_type: ResponseType,
    row_sample_count: int,
    recent_file_count: int,
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
) -> list[CheckComplianceS3Response]:
    """
    Detect data assets in S3 bucket.
    Args:
        bucket (str): S3 bucket name.
        lookback_days (int): Lookback days.
        row_sample_count (int): Number of rows to sample per S3 file.
        lookback_days: (int), number of days to look back from the latest day in the list of paths. For example
                if the latest path is 2024/01/02, and lookback_days is 3, then the paths return will have
                2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30.
        skip_profiling (bool): Whether to compute data profiles.
    Returns:
        dict[str, S3DetectionResult]: Mapping of asset pattern to schema/data profiles.
    """
    patterns_to_urls = discover_patterns_from_s3_bucket(
        get_s3_client(),
        strip_s3_bucket_prefix(bucket_name),
        recent_file_count,
        start_date=datetime.now() - timedelta(days=lookback_days),
        include_prefix=include_prefix,
        exclude_prefix=exclude_prefix,
        ignore_timeframe_bounds=False,
    )
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda entry: _get_and_check_compliance_merged_def_from_s3_files(
                client,
                strip_s3_bucket_prefix(bucket_name),
                entry[0],
                set([url for _, url in entry[1]]),
                response_type,
                row_sample_count,
                skip_profiling,
            ),
            patterns_to_urls.items(),
        )
        return list(filter(None, results))


def _register_and_check_s3_files(
    client: GableAPIClient,
    bucket: str,
    event_name: str,
    s3_urls: set[str],
    row_sample_count: int,
    recent_file_count: int,
    skip_profiling: bool = False,
    dry_run: bool = False,
) -> tuple[RegisterS3Response, CheckComplianceS3Response]:
    """
    Get merged schema along with data profile from given S3 file urls (only CSV, JSON, and parquet currently supported), and
    call register (if dry_run is False) and check API.
    Args:
        bucket_name (str): S3 bucket name.
        event_name (str): Event name.
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
        skip_profiling (bool): Whether to compute data profiles.
        dry_run (bool): Whether to register detected data assets.
    """
    if result := get_schema_from_s3_files(
        bucket, event_name, s3_urls, row_sample_count, recent_file_count, skip_profiling
    ):
        logger.info(
            f"Pattern: {event_name}\nSchema: {json.dumps(result.schema, indent=4)}"
        )
        if dry_run:
            register_response = (
                IngestDataAssetResponse(message="", registered=[], success=True),
                True,
                200,
            )
            check_response = []

        else:
            register_request = RegisterDataAssetS3Request(
                dry_run=dry_run,
                assets=[
                    S3Asset(
                        schema=result.schema,
                        fieldNameToDataAssetFieldProfileMap=result.data_asset_fields_to_profiles_map,
                        bucket=bucket,
                        pattern=event_name,
                    )
                ],
            )
            register_response = client.post_data_asset_register_s3(register_request)
            check_response = get_check_compliance_s3_results(
                result, bucket, event_name, ResponseType.DETAILED, client
            )
        return (register_response, check_response)
    else:
        return (
            (
                ErrorResponseDeprecated(
                    message=f"No data found in S3 files for event name: {event_name}",
                    success=False,
                ),
                False,
                404,
            ),
            ErrorResponse(
                message=f"No data found in S3 files for event name: {event_name}",
            ),
        )


def _get_and_check_compliance_merged_def_from_s3_files(
    client: GableAPIClient,
    bucket: str,
    event_name: str,
    s3_urls: set[str],
    response_type: ResponseType,
    row_sample_count: int,
    recent_file_count: int,
    skip_profiling: bool = False,
) -> CheckComplianceS3Response:
    """
    Get merged definition along with data profile from given S3 file urls (only CSV, JSON, and parquet currently supported).
    Args:
        bucket_name (str): S3 bucket name.
        event_name (str): Event name.
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
    Returns:
        tuple[dict, Optional[DataProfileFieldsMapping]]: Merged definition and data profile if able to be computed.
    """
    if result := get_schema_from_s3_files(
        bucket, event_name, s3_urls, row_sample_count, recent_file_count, skip_profiling
    ):
        return get_check_compliance_s3_results(
            result, bucket, event_name, response_type, client
        )
    else:
        return ErrorResponse(
            message=f"No data found in S3 files for event name: {event_name}",
        )


def get_check_compliance_s3_results(
    result: S3DetectionResult,
    bucket: str,
    event_name: str,
    response_type: ResponseType,
    client: GableAPIClient,
) -> CheckComplianceS3Response:
    request = CheckComplianceDataAssetsS3Request(
        assets=[
            S3Asset(
                schema=result.schema,
                fieldNameToDataAssetFieldProfileMap=result.data_asset_fields_to_profiles_map,
                bucket=bucket,
                pattern=event_name,
            )
        ],
        responseType=response_type,
    )
    return client.post_check_compliance_data_assets_s3(request)
