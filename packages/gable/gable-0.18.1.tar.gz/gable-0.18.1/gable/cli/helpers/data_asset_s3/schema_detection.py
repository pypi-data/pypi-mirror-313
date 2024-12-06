import math
from dataclasses import dataclass
from typing import Optional

import boto3
import click
import pandas as pd
import pyarrow.fs
import pyarrow.orc
import s3fs
from fastparquet import ParquetFile
from gable.cli.helpers.data_asset_s3.logger import log_debug
from gable.cli.helpers.data_asset_s3.native_s3_converter import NativeS3Converter
from gable.cli.helpers.data_asset_s3.path_pattern_manager import SUPPORTED_FILE_TYPES
from gable.cli.helpers.data_asset_s3.schema_profiler import (
    get_data_asset_field_profiles_for_data_asset,
)
from gable.openapi import DataAssetFieldsToProfilesMapping, S3SamplingParameters
from loguru import logger

CHUNK_SIZE = 100


@dataclass
class S3DetectionResult:
    schema: dict
    data_asset_fields_to_profiles_map: Optional[DataAssetFieldsToProfilesMapping] = None


@dataclass
class S3ReadResult:
    df: pd.DataFrame
    has_schema: bool


def read_s3_files(
    s3_urls: list[str],
    row_sample_count: int,
    s3_opts: Optional[dict] = None,
) -> dict[str, S3ReadResult]:
    """
    Read data from given S3 file urls (only CSV, JSON, and parquet currently supported) and return pandas DataFrames.
    Args:
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
        s3_opts (dict): S3 storage options. - only needed for tests using moto mocking
    Returns:
        dict[str, S3ReadResult]: Dict of file url to pandas DataFrames and a boolean indicating if the DataFrame has a predefined schema.
    """
    result: dict[str, S3ReadResult] = {}
    for url in s3_urls:
        if df := read_s3_file(url, row_sample_count, s3_opts):
            result[url] = df
    return result


def read_s3_file(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> Optional[S3ReadResult]:
    """
    Returns a tuple of pandas DataFrame and a boolean indicating if the DataFrame has a predefined schema.
    """
    try:
        if url.endswith(SUPPORTED_FILE_TYPES.CSV.value):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            df = get_csv_df(url, num_rows_to_sample, s3_opts)
            if df.empty:
                logger.info(f"No data found in the CSV file: {url}")
            return S3ReadResult(df, False)
        elif url.endswith(SUPPORTED_FILE_TYPES.JSON.value):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            chunks = list(
                pd.read_json(
                    url,
                    lines=True,
                    chunksize=CHUNK_SIZE,
                    nrows=num_rows_to_sample,
                    storage_options=s3_opts,
                )
            )
            if not chunks:  # No data was read, file is empty
                logger.info(f"No data found in the JSON file: {url}")
                return S3ReadResult(pd.DataFrame(), False)
            df = pd.concat(chunks, ignore_index=True)
            return S3ReadResult(flatten_json(df), False)
        elif url.endswith(SUPPORTED_FILE_TYPES.PARQUET.value):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            df = get_parquet_df(url, num_rows_to_sample, s3_opts)
            if df.empty:
                logger.info(f"No data found in the Parquet file: {url}")
            return S3ReadResult(df, True)
        elif url.endswith(SUPPORTED_FILE_TYPES.ORC.value) or url.endswith(
            SUPPORTED_FILE_TYPES.ORC_SNAPPY.value
        ):
            log_debug(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            df = get_orc_df(url, num_rows_to_sample, s3_opts)
            if df.empty:
                logger.info(f"No data found in the ORC file: {url}")
            return S3ReadResult(df, True)
        else:
            log_debug(f"Unsupported file format: {url}")
            return None
    except Exception as e:
        # Swallowing exceptions to avoid failing processing other files
        logger.opt(exception=e).error(f"Error reading file {url}: {e}")
        return None


def get_orc_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read ORC file from S3 and return a pandas DataFrame.
    """
    endpoint_override = (
        s3_opts.get("client_kwargs", {}).get("endpoint_url") if s3_opts else None
    )
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise click.ClickException("No AWS credentials found")
    filesystem = pyarrow.fs.S3FileSystem(
        endpoint_override=endpoint_override,
        access_key=credentials.access_key,
        secret_key=credentials.secret_key,
        session_token=credentials.token,
        region=boto3.Session().region_name,
    )
    bucket_and_path = strip_s3_bucket_prefix(url)
    with filesystem.open_input_file(bucket_and_path) as f:
        orcfile = pyarrow.orc.ORCFile(f)
        if orcfile.nrows == 0:
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the ORC file has no rows
        rows_per_stripe = orcfile.nrows / orcfile.nstripes
        stripes_to_sample = min(
            math.ceil(num_rows_to_sample / rows_per_stripe), orcfile.nstripes
        )
        log_debug(
            f"Reading {stripes_to_sample} stripes from {url} (total rows: {orcfile.nrows}, total stripes: {orcfile.nstripes})"
        )
        return pyarrow.Table.from_batches(
            [orcfile.read_stripe(i) for i in range(stripes_to_sample)]
        ).to_pandas()


def get_parquet_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read Parquet file from S3 and return an empty pandas DataFrame with the schema.
    """
    try:
        # Initialize the S3 file system
        s3_filesystem = s3fs.S3FileSystem(**(s3_opts or {}))

        # Initialize the ParquetFile
        parquet_file = ParquetFile(url, fs=s3_filesystem)

        # Check if the file has any rows
        if parquet_file.count() == 0:
            log_debug(f"The Parquet file {url} is empty.")
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the Parquet file has no rows

        # Try to read the specified number of rows
        return parquet_file.head(num_rows_to_sample)

    except ValueError as ve:
        if "Seek before start of file" in str(ve):
            log_debug(
                f"Seek error for file {url}, this could be due to an empty or corrupted file."
            )
            return pd.DataFrame()  # Return an empty DataFrame in case of seek error
        else:
            logger.error(
                f"ValueError encountered while reading Parquet file {url}: {ve}"
            )
            raise

    except Exception as e:
        logger.error(f"Unexpected error while reading Parquet file {url}: {e}")
        raise


def df_has_header(df: pd.DataFrame) -> bool:
    # (Modified from csv.Sniffer.has_header)
    # Creates a dictionary of types of data in each column. If any
    # column is of a single type (say, integers), *except* for the first
    # row, then the first row is presumed to be labels. If the type
    # can't be determined, it is assumed to be a string in which case
    # the length of the string is the determining factor: if all of the
    # rows except for the first are the same length, it's a header.
    # Finally, a 'vote' is taken at the end for each column, adding or
    # subtracting from the likelihood of the first row being a header.

    maybe_header = df.iloc[0]
    columns = len(df.columns)
    columnTypes: dict[int, type[complex] | int | None] = {}
    for i in range(columns):
        columnTypes[i] = None

    checked = 0
    for _, row in df.iloc[1:].iterrows():
        # arbitrary number of rows to check, to keep it sane
        if checked > 20:
            break
        checked += 1

        if len(row) != columns:
            continue  # skip rows that have irregular number of columns

        for col in list(columnTypes.keys()):
            thisType = complex
            try:
                thisType(row[col])
            except (ValueError, OverflowError):
                # fallback to length of string
                thisType = len(row[col])

            if thisType != columnTypes[col]:
                if columnTypes[col] is None:  # add new column type
                    columnTypes[col] = thisType
                else:
                    # type is inconsistent, remove column from
                    # consideration
                    del columnTypes[col]

    # finally, compare results against first row and "vote"
    # on whether it's a header
    hasHeader = 0
    for col, colType in columnTypes.items():
        if type(colType) == type(0):  # it's a length
            if len(maybe_header[col]) != colType:
                hasHeader += 1
            else:
                hasHeader -= 1
        else:  # attempt typecast
            try:
                colType(maybe_header[col])  # type: ignore
            except (ValueError, TypeError):
                hasHeader += 1
            else:
                hasHeader -= 1

    return hasHeader > 0


def get_csv_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read CSV file from S3 and return a pandas DataFrame. Special handling for CSV files with and without headers.
    """
    try:
        # Sample a small part of the CSV file to determine if there is a header
        sample_no_header_df = pd.read_csv(
            url, nrows=10, storage_options=s3_opts, engine="python", header=None
        )

        # If the sample dataframe is empty, return an empty DataFrame
        if sample_no_header_df.empty:
            log_debug(f"The CSV file {url} is empty.")
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the CSV file has no rows

        has_header = df_has_header(sample_no_header_df)

        if has_header:
            df = pd.concat(
                pd.read_csv(
                    url,
                    chunksize=CHUNK_SIZE,
                    nrows=num_rows_to_sample,
                    storage_options=s3_opts,
                ),
                ignore_index=True,
            )
        else:
            df = pd.concat(
                pd.read_csv(
                    url,
                    header=None,
                    chunksize=CHUNK_SIZE,
                    nrows=num_rows_to_sample,
                    storage_options=s3_opts,
                ),
                ignore_index=True,
            )
        return df

    except pd.errors.EmptyDataError:
        log_debug(f"No columns to parse from file {url}. Returning empty DataFrame.")
        return (
            pd.DataFrame()
        )  # Return an empty DataFrame if the CSV file has no columns

    except Exception as e:
        logger.error(f"Unexpected error while reading CSV file {url}: {e}")
        raise


def flatten_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens any nested JSON data to a single column
    {"customerDetails": {"technicalContact": {"email": "...."}}}" => customerDetails.technicalContact.email
    """
    normalized_df = pd.json_normalize(df.to_dict(orient="records"))
    return drop_null_parents(normalized_df)


def drop_null_parents(df: pd.DataFrame) -> pd.DataFrame:
    # Identify null columns
    null_columns = {col for col in df.columns if df[col].isnull().all()}  # type: ignore

    # Identify nested columns
    parent_columns = {col for col in df.columns if "." in col}

    # For null parent columns, drop them if they will be represented by the nested columns
    columns_to_drop = [
        null_column
        for null_column in null_columns
        for parent_column in parent_columns
        if null_column != parent_column and null_column in parent_column
    ]
    return df.drop(columns=columns_to_drop)


def append_s3_url_prefix(bucket_name: str, url: str) -> str:
    return "s3://" + bucket_name + "/" + url if not url.startswith("s3://") else url


def strip_s3_bucket_prefix(bucket_name: str) -> str:
    return bucket_name.removeprefix("s3://")


def get_schema_from_s3_files(
    bucket: str,
    event_name: str,
    s3_urls: set[str],
    row_sample_count: int,
    recent_file_count: int,
    skip_profiling: bool = False,
) -> Optional[S3DetectionResult]:
    """
    Get schema along with data profile from given S3 file urls (only CSV, JSON, and parquet currently supported).
    Args:
        bucket_name (str): S3 bucket name.
        event_name (str): Event name.
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
    Returns:
        S3DetectionResult: Merged schema and data profile if able to be computed.
    """
    urls = [append_s3_url_prefix(bucket, url) for url in s3_urls]
    s3_data = read_s3_files(urls, row_sample_count)
    if len(s3_data) > 0:
        schema = merge_schemas(
            [
                NativeS3Converter().to_recap(
                    df_result.df, df_result.has_schema, event_name
                )
                for _, df_result in s3_data.items()
                if len(df_result.df.columns) > 0
            ]
        )
        if skip_profiling:
            log_debug(f"Skipping data profiling for event name: {event_name}")
            return S3DetectionResult(schema)
        else:
            profiles = get_data_asset_field_profiles_for_data_asset(
                schema,
                {file_url: df_data.df for file_url, df_data in s3_data.items()},
                event_name,
                S3SamplingParameters(
                    rowSampleCount=row_sample_count,
                    recentFileCount=recent_file_count,
                ),
            )
            return S3DetectionResult(schema, profiles)


def merge_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple schemas into a single schema.
    Args:
        schemas (list[dict]): List of schemas.
    Returns:
        dict: Merged schema.
    """
    # Dictionary of final fields, will be turned into a struct type at the end
    result_dict: dict[str, dict] = {}
    for schema in schemas:
        if "fields" in schema:
            for field in schema["fields"]:
                field_name = field["name"]
                # If the field is not yet in the result, just add it
                if field_name not in result_dict:
                    result_dict[field_name] = field
                elif field != result_dict[field_name]:
                    # If both types are structs, recursively merge them
                    if (
                        field["type"] == "struct"
                        and result_dict[field_name]["type"] == "struct"
                    ):
                        result_dict[field_name] = {
                            "fields": merge_schemas([result_dict[field_name], field])[
                                "fields"
                            ],
                            "name": field_name,
                            "type": "struct",
                        }
                    else:
                        # Merge the two type into a union, taking into account that one or both of them
                        # may already be unions
                        result_types = (
                            result_dict[field_name]["types"]
                            if result_dict[field_name]["type"] == "union"
                            else [result_dict[field_name]]
                        )
                        field_types = (
                            field["types"] if field["type"] == "union" else [field]
                        )
                        result_dict[field_name] = {
                            "type": "union",
                            "types": get_distinct_dictionaries(
                                remove_names(result_types) + remove_names(field_types)
                            ),
                            "name": field_name,
                        }

    return {"fields": list(result_dict.values()), "type": "struct"}


def get_distinct_dictionaries(dictionaries: list[dict]) -> list[dict]:
    """
    Get distinct dictionaries from a list of dictionaries.
    Args:
        dictionaries (list[dict]): List of dictionaries.
    Returns:
        list[dict]: List of distinct dictionaries.
    """
    # Remove duplicates, use a list instead of a set to avoid
    # errors about unhashable types
    distinct = []
    for d in dictionaries:
        if d not in distinct:
            distinct.append(d)
    # Sort for testing so we have deterministic results
    return sorted(
        distinct,
        key=lambda x: x["type"],
    )


def remove_names(list: list[dict]) -> list[dict]:
    """
    Remove names from a list of dictionaries.
    Args:
        list (dict): List of dictionaries.
    Returns:
        dict: List of dictionaries without names.
    """
    for t in list:
        if "name" in t:
            del t["name"]
    return list
