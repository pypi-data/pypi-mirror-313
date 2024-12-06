from datetime import datetime
from typing import Union


def get_datetime_from_data(input_datetime: Union[datetime, str]):
    if isinstance(input_datetime, datetime):
        return input_datetime
    elif isinstance(input_datetime, str):
        return datetime.fromisoformat(input_datetime)
    return None