"""
author: 馒头
email: neihanshenshou@163.com
"""

from typing import Any, Literal
from typing import Callable
from typing import Optional
from typing import Sequence
from typing import Union

import allure
import pytest

_ScopeName = Literal["session", "package", "module", "class", "function"]


def fixture(scope: "Union[_ScopeName, Callable[[str, []], _ScopeName]]" = "function",
            params=None,
            autouse: bool = False,
            ids: Optional[
                Union[Sequence[Optional[object]], Callable[[Any], Optional[object]]]
            ] = None,
            name: Optional[str] = None):
    return pytest.fixture(
        scope=scope,
        params=tuple(params) if params is not None else None,
        autouse=autouse,
        ids=None if ids is None else ids if callable(ids) else tuple(ids),
        name=name
    )


def case_title(title):
    """
    用例标题文案
    """

    def inner(func):
        return allure.title(test_title=title)(func)

    return inner


def case_step(desc):
    """
    用例步骤描述
    :param desc: 步骤描述
    """

    from SteamedBread import logger
    logger.step(msg=desc)
    return allure.step(title=desc)


def case_severity(level):
    """
    用例优先级、重要级别
    """

    def inner(func):
        return allure.severity(severity_level=level)(func)

    return inner


def case_tag(*tags):
    """
    用例标签
    """

    def inner(func):
        return allure.tag(*tags)(func)

    return inner


def case_feature(*features):
    """
    用例特性
    """

    def inner(func):
        return allure.feature(*features)(func)

    return inner


def case_story(*stories):
    """
    用例描述
    """

    def inner(func):
        return allure.story(*stories)(func)

    return inner


def case_attach(body, name=None, attachment_type=allure.attachment_type.TEXT):
    """
    用例附件
    """
    return allure.attach(
        body=body,
        name=name,
        attachment_type=attachment_type
    )


def case_skip(reason: str = ...):
    """
    用例 任意情况下跳过执行
    """
    return pytest.mark.skip(reason=reason)


def case_skip_if(condition, *conditions, reason):
    """
    用例 满足条件跳过执行
    """
    return pytest.mark.skipif(condition=condition, conditions=conditions, reason=reason)


def case_desc_html(content):
    """
    用例描述文案默认提示
    """

    def inner(func):
        return allure.description_html(test_description_html=content)(func)

    return inner


def case_desc_ok(content: str):
    """
    用例描述文案绿色提示
    """

    def inner(func):
        new_content = ('<h2>'
                       '<span>Tip:【用例正常运行】</span>'
                       '</h2>')
        for index, each in enumerate(content.split(';')):
            new_content += f'<h3 style="color: #2bbf02">{index + 1}. {each}</h3>'
        return allure.description_html(test_description_html=new_content)(func)

    return inner


def case_desc_error(content: str):
    """
    用例描述文案红色提示
    """

    def inner(func):
        new_content = ('<h2>'
                       '<span>Tip:【用例发现缺陷】</span>'
                       '</h2>')
        for index, each in enumerate(content.split(';')):
            new_content += f'<h3 style="color: #ff0011">{index + 1}. {each}</h3>'
        return allure.description_html(test_description_html=new_content)(func)

    return inner


def case_desc_up(content: str):
    """
    用例描述文案警告色提示
    """

    def inner(func):
        new_content = ('<h2>'
                       '<span>Tip:【用例可持续优化】</span>'
                       '</h2>')
        for index, each in enumerate(content.split(';')):
            new_content += f'<h3 style="color: #f0bb0e">{index + 1}. {each}</h3>'
        return allure.description_html(test_description_html=new_content)(func)

    return inner


def case_priority(order=0):
    """
    用例执行的优先级, 其中 0 的优先级最高, 比负数、正数都高
    example:

        @priority(order=2)
        def test_01():
            pass

        @priority(order=1)
        def test_02():
            pass

    actual order is: test_02 -> test_01
    """

    def inner(func):
        return pytest.mark.run(order=order)(func)

    return inner
