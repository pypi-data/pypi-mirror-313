import re
from datetime import datetime
from typing import List, Sequence, Union

import pandas as pd
from pyspark.sql.types import StructType, TimestampType


def handle_pyspark_timestamp_in_schema(pyspark_schema: StructType) -> StructType:
    """
    Recursively traverses a PySpark schema and converts fields with a 'format' metadata key
    and value of 'date-time' or 'date' to TimestampType.

    Args:
        pyspark_schema (StructType): The PySpark schema to be processed.

    Returns:
        StructType: The updated PySpark schema with converted field types.
    """

    def is_struct_type(field):
        return field.simpleString()[:6] == "struct"

    def is_array_type(field):
        return field.simpleString()[:5] == "array"

    # for each field in schema
    for field in pyspark_schema.fields:
        field_metadata = field.metadata
        if is_struct_type(field.dataType):
            handle_pyspark_timestamp_in_schema(field.dataType)  # type: ignore
        elif is_array_type(field.dataType):
            if is_struct_type(field.dataType.elementType):  # type: ignore
                handle_pyspark_timestamp_in_schema(field.dataType.elementType)  # type: ignore
        # if 'format' is in field metadata key and the value is 'date-time' or 'date'
        # convert field type to TimestampType
        elif "format" in field_metadata.keys():
            field_format = field_metadata["format"]
            if field_format in ("date-time", "date"):
                field.dataType = TimestampType()
    return pyspark_schema


def generate_date_paths(
    base_path: str,
    dates: Union[
        datetime,
        Sequence[Union[Union[str, datetime], List[Union[str, datetime]]]],
    ],
    year_partition: str = "year",
    month_partition: str = "month",
    day_partition: str = "day",
) -> List[str]:
    """
    Generate a list of date paths based on the given parameters.

    Args:
        base_path (str): The base path for the date paths.
        dates (List[Union[Union[str, datetime], List[Union[str, datetime]]]]): A list of dates or date ranges.
            Each date or date range can be provided as a string in the format 'YYYY-MM-DD' or 'YYYY-MM',
            or as a datetime object. Date ranges should be provided as a list of two dates.
        year_partition (str, optional): The name of the year partition. Defaults to "year".
        month_partition (str, optional): The name of the month partition. Defaults to "month".
        day_partition (str, optional): The name of the day partition. Defaults to "day".

    Returns:
        List[str]: A sorted list of date paths in the format '{base_path}/{year_partition}={year}/{month_partition}={month}/{day_partition}={day}'.

    Raises:
        ValueError: If an invalid date format is provided.

    """

    def to_datetime_end_of_period(str_date: str) -> datetime:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", str_date):  # YYYY-MM-DD
            return pd.to_datetime(str_date)
        elif re.match(r"^\d{4}-\d{2}$", str_date):  # YYYY-MM
            return (
                pd.to_datetime(str_date)
                + pd.DateOffset(months=1)
                - pd.DateOffset(days=1)
            )
        elif re.match(r"^\d{4}$", str_date):  # YYYY
            return (
                pd.to_datetime(str_date)
                + pd.DateOffset(years=1)
                - pd.DateOffset(days=1)
            )
        else:
            raise ValueError(
                f"Invalid date format: {str_date}. Valid formats are 'YYYY-MM-DD', 'YYYY-MM', and 'YYYY'."
            )

    if isinstance(dates, datetime):
        dates = [dates]

    paths_set = set()

    for date_item in dates:
        if isinstance(date_item, list):
            if len(date_item) != 2:
                raise ValueError("Each date_range must be a list of two dates")
            start_date = pd.to_datetime(date_item[0])
            if isinstance(date_item[1], str):
                end_date = to_datetime_end_of_period(date_item[1])
            else:
                end_date = date_item[1]
            date_list = pd.date_range(start=start_date, end=end_date)
        else:
            if isinstance(date_item, str):
                start_date = pd.to_datetime(date_item)
                end_date = to_datetime_end_of_period(date_item)
                date_list = pd.date_range(start=start_date, end=end_date)
            else:
                date_list = [date_item]

        for date in date_list:
            year = date.strftime("%Y")
            month = date.strftime("%m")
            day = date.strftime("%d")
            paths_set.add(
                f"{base_path}/{year_partition}={year}/{month_partition}={month}/{day_partition}={day}"
            )

    return sorted(list(paths_set))
