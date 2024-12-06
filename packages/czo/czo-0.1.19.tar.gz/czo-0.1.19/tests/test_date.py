import datetime
import random
import time

from czo import DateLib

TZ = time.tzname[time.daylight]


def test_1():
    assert DateLib.now_date() == datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def test_2():
    now_date = datetime.datetime.now()
    y = str(now_date.year)
    m = str(now_date.month)
    d = str(now_date.day)
    assert DateLib.now_ymd() == [y, m, d]


def test_3():
    if TZ == "CST":
        assert DateLib.timestamp_to_date(1640995200) == "2022-01-01 08:00:00"
        assert DateLib.timestamp_to_date(1640995200000) == "2022-01-01 08:00:00"
    elif TZ == "UTC":
        assert DateLib.timestamp_to_date(1640995200) == "2022-01-01 00:00:00"
        assert DateLib.timestamp_to_date(1640995200000) == "2022-01-01 00:00:00"


def test_4():
    if TZ == "CST":
        assert DateLib.date_to_timestamp("2022-01-01 12:00:00") == 1641009600
        assert DateLib.date_to_timestamp("2022-01-01 12:00:00", True) == 1641009600000
    elif TZ == "UTC":
        assert DateLib.date_to_timestamp("2022-01-01 12:00:00") == 1641038400
        assert DateLib.date_to_timestamp("2022-01-01 12:00:00", True) == 1641038400000


def test_5():
    yesterday = datetime.date.today() - datetime.timedelta(days=2)
    ms = int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d"))) * 1000
    s = int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d")))
    assert DateLib.yesterday_zero_point_timestamp(2) == s
    assert DateLib.yesterday_zero_point_timestamp(2, True) == ms


def test_6():
    assert (
        DateLib.difference_time_two("2022-01-01 10:00:00", "2022-01-01 12:00:00")
        == 7200
    )
    assert (
        DateLib.difference_time_two("2022-01-01 10:00:00", "2022-01-01 12:00:00", True)
        == -7200
    )


def test_7():
    now_time = datetime.datetime.now()
    now_time = now_time - datetime.timedelta(minutes=int(60))
    assert DateLib.date_before_minutes(60) == now_time.strftime("%Y-%m-%d %H:%M:%S")


def test_8():
    now_time = datetime.datetime.now()
    now_time = now_time - datetime.timedelta(hours=int(24))
    assert DateLib.date_before_hours(24) == now_time.strftime("%Y-%m-%d %H:%M:%S")


def test_9():
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-7)
    assert DateLib.date_before_days(7) == (today + offset).strftime("%Y-%m-%d %H:%M:%S")


def test_10():
    date = datetime.datetime.strptime(
        "2022-01-01T12:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    local_time = date + datetime.timedelta(hours=8)
    assert DateLib.time_handler("2022-01-01T12:00:00.000Z") == local_time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def test_11():
    parsed_date = datetime.datetime.strptime(
        "Sat, 01 Jan 2022 12:00:00 GMT", "%a, %d %b %Y %H:%M:%S %Z"
    )
    parsed_date = parsed_date + datetime.timedelta(hours=8)
    assert DateLib.http_header_time_to_str(
        "Sat, 01 Jan 2022 12:00:00 GMT"
    ) == parsed_date.strftime("%Y-%m-%d %H:%M:%S")


def test_12():
    now = datetime.datetime.now()
    start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    end_of_day = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

    timestamp_tuple = int(start_of_day.timestamp()), int(end_of_day.timestamp())
    date_tuple = str(start_of_day), str(end_of_day)

    assert DateLib.now_start_end() == date_tuple
    assert DateLib.now_start_end(True) == timestamp_tuple


def test_13():
    a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    assert DateLib.fmt_date() == a


def test_14():
    start = datetime.datetime.strptime("2023-01-01 07:08:16", "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime("2023-01-10 07:08:16", "%Y-%m-%d %H:%M:%S")

    start_timestamp = int(start.timestamp())
    end_timestamp = int(end.timestamp())

    random_timestamp = random.randint(start_timestamp, end_timestamp)

    random_date = datetime.datetime.fromtimestamp(random_timestamp)
    date, timestamp = DateLib.generate_random_date_and_timestamp(
        "2023-01-11 07:08:16", "2023-01-12 07:08:16"
    )
    assert random_date.__str__() < date.__str__()
    assert random_timestamp < timestamp
