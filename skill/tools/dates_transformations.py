import datetime

from dateutil import relativedelta


def adjust_relative_dates(
    *, initial_date: datetime.datetime, yandex_dict: dict
) -> datetime.datetime:
    if "value" in yandex_dict:
        yandex_dict = yandex_dict["value"]
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


def adjust_absolute_dates(
    *, initial_date: datetime.datetime, yandex_dict: dict
) -> datetime.datetime:
    if "value" in yandex_dict:
        yandex_dict = yandex_dict["value"]
    adjusted_date = initial_date
    if yandex_dict.get("year_is_relative", False) is False:
        adjusted_date = adjusted_date.replace(year=yandex_dict.get("year", 0))

    if yandex_dict.get("month_is_relative", False) is False:
        adjusted_date = adjusted_date.replace(month=yandex_dict.get("month", 0))

    if yandex_dict.get("day_is_relative", False) is False:
        adjusted_date = adjusted_date.replace(day=yandex_dict.get("day", 0))

    if yandex_dict.get("hour_is_relative", False) is False:
        adjusted_date = adjusted_date.replace(hour=yandex_dict.get("hour", 0))

    if yandex_dict.get("minute_is_relative", False) is False:
        adjusted_date = adjusted_date.replace(minute=yandex_dict.get("minute", 0))

    if yandex_dict.get("second_is_relative", False) is False:
        adjusted_date = adjusted_date.replace(second=yandex_dict.get("second", 0))

    return adjusted_date


def transform_yandex_datetime_value_to_datetime(
    yandex_datetime_value_dict,
) -> datetime.datetime:
    return adjust_absolute_dates(
        initial_date=adjust_relative_dates(
            initial_date=datetime.datetime.now(), yandex_dict=yandex_datetime_value_dict
        ),
        yandex_dict=yandex_datetime_value_dict,
    )
