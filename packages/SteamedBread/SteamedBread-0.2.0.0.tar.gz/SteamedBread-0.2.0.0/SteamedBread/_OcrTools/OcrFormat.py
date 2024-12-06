"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: OcrFormat.py
@Time: 2024/2/2 21:36
"""

import requests


class OcrFormat:

    @staticmethod
    def ocr_word(filename: str = "", show=True):
        """
        识别图片中的文字
        :param filename: 图片的文件路径
        :param show: 展示结果
        :return:
        """

        response = requests.post(
            url="https://api.oioweb.cn/api/ocr",
            files={"file": open(file=filename, mode="rb", encoding=None)},
            verify=False
        )
        try:
            word = response.json().get("result", [])
        except Exception as e:
            word = [] and e

        if show and word:
            print(f"识别到的字符: {word}")
        return word
