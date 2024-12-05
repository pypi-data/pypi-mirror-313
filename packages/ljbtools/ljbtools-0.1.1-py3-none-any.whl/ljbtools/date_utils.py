#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   date_utils.py.py
# @Time    :   2022/7/13 16:44
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :

# here put the import lib
import datetime
import time


def now_timestamp():
    """
    返回当前的毫秒级时间戳
    :return:
    """
    return int(time.time() * 1000)


def now_date(_str=True, zero=True, time_format='%Y-%m-%d %H:%M:%S'):
    """

    :param _str:
    :param zero:
    :param time_format:
    :return:
    """
    _now = datetime.datetime.now()

    if zero:
        _now = datetime.datetime.strptime(
            _now.strftime('%Y-%m-%d'), '%Y-%m-%d')

    if _str:
        _now = _now.strftime(time_format)

    return _now


def get_datetime(day=None, date_format='%Y-%m-%d'):
    """

    :param day:
    :param date_format:
    :return: datetime
    """
    if day is None:
        return now_date(_str=False)
    return datetime.datetime.strptime(day, date_format)


def date_add_timedelta(value: int, _type='days'):
    """

    :param value:
    :param _type:  day hour minute
    :return:
    """
    today = datetime.datetime.now()
    if _type == 'hours':
        offset = datetime.timedelta(hours=value)
    elif _type == 'minutes':
        offset = datetime.timedelta(minutes=value)
    else:
        offset = datetime.timedelta(days=value)
    return (today + offset).strftime('%Y-%m-%d %H:%M:%S')


def timestamp_to_datetime_str(timestamp):
    """
    :param timestamp:
    :return:
    """
    if len(str(timestamp)) == 13:
        timestamp = int(timestamp) / 1000.0
    time_array = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def datetime_str_to_timestamp(tss):
    """
    把 年月日时分 转换为 时间戳格式
        :param tss: str
        :return: timeStamp:int
        """
    time_array = time.strptime(tss, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_array))


def chg_timestamp_to_datetime(timestamp, pek_timezone=True):
    """
    timestamp -> datetime 1579246559 -> 2020-01-17 07:35:59
    """
    timestamp = int(timestamp)
    if timestamp > 1000000000000:
        timestamp = int(timestamp / 1000)
    date_array = datetime.datetime.utcfromtimestamp(timestamp)
    # pek timezone +8 hour
    if pek_timezone:
        date_array += datetime.timedelta(hours=8)
    return date_array


def now_ymd() -> tuple:
    """
    获取当前 年，月，日
    :return: tuple:(年,月,日)
    """
    _now = datetime.datetime.now()
    return _now.year, _now.month, _now.day


def java_date(date, to_format="%Y-%m-%d %H:%M:%S", timezone="CST"):
    """ java时间格式转换为python日期格式
    %a: 星期的缩写
    %b: 月份英文名的缩写
    %d: 日期(以01-31来表示)
    %Y: 年份(以四位数来表示)
    :param:　data:　Fri May 18 15:46:24 CST 2016
    :param:  timezone：时区 "CST"
    :return: to_format="%Y-%m-%d %H:%M:%S"
    """
    data_format = "%a %b %d %H:%M:%S {} %Y".format(timezone)
    time_struct = time.strptime(str(date), data_format)
    ctime = time.strftime(to_format, time_struct)
    return ctime
