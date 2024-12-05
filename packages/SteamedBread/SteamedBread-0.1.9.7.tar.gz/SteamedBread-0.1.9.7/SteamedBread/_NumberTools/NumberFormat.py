"""
author: 馒头
email: neihanshenshou@163.com
"""


class NumberTools:

    @staticmethod
    def point(number, rate=2):
        """
        :param number: 数字
        :param rate: 小数位
        :return point(1, 3) = 1.000
        """
        if not isinstance(number, (int, float,)):
            try:
                number = float(number)
            except Exception as e:
                if isinstance(number, str):
                    if number.isalnum():
                        number = ord(number)
                        return f"{number:.{rate}f}"
                raise "请输入数字 或者可转换为数字的字符" and e
        return f"{number:.{rate}f}"

    @staticmethod
    def percent(number, rate=2):
        """
        :param number: 数字
        :param rate: 小数位 默认为2
        :return
            point(1) = 1.00%
            point(100) = 100.00%
        """

        return f"{NumberTools.point(number=number, rate=rate)}%"
