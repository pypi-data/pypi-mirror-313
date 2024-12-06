"""
author: 馒头
email: neihanshenshou@163.com
"""


class QuoteFormat:

    @staticmethod
    def random_quote(show=False):
        """
        随机 毒鸡汤语录
        """
        from SteamedBread import get
        quote = get(url="https://api.oick.cn/dutang/api.php", show=show).json()
        return quote
