from datetime import datetime

from dateutil import relativedelta


def adjust_relative_dates(yandex_dict: dict) -> datetime:
    initial_date = datetime.today()
    relative_year = (
        yandex_dict["year"] if yandex_dict.get("year_is_relative", False) else 0
    )

    relative_month = (
        yandex_dict["month"] if yandex_dict.get("month_is_relative", False) else 0
    )

    relative_day = (
        yandex_dict["day"] if yandex_dict.get("day_is_relative", False) else 0
    )

    relative_hour = (
        yandex_dict["hour"] if yandex_dict.get("hour_is_relative", False) else 0
    )

    relative_minute = (
        yandex_dict["minute"] if yandex_dict.get("minute_is_relative", False) else 0
    )

    relative_second = (
        yandex_dict["second"] if yandex_dict.get("second_is_relative", False) else 0
    )
    return initial_date + relativedelta.relativedelta(
        years=relative_year,
        months=relative_month,
        days=relative_day,
        hours=relative_hour,
        minutes=relative_minute,
        seconds=relative_second,
    )


def adjust_absolute_dates(yandex_dict: dict) -> datetime:
    adjusted_date = datetime.today()
    if "year" in yandex_dict:
        adjusted_date = adjusted_date.replace(year=yandex_dict.get("year", 0))

    if "month" in yandex_dict:
        adjusted_date = adjusted_date.replace(month=yandex_dict.get("month", 0))

    if "day" in yandex_dict:
        adjusted_date = adjusted_date.replace(day=yandex_dict.get("day", 0))

    if "hour" in yandex_dict:
        adjusted_date = adjusted_date.replace(hour=yandex_dict.get("hour", 0))

    if "minute" in yandex_dict:
        adjusted_date = adjusted_date.replace(minute=yandex_dict.get("minute", 0))

    if "second" in yandex_dict:
        adjusted_date = adjusted_date.replace(second=yandex_dict.get("second", 0))

    return adjusted_date


def transform_yandex_datetime_value_to_datetime(
    yandex_datetime,
) -> datetime:
    relative = (
        yandex_datetime.get("year_is_relative", False)
        or yandex_datetime.get("month_is_relative", False)
        or yandex_datetime.get("day_is_relative", False)
        or yandex_datetime.get("hour_is_relative", False)
        or yandex_datetime.get("minute_is_relative", False)
        or yandex_datetime.get("second_is_relative", False)
    )

    if relative:

        return adjust_relative_dates(yandex_datetime)

    else:
        return adjust_absolute_dates(yandex_datetime)
