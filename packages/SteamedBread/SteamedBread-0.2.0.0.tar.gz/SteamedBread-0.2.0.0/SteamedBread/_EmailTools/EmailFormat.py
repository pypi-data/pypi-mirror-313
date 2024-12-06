"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: EmailFormat.py
@Time: 2023/12/9 18:00
"""

import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Email:

    def __init__(self, receiver=None):
        """
        一些初始化的信息
            Email(
                receiver=['478693360@qq.com']
            ).bedeck_report_html(
                data={"total": 100, "passed": 95, "fail": 3, "error": 1, "skip": 2, "rate": 95, "duration": "13秒"}
            )
        """

        self.smtp = 'smtp.163.com'  # 邮箱服务器地址
        self.username = 'neihanshenshou@163.com'  # 发件人地址
        self.password = "YWYGLQNOPLWNNJJY"  # 授权码

        self.subject = '自动化测试报告'  # 邮件主题
        self.sender = 'neihanshenshou@163.com'  # 发件人
        if isinstance(receiver, list):
            self.receiver = receiver
        elif isinstance(receiver, str):
            self.receiver = receiver.split(",")

    @staticmethod
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def message_init(self, html):
        """
        对即将发送的内容进行初始化
        :param html: 发送邮件正文内容
        :return:
        """
        message = MIMEMultipart()  # 内容接收池
        message['subject'] = Header(self.subject, 'utf-8')
        message['From'] = self._format_addr('馒头 <%s>' % self.sender)
        message['To'] = ', '.join(self.receiver)
        # 解决乱码，html是html格式的字符串
        message_content = MIMEText(html, _subtype='html', _charset='utf-8')
        # 邮件的正文内容
        message.attach(message_content)

        return message

    def send_email(self, html):
        """
        发送邮件
        :param html: 邮件正文内容
        """
        try:
            # 连接邮箱的服务器及端口号
            smtp_obj = smtplib.SMTP(self.smtp, 25)  # smtp服务器端口默认是25
            # 登录邮箱：用户名及密码
            smtp_obj.login(self.username, self.password)
            # 发送邮件
            smtp_obj.sendmail(self.sender, self.receiver, self.message_init(html).as_string())
            print('邮件发送成功')
            smtp_obj.quit()  # 关闭服务器
        except Exception as e:
            raise Exception('邮件发送失败：{}'.format(e))

    @staticmethod
    def _rich_txt_html(url, total, passed, fail, error, skip, color, rate, duration):
        return f"""
            <table border="1px" width="330" align="center" cellspacing="0">
                <h1 align="center">自动化测试报告【{time.strftime("%F")}】</h1>
                <tr align="center">
                    <td>维度统计</td>
                    <td><a href="{url}" style="text-decoration:none">详情(点击查看)</a></td>
                </tr>
                <tr align="center">
                    <td>用例总数</td>
                    <td><b>{total}</b></td>
                </tr>
                <tr align="center">
                    <td>用例通过</td>
                    <td style="color: green"><b>{passed}</b></td>
                </tr>
                <tr align="center">
                    <td>用例失败</td>
                    <td style="color: orange"><b>{fail}</b></td>
                </tr>
                <tr align="center">
                    <td>用例跳过</td>
                    <td style="color: gray"><b>{skip}</b></td>
                </tr>
                <tr align="center">
                    <td>用例错误</td>
                    <td style="color: red"><b>{error}</b></td>
                </tr>
                <tr align="center">
                    <td>成功率</td>
                    <td style="color: {color}"><b>{rate}%</b></td>
                </tr>
                <tr align="center">
                    <td>执行时长</td>
                    <td><b>{duration}</b></td>
                </tr>
            </table>
        """

    def bedeck_report_html(self, data: dict):
        """
            修饰测试报告html文案
        Args:
            data: {
                    "url": "http://localhost:7021/",
                    "total": 10,
                    "passed": 9,
                    "fail": 1,
                    "skip": 0,
                    "error": 0,
                    "rate": "90%",
                    "duration": "1秒"
                }
        Returns:

        """
        report_url = data.get("url", "https://github.com/neihanshenshou/SteamedBread/blob/master/README.md")
        total = data.get("total", 0)
        passed = data.get("pass", 0)
        fail = data.get("fail", 0)
        skip = data.get("skip", 0)
        error = data.get("error", 0)
        rate = data.get("rate", 0) or passed / total * 100
        duration = data.get("duration", "未统计时间")
        if rate == 100:
            color = "green"
        elif rate < 90:
            color = "red"
        else:
            color = "orange"

        message = self._rich_txt_html(
            url=report_url,
            total=total,
            passed=passed,
            fail=fail,
            error=error,
            skip=skip,
            color=color,
            rate=f"{rate:.2f}",
            duration=duration
        )
        self.send_email(html=message)
        return message
