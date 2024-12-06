
import datetime
from typing import Dict, List, Any, Union, Set,Optional
import uuid


def list_as_strings(*enums):
    """Converts a list of Enum members to their string values."""
    return [str(enum) for enum in enums]

def val_as_string(value):
    """
    Converts various data types to a string representation.
    """
    if isinstance(value, datetime.datetime):
        return value.isoformat()  # Example: '2024-08-16T14:30:00'
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')  # Date-only format
    elif isinstance(value, datetime.time):
        return value.strftime('%H:%M:%S')  # Time-only format
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        return f"{value:.5f}"  # Convert float with six decimal places (adjust precision as needed)
    elif isinstance(value, bool):
        return "True" if value else "False"
    elif value is None:
        return ""  # Return an empty string for NoneType
    else:
        return str(value)  # Fallback for other types




def filter_records(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    column_to_filter_on: str,
    values_to_filter: Set[Any],
) -> List[Dict[str, Any]]:
    """
    Filters records based on a provided column and values, 
    with early type checking and handling for empty data.

    Args:
        data (Union[Dict[str, Any], List[Dict[str, Any]]]): Input data.
        column_to_filter_on (str): Filtering column name.
        values_to_filter (Set[Any]): Values to filter against.

    Returns:
        List[Dict[str, Any]]: Filtered records.

    Raises:
        TypeError: If a type mismatch is detected during the early check.
    """

    if isinstance(data, dict):
        data = [data]

    # Handle empty data
    if not data:
        return []

    # If values_to_filter is empty, no filtering needed
    if not values_to_filter:
        return data

    # Early Type Check using only the first value in the set
    first_record_value = data[0].get(column_to_filter_on)
    
    if first_record_value is None:
        raise ValueError(f"Column '{column_to_filter_on}' not found in the data.")

    filter_value_type = type(first_record_value)

    # Check the type of the first value in values_to_filter
    first_filter_value = next(iter(values_to_filter))
    if not isinstance(first_filter_value, filter_value_type):
        raise TypeError(
            f"Type mismatch detected: column '{column_to_filter_on}' has values of type "
            f"{filter_value_type}, but 'values_to_filter' contains values of type {type(first_filter_value)}."
        )

    # Filtering: No type conversion, just filtering
    filtered_records = [
        record
        for record in data
        if record[column_to_filter_on] not in values_to_filter
    ]

    return filtered_records



def company_seed_uuid() -> str:
    """
    Returns Future Edge Group's Seed UUID which was generated using:
    uuid.uuid5(uuid.NAMESPACE_DNS, "ftredge.com")
    """
    return "d0a97da8-66c8-5946-ab48-340ef927b0ff"


def generate_reproducible_uuid_for_namespace(namespace: uuid.UUID | str, seed_description: str, prefix:Optional[str]=None) -> str:
    """
    Generates a reproducible UUID based on the input namespace (UUID object or string) and seed_description.
    For reproducibility, ensure the same namespace and seed_description are used.
    """
    if isinstance(namespace, str):
        namespace = uuid.UUID(namespace)  # Convert string to uuid.UUID object
    if prefix:
        return f"{prefix}_{str(uuid.uuid5(namespace, seed_description))}"
    return str(uuid.uuid5(namespace, seed_description))
