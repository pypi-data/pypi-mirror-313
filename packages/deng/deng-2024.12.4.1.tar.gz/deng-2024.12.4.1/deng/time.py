import time
import math
import datetime
from typing import Union


def get_timestamp(length: int = 10, utc=False) -> int:
    """获取系统时间时间戳"""
    assert length in (10, 13), "时间戳长度参数错误，只有10位与13位时间戳"
    if utc:
        current_timestamp = datetime.datetime.utcnow().timestamp()
    else:
        current_timestamp = datetime.datetime.now().timestamp()
    return int(str(current_timestamp * 1000)[:length])


def get_current_time(
    _format: str = "long", offset: int = 0, sep1="-", sep2=":", **kwargs
) -> str:
    if not isinstance(offset, int):
        raise ValueError(f"offset参数非法，预期为int类型，实际为{type(offset)}")

    now_time = datetime.datetime.now()
    target_time = now_time - datetime.timedelta(seconds=offset)
    if _format.lower() == "short":
        return target_time.strftime(f"%Y{sep1}%m{sep1}%d")
    elif _format.lower() == "long":
        return target_time.strftime(f"%Y{sep1}%m{sep1}%d %H{sep2}%M{sep2}%S")
    elif _format.lower() == "max":
        return target_time.strftime(f"%Y{sep1}%m{sep1}%d %H{sep2}%M{sep2}%S.%f")
    else:
        return target_time.strftime(_format)


def str_to_time(time_str: str, _format="long") -> Union[datetime.datetime, datetime.date]:
    if not time_str:
        raise ValueError(f"time_str参数非法：{time_str}")

    if _format == "long":
        return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    else:
        day = datetime.datetime.strptime(time_str, "%Y-%m-%d")
        return day.date()


def time_to_str(_time: datetime.datetime, _format="long") -> str:
    if _format == "long":
        return _time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return _time.strftime("%Y-%m-%d")


def timestamp_to_str(timestamp: int, fmt="%Y-%m-%d %H:%M:%S") -> str:
    """时间戳转换时间字符串"""
    if len(str(timestamp)) == 13:
        current_time = math.floor(int(timestamp) / 1000)
        return time.strftime(fmt, time.localtime(current_time))
    elif len(str(timestamp)) == 10:
        return time.strftime(fmt, time.localtime(int(timestamp)))
    else:
        raise ValueError(f"时间戳格式错误：{timestamp}")


def str_to_timestamp(time_str: str, fmt: str) -> float:
    """时间字符串转换时间戳"""
    time_obj = datetime.datetime.strptime(time_str, fmt)
    return time_obj.timestamp()
