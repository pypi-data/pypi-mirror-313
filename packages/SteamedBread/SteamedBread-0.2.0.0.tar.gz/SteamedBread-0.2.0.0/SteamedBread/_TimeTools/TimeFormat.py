"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: TimeFormat.py
@Time: 2023/12/9 18:00
"""

import calendar
import time
from datetime import datetime

from dateutil import parser


class TimeFormat:
    def __init__(self, dt=None):
        dt = dt or time.time()
        if isinstance(dt, datetime):
            self.date = datetime
        elif isinstance(dt, float):
            self.date = datetime.fromtimestamp(dt)
        elif isinstance(dt, str):
            self.date = parser.parse(timestr=dt)

    def __add__(self, other):
        """
            将两个datetime对象相加，需要首先将它们转换为时间间隔

            other = TimeFormat("00:30") - TimeFormat("01:30")
        :param other: 时间间隔
        :return:
        """
        self.date = other.date + self.date
        return self

    def __sub__(self, other):
        """
            将它们转换为时间间隔
        :param other: 时间间隔
        :return:
        """
        self.date -= other.date
        return self

    def __gt__(self, other):
        """
        两个对象进行比较大小, greater than
        :param other: 另一个对象
        :return:
        """
        return self.date > other.date

    def __lt__(self, other):
        """
        两个对象进行比较大小, less than
        :param other: 另一个对象
        :return:
        """
        return self.date < other.date

    @staticmethod
    def flash_back(days=1, month=0, weeks=0, years=0) -> datetime:
        """
        时间回溯器、时光穿越机
        :param days: 回溯 < 0, 穿越 > 0
        :param month: 回溯 < 0, 穿越 > 0
        :param weeks: 回溯 < 0, 穿越 > 0
        :param years: 回溯 < 0, 穿越 > 0
        :return: datetime
        """
        future = 0
        if days:
            future += days * 86400
        if month:
            today = datetime.today()
            month_range = calendar.monthrange(today.year, today.month)[1]
            future += month * month_range * 86400
        if weeks:
            future += weeks * 7 * 86400
        if years:
            future += years * 365 * 86400
        return datetime.fromtimestamp(int(str(int(future + time.time()))[:10]))
