import datetime
from datetime import datetime, timedelta


def today():
    return datetime.today().strftime("%Y-%m-%d")


def day_delta(date_str: str | int, days: int | None = None):
    if isinstance(date_str, int) and not days:
        return day_delta(today(), date_str)

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    new_date_obj = date_obj + timedelta(days=days)
    return new_date_obj.strftime("%Y-%m-%d")
