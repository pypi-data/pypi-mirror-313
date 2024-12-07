import datetime
from dataclasses import is_dataclass, asdict
from enum import Enum


def as_serializable_dict(obj):
    """Convert a dataclass to a JSON-serializable dictionary."""
    if not is_dataclass(obj):
        raise TypeError(f"Object {obj} is not a dataclass instance.")

    def serialize(value):
        if isinstance(value, datetime.datetime):
            return value.isoformat()  # Convert datetime to ISO 8601 string
        elif isinstance(value, Enum):
            return value.value  # Convert Enum to its value
        elif isinstance(value, list):
            return [serialize(v) for v in value]  # Recursively serialize lists
        elif isinstance(value, dict):
            return {k: serialize(v) for k, v in
                    value.items()}  # Serialize dictionaries
        elif is_dataclass(value):
            return as_serializable_dict(
                value)  # Recursively serialize nested dataclasses
        return value  # Return other types as-is

    return {key: serialize(value) for key, value in asdict(obj).items()}