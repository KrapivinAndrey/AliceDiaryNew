import datetime

from diary.skill.tools.dates_transformations import (
    transform_yandex_datetime_value_to_datetime as ya_transform,
)
from alicefluentcheck import AliceEntity

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)


def test_today():

    entity = AliceEntity().datetime(day=0, day_is_relative=True).val["value"]
    result = ya_transform(entity)
    assert result.strftime("%d.%m.%Y") == today.strftime("%d.%m.%Y")


def test_yesterday():

    entity = AliceEntity().datetime(day=-1, day_is_relative=True).val["value"]
    result = ya_transform(entity)
    assert result.strftime("%d.%m.%Y") == yesterday.strftime("%d.%m.%Y")


def test_tomorrow():

    entity = AliceEntity().datetime(day=1, day_is_relative=True).val["value"]
    result = ya_transform(entity)
    assert result.strftime("%d.%m.%Y") == tomorrow.strftime("%d.%m.%Y")


def test_absolute():
    entity = AliceEntity().datetime(day=1, month=1, year=2020).val["value"]
    result = ya_transform(entity)
    assert result.strftime("%d.%m.%Y") == "01.01.2020"
