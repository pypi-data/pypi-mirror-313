import datetime
import random
import time
from typing import Optional, Union
import warnings

from .utils import add_help


@add_help
class DateLib:
    """
    提供了一组静态方法，用于处理日期和时间的常见操作。
    """

    def help() -> None: ...

    @staticmethod
    def timestamp() -> int:
        """
        返回当前时间的时间戳。
        """
        return int(time.time())

    @staticmethod
    def timestamp_ms() -> int:
        """
        返回当前时间的时间戳。
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def now_date() -> str:
        """
        返回当前日期和时间的格式化字符串。

        Returns:
            当前日期和时间的格式化字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> now_date()
            '2022-01-01 12:00:00'
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def now_ymd() -> list:
        """
        返回当前日期的年、月、日。

        Returns:
            包含当前年、月、日的列表。

        Examples:
            >>> now_ymd()
            ['2022', '01', '01']
        """
        now_date = datetime.datetime.now()
        y = str(now_date.year)
        m = str(now_date.month)
        d = str(now_date.day)
        return [y, m, d]

    @staticmethod
    def timestamp_to_date(timestamp) -> str:
        """
        将时间戳转换为日期字符串。

        Args:
            timestamp: 要转换的时间戳。

        Returns:
            转换后的日期字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> timestamp_to_date(1640995200)
            '2022-01-01 00:00:00'
            >>> timestamp_to_date(1640995200000)
            '2022-01-01 00:00:00'
        """
        if len(str(timestamp)) == 13:
            timestamp = int(timestamp) / 1000.0
        return (
            datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
            .astimezone()
            .strftime("%Y-%m-%d %H:%M:%S")
        )

    @staticmethod
    def date_to_timestamp(date, ms=False) -> int:
        """
        将日期转换为时间戳。

        Args:
            date: 要转换的日期，格式为"%Y-%m-%d %H:%M:%S"。
            ms: 是否返回毫秒级时间戳，默认为False。

        Returns:
            转换后的时间戳，单位为秒或毫秒，取决于ms参数的值。

        Examples:
            >>> date_to_timestamp("2022-01-01 12:00:00")
            1641009600
            >>> date_to_timestamp("2022-01-01 12:00:00", ms=True)
            1641009600000
        """
        if ms:
            return (
                int(datetime.datetime.fromisoformat(date).astimezone().timestamp())
                * 1000
            )
        return int(datetime.datetime.fromisoformat(date).astimezone().timestamp())

    @staticmethod
    def yesterday_zero_point_timestamp(day=1, ms=False) -> int:
        """
        返回昨天零点的时间戳。

        Args:
            day: 要减去的天数，默认为1。
            ms: 是否返回毫秒级时间戳，默认为False。

        Returns:
            昨天零点的时间戳，单位为秒或毫秒，取决于ms参数的值。

        Examples:
            >>> yesterday_zero_point_timestamp()
            1640995200
            >>> yesterday_zero_point_timestamp(day=2, ms=True)
            1640908800000
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=day)
        if ms:
            return int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d"))) * 1000
        return int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d")))

    @staticmethod
    def difference_time_two(date1: str, date2: str, reversal: bool = False) -> float:
        """
        计算两个日期之间的时间差（以秒为单位）。

        Args:
            date1: 第一个日期，格式为"%Y-%m-%d %H:%M:%S"。
            date2: 第二个日期，格式为"%Y-%m-%d %H:%M:%S"。
            reversal: 默认使用 date2 - date1 的方式计算时间差，如果为 True，则使用 date1 - date2 的方式计算时间差。

        Returns:
            两个日期之间的时间差，以秒为单位。

        Examples:
            >>> difference_time_two("2022-01-01 10:00:00", "2022-01-01 12:00:00")
            7200.0
        """
        date1 = datetime.datetime.strptime(date1.strip(), "%Y-%m-%d %H:%M:%S")
        date2 = datetime.datetime.strptime(date2.strip(), "%Y-%m-%d %H:%M:%S")
        if reversal:
            date1, date2 = date2, date1
        return (date2 - date1).total_seconds()

    @staticmethod
    def date_before_minutes(value) -> str:
        """
        返回指定分钟数之前的日期和时间。

        Args:
            value: 要减去的分钟数。

        Returns:
            格式化的日期和时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> date_before_minutes(30)
            '2022-01-01 11:30:00'
        """
        now_time = datetime.datetime.now()
        now_time = now_time - datetime.timedelta(minutes=int(value))
        return now_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def date_before_hours(value) -> str:
        """
        返回指定小时数之前的日期和时间。

        Args:
            value: 要减去的小时数。

        Returns:
            格式化的日期和时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> date_before_hours(3)
            '2022-01-01 09:00:00'
        """
        now_time = datetime.datetime.now()
        now_time = now_time - datetime.timedelta(hours=int(value))
        return now_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def date_before_days(day: int) -> str:
        """
        返回指定天数之前的日期和时间。

        Args:
            day: 要减去的天数。

        Returns:
            格式化的日期和时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> date_before_days(7)
            '2022-01-01 12:00:00'
        """
        today = datetime.datetime.now()
        offset = datetime.timedelta(days=-day)
        return (today + offset).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def time_handler(date_str: str) -> str:
        """
        将格式为"%Y-%m-%dT%H:%M:%S.%fZ"的日期字符串转换为格式化的本地时间字符串。

        Args:
            date_str: 要转换的日期字符串。

        Returns:
            格式化的本地时间字符串，格式为"%Y-%m-%d %H:%M:%S"。

        Examples:
            >>> time_handler("2022-01-01T12:00:00.000Z")
            '2022-01-01 20:00:00'
        """
        date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        local_time = date + datetime.timedelta(hours=8)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def http_header_time_to_str(date_str: str):
        """
        将HTTP头时间字符串转换为格式化的日期和时间字符串。

        Args:
            date_str: 要转换的HTTP头时间字符串。

        Returns:
            格式化的日期和时间字符串，格式为"YYYY-MM-DD HH:MM:SS"。

        Examples:
            >>> http_header_time_to_str("Sat, 01 Jan 2022 12:00:00 GMT")
            '2022-01-01 20:00:00'
        """
        # 解析字符串为 datetime 对象
        parsed_date = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        parsed_date = parsed_date + datetime.timedelta(hours=8)
        # 格式化为想要的时间格式
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def now_start_end(timestamp: bool = False) -> tuple:
        """
        返回当前日期的开始和结束时间。

        Args:
            timestamp (bool, 可选): 如果为True，则返回开始和结束时间的时间戳。默认为False。

        Returns:
            tuple: 包含当前日期的开始时间（00:00:00）和结束时间（23:59:59）的元组。如果timestamp为True，则返回开始和结束时间的时间戳。
        """
        # 获取当前日期时间
        now = datetime.datetime.now()
        # 获取当天开始时间（即 00:00:00）
        start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        # 获取当天结束时间（即 23:59:59）
        end_of_day = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
        if timestamp:
            return int(start_of_day.timestamp()), int(end_of_day.timestamp())
        return str(start_of_day), str(end_of_day)

    @staticmethod
    def fmt_date(fmt="%Y-%m-%d %H:%M:%S") -> str:
        """格式化当前时间。方便创建不同的字面量。

        Args:
            fmt (str): 格式. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            str: 当前时间格式化后的时间字符串

        Examples:
            >>> fmt_date()
            "2024-05-13 14:58:18"
        """
        return time.strftime(fmt, time.localtime(int(time.time())))

    @staticmethod
    def generate_random_date_and_timestamp(
        start: datetime.datetime | str, end: datetime.datetime | str
    ) -> tuple[datetime.datetime, int]:
        """
        生成指定范围内的随机日期和时间戳。

        Args:
            start -- 字符串或datetime.datetime对象格式起始日期。
            end -- 字符串或datetime.datetime对象格式结束日期。

        Returns:
            random_date -- 随机日期，datetime.datetime 对象。
            random_timestamp -- 随机日期对应的时间戳，int 类型。

        Examples:

            >>> start_date = "2024-01-10 07:08:16"
            >>> end_date = "2024-06-10 07:08:16"
            >>> random_date, random_timestamp = DateLib.generate_random_date_and_timestamp(start_date, end_date)
            ...
            >>> random_date, random_timestamp = DateLib.generate_random_date_and_timestamp(*DateLib.get_dates_offset_by_days(-3))
        """

        if isinstance(start, str) and isinstance(end, str):
            start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

        if start > end:
            warnings.warn(
                f"开始时间：{start} 早于结束时间：{end}，已自动交换，这可能不符合预期！",
                stacklevel=2,
            )
            start, end = end, start

        start_timestamp = int(start.timestamp())
        end_timestamp = int(end.timestamp())

        random_timestamp = random.randint(start_timestamp, end_timestamp)

        # 将随机时间戳转换回日期
        random_date = datetime.datetime.fromtimestamp(random_timestamp).astimezone()
        return random_date, random_timestamp

    @staticmethod
    def get_dates_offset_by_days(
        day: int,
        now: Optional[Union[str, datetime.datetime]] = None,
        date_ok: bool = False,
    ) -> tuple[str, str]:
        """
        获取指定日期与当前日期之间的偏移日期，以字符串格式返回。

        Args:
            day (int): 与当前日期的偏移天数，负数表示过去，正数表示未来。
            now (Optional[Union[str, datetime.datetime]]): 参考日期，默认为当前时间。如果为字符串，需符合 '%Y-%m-%d %H:%M:%S' 格式。
            date_ok (bool): 是否仅返回日期（无时间）。

        Returns:
            tuple[str, str]: 包含两个日期字符串的元组，第一个为偏移后的日期，第二个为参考日期。

        Examples:
            >>> print(DateLib.get_dates_offset_by_days(-7))
            ('2024-11-28 11:06:13', '2024-12-04 11:06:13')
            >>> print(DateLib.get_dates_offset_by_days(-7, "2024-12-20 00:02:00"))
            ('2024-12-14 00:02:00', '2024-12-20 00:02:00')
        """
        if isinstance(now, str):
            today = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        elif isinstance(now, datetime.datetime):
            today = now
        else:
            today = datetime.datetime.now()

        # 创建一个时间偏移量，用于计算过去某一天的日期
        offset = datetime.timedelta(days=day)

        fmt = "%Y-%m-%d" if date_ok else "%Y-%m-%d %H:%M:%S"

        past = (today + offset).strftime(fmt)
        today = today.strftime(fmt)
        return (past, today)
