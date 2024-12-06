import array
from typing import Any, Optional

import numpy as np
import pandas as pd
from gable.cli.helpers.data_asset_s3.logger import log_error
from gable.cli.helpers.data_asset_s3.native_s3_converter import NativeS3Converter
from gable.cli.helpers.data_asset_s3.path_pattern_manager import (
    UUID_REGEX_V1,
    UUID_REGEX_V3,
    UUID_REGEX_V4,
    UUID_REGEX_V5,
)
from gable.openapi import (
    DataAssetFieldProfile,
    DataAssetFieldProfileBoolean,
    DataAssetFieldProfileList,
    DataAssetFieldProfileNumber,
    DataAssetFieldProfileOther,
    DataAssetFieldProfileString,
    DataAssetFieldProfileTemporal,
    DataAssetFieldProfileUnion,
    DataAssetFieldProfileUUID,
    DataAssetFieldsToProfilesMapping,
    S3SamplingParameters,
)
from loguru import logger


def get_data_asset_field_profiles_for_data_asset(
    recap_schema: dict,
    file_to_df: dict[str, pd.DataFrame],
    event_name: str,
    sampling_params: S3SamplingParameters,
) -> Optional[DataAssetFieldsToProfilesMapping]:
    """
    given a mapping of column name to pandas dataframe, return a mapping of column names to data asset field profiles
    """
    logger.debug(f"Attempting to compute data asset profile for asset: {event_name}")

    try:
        df = pd.concat(file_to_df.values())
        file_list = list(file_to_df.keys())
        result: dict[str, DataAssetFieldProfile] = {}

        column_name_to_schema: dict[str, dict] = {}
        _populate_column_schemas(recap_schema, column_name_to_schema)
        for column_name, column_schema in column_name_to_schema.items():
            if column_name not in df.columns:
                log_error(
                    f"column {column_name} not found in data - skipping in data asset profile"
                )
            else:
                try:
                    result[column_name] = _get_data_asset_field_profile_for_column(
                        column_schema, df[column_name], file_list, sampling_params  # type: ignore
                    )
                except Exception as e:
                    log_error(
                        f"Error computing data asset profile for column {column_name} in asset {event_name}: {e}"
                    )

        return DataAssetFieldsToProfilesMapping(__root__=result)
    except Exception as e:
        log_error(f"Error computing data asset profiles for asset {event_name}: {e}")


def _populate_column_schemas(
    recap_schema: dict, map: dict[str, dict], prefix: str = ""
):
    for column_schema in recap_schema["fields"]:
        column_name = column_schema["name"]
        if "fields" in column_schema:
            # If the schema is a struct type, we need to go into the nested level
            _populate_column_schemas(column_schema, map, prefix + column_name + ".")
        else:
            map[prefix + column_name] = column_schema


def get_data_asset_field_profile_for_union_column(
    schema: dict,
    column: pd.Series,
    file_list: list[str],
    sampling_params: S3SamplingParameters,
    nullable: bool = False,
) -> DataAssetFieldProfile:
    """
    for recursive union calls, handle splitting up the constituent profile data and stats
    """
    converter = NativeS3Converter()
    df = pd.DataFrame(column)
    filter_types = None
    if schema["type"] in ("int", "float"):
        if _schema_is_date(schema):
            filter_types = [pd.Series().astype("datetime64[ns]").dtype]
        else:
            filter_types = [pd.Int64Dtype(), pd.Float64Dtype()]
    elif schema["type"] == "string":
        filter_types = [pd.StringDtype()]
    elif schema["type"] == "bool":
        filter_types = [pd.BooleanDtype()]

    if filter_types is not None:
        column = pd.Series(
            [
                entry
                for entry in column
                if converter.detect_type(entry, df, str(column.name)) in filter_types
            ]
        )
    return _get_data_asset_field_profile_for_column(
        schema, column, file_list, sampling_params, nullable
    )


def _get_data_asset_field_profile_for_column(
    schema: dict,
    column: pd.Series,
    file_list: list[str],
    sampling_params: S3SamplingParameters,
    nullable: bool = False,
) -> DataAssetFieldProfile:
    """
    given a column name and a pandas series, return a data asset field profile
    """
    res = None
    null_count = None
    sampled_records_count = len(column)
    null_count = column.isnull().sum() if nullable else None
    column_without_empty_string = (
        column.replace("", np.nan).infer_objects(copy=False)
        if schema["type"] != "list"
        else column
    )
    column_without_empty_null: pd.Series = column_without_empty_string.dropna()
    if schema["type"] == "bool":
        column_to_filter = column_without_empty_null.astype(str)
        true_series = column_to_filter.str.contains("true", case=False)
        false_series = column_to_filter.str.contains("false", case=False)
        res = DataAssetFieldProfileBoolean(
            profileType="boolean",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            trueCount=len(column_to_filter[true_series]),
            falseCount=len(column_to_filter[false_series]),
            sampledFiles=file_list,
            samplingParameters=sampling_params,
        )
    elif schema["type"] in ("int", "float"):
        if _schema_is_date(schema):
            res = DataAssetFieldProfileTemporal(
                profileType="temporal",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                min=column_without_empty_null.min(),
                max=column_without_empty_null.max(),
                format="",  # TODO: revisit how to support with MM, DD, YY notation
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
        else:
            res = DataAssetFieldProfileNumber(
                profileType="number",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                uniqueCount=column_without_empty_null.nunique(),
                min=column_without_empty_null.min(),
                max=column_without_empty_null.max(),
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
    elif schema["type"] == "string":
        for version, regex in [
            (1, UUID_REGEX_V1),
            (3, UUID_REGEX_V3),
            (4, UUID_REGEX_V4),
            (5, UUID_REGEX_V5),
        ]:
            if column_without_empty_null.str.fullmatch(rf"^{regex}$", case=False).all():
                res = DataAssetFieldProfileUUID(
                    profileType="uuid",
                    sampledRecordsCount=sampled_records_count,
                    nullable=nullable,
                    nullCount=null_count,
                    uuidVersion=version,
                    emptyCount=(column == "").sum(),
                    uniqueCount=column_without_empty_null.nunique(),
                    maxLength=column_without_empty_null.str.len().max(),
                    minLength=column_without_empty_null.str.len().min(),
                    sampledFiles=file_list,
                    samplingParameters=sampling_params,
                    # TODO - add format
                )
                break
        if res is None:
            res = DataAssetFieldProfileString(
                profileType="string",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                emptyCount=(column == "").sum(),
                uniqueCount=column_without_empty_null.nunique(),
                maxLength=column_without_empty_null.str.len().max(),
                minLength=column_without_empty_null.str.len().min(),
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
    elif schema["type"] == "list":
        res = DataAssetFieldProfileList(
            profileType="list",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            maxLength=column_without_empty_null.str.len().max(),
            minLength=column_without_empty_null.str.len().min(),
            sampledFiles=file_list,
            samplingParameters=sampling_params,
        )
    elif schema["type"] == "union":
        non_null_schemas = [
            field for field in schema["types"] if field["type"] != "null"
        ]
        if (
            len(non_null_schemas) == 1
        ):  # it not a proper union, it's just representing a nullable field
            return _get_data_asset_field_profile_for_column(
                non_null_schemas[0], column, file_list, sampling_params, True
            )
        else:
            non_null_profiles: list[DataAssetFieldProfile] = [
                get_data_asset_field_profile_for_union_column(
                    schema, column, file_list, sampling_params, nullable
                )
                for schema in non_null_schemas
            ]
            res = DataAssetFieldProfileUnion(
                profileType="union",
                sampledRecordsCount=sampled_records_count,
                nullable=False,
                profiles=non_null_profiles,
                sampledFiles=file_list,
                samplingParameters=sampling_params,
            )
    else:
        res = DataAssetFieldProfileOther(
            profileType="other",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            sampledFiles=file_list,
            samplingParameters=sampling_params,
        )
    return DataAssetFieldProfile(__root__=res)


def replace_empty_string_with_nan(element: Any) -> Any:
    if isinstance(element, np.ndarray):
        return element
    else:
        return np.nan if element == "" else element


def _schema_is_date(schema: dict) -> bool:
    return schema["type"] == "int" and schema.get("logical", None) in [
        "Timestamp",
        "Date",
    ]
