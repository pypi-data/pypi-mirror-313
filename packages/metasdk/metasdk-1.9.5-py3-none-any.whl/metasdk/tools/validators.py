from datetime import datetime

from metasdk.exceptions import BadParametersError


def check_postgres_datetime_with_tz(value):
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        raise BadParametersError(f"Datetime should match format '%Y-%m-%dT%H:%M:%S.%f%z': {value}")


def check_postgres_datetime_without_tz(value):
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise BadParametersError(f"Datetime should match format '%Y-%m-%dT%H:%M:%S': {value}")


def check_postgres_date(value):
    value = value.split("T")[0]
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise BadParametersError(f"Date should match format '%Y-%m-%d': {value}")