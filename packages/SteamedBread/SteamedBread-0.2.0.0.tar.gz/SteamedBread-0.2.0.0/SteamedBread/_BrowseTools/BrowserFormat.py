"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: BrowserFormat.py
@Time: 2023/12/27 21:19
"""

import os
import time

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver import Chrome
from selenium.webdriver import Edge
from selenium.webdriver import Remote
from selenium.webdriver import Safari
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.service import Service


class ReuseBrowser(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dict like {}")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.caps = {} and options.Options().to_capabilities()
        self.session_id = self.r_session_id


class StartBrowser:

    def __init__(self, capabilities=None):
        self.capabilities = capabilities
        self._session_cache_path = os.path.join(os.path.dirname(__file__), "browser_session.yaml")
        self.driver = self.__start_session
        self._expect_driver = ...

    def _session_cache_get(self):
        _session_cache = {}
        if os.path.exists(self._session_cache_path):
            from SteamedBread import FileOperate
            _session_cache = FileOperate.read_file(filename=self._session_cache_path, jsonify=True, yamlify=True)

        return _session_cache

    def __start_session(self, browser_type: str = "Chrome", **kwargs):
        """
        :param browser_type: 浏览器类型 - Chrome、Edge、Safari 目前支持三类，但均需要自行下载驱动(不建议使用Edge)
        :param kwargs: executable_path - 浏览器驱动执行路径，建议配置为环境变量 一劳永逸
        :param kwargs: headless - 无头模式
        :param kwargs: wap - 是否开启wap模式
        :param kwargs: width - 开启wap模式后的宽度
        :param kwargs: height - 开启wap模式后的高度
        :param kwargs: options - 自定义option.Options()
        """
        from SteamedBread import logger

        _session = self._session_cache_get()
        self.capabilities = kwargs.get("caps")
        headless = kwargs.get("headless", False)
        wap = kwargs.get("wap", False)
        width, height = kwargs.get("width", 375), kwargs.get("height", 776)
        browser_type = browser_type.upper()

        try:
            if browser_type == "SAFARI":
                logger.warning("⚠️ ⚠️ It Seems That You Want To Use Safari Browser. "
                               "Please Don't Use By.Id To Find AN Element")
            self._expect_driver = ReuseBrowser(
                command_executor=_session.get("executor_url"),
                session_id=_session.get("session_id")
            )
            self._expect_driver.refresh()
            logger.info("✅ [Congratulation] Current Browser Session Cache Is Enable!")
        except Exception as e:
            logger.warning(f"[Ignore] {e.args[0] if len(e.args) else e.args}")
            _options = kwargs.get("options", options.Options())
            from SteamedBread import FileOperate
            if browser_type == "CHROME":
                if headless:
                    _options.headless = True
                if isinstance(self.capabilities, options.Options):
                    self.capabilities = self.capabilities.to_capabilities()
                if wap:
                    # 设置用户代理为iPhone的用户代理
                    _options.add_argument(("user-agent=Mozilla/5.0 "
                                           "(iPhone; CPU iPhone OS 14_0 like Mac OS X) "
                                           "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 "
                                           "Mobile/15E148 Safari/604.1"))

                    # 设置窗口大小为手机屏幕的大小 (例如 iPhone 6/7/8)
                    _options.add_argument(f"window-size={width},{height}")
                self._expect_driver = Chrome(
                    desired_capabilities=self.capabilities,
                    options=_options,
                    service=Service("chromedriver", 0, None, None)
                )

            elif browser_type == "SAFARI":
                if headless:
                    logger.warning("⚠️ ⚠️ Safari Browser Does Not Support Headless Mode For The Time Being.")
                self._expect_driver = Safari(desired_capabilities=self.capabilities)

            elif browser_type == "EDGE":
                executable_path = kwargs.get("executable_path", "msedgedriver")
                capabilities = {}
                if headless:
                    capabilities = {"ms:edgeOptions": {
                        'args': ['--headless']
                    }}
                self._expect_driver = Edge(capabilities=capabilities, executable_path=executable_path)
            else:
                raise EnvironmentError("Only Support Browser Is [Chrome、Safari、Edge] Now")

            FileOperate.write_file(
                filename=self._session_cache_path,
                data={
                    "session_id": self._expect_driver.session_id,
                    "executor_url": self._expect_driver.service.service_url,
                    "timestamp": time.strftime("%F %T")
                }
            )
        time.sleep(0.7)
        return self._expect_driver


Browser = StartBrowser().driver
