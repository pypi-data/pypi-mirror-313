__version__ = "1.0.10"

from datetime import timedelta, datetime
from typing import Literal, Union, List
from clicknium import clicknium as cc, locator, ui
from BotniumPlus.logger import logger
from BotniumPlus.common.models import RpaException
from time import sleep
from clicknium.common.enums import *
from clicknium.core.models.uielement import UiElement, MouseLocation
from clicknium.locator import _Locator

def init():
    cc.config.disable_telemetry()
    pass

def wait_appear(
    _locator,
    locator_variables: dict = {},
    wait_timeout: int = 30
    ):
    logger.debug('开始等待元素出现 - {}'.format(str(_locator)))
    result = cc.wait_appear(_locator, locator_variables, wait_timeout)
    logger.debug('结束等待元素出现 - {}，是否存在：{}'.format(str(_locator), ('是' if result else '否')))
    return result

def wait_disappear(
    _locator,
    locator_variables: dict = {},
    wait_timeout: int = 30
    ):
    logger.debug('开始等待元素消失 - {}'.format(str(_locator)))
    exists = cc.is_existing(_locator, locator_variables, timeout=10)
    retryTimes = 1
    while exists and retryTimes * 10 < wait_timeout:
        exists = cc.is_existing(_locator, locator_variables, timeout=10)
        retryTimes += 1
        pass
    logger.debug('结束等待元素消失 - {}，是否存在：{}'.format(str(_locator), ('是' if exists else '否')))
    if exists:
        raise RpaException('等待元素{}消失失败'.format(_locator))

def click(
        _locator,
        locator_variables: dict = {},
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        mouse_location: MouseLocation = MouseLocation(),
        by: Literal["default", "mouse-emulation", "control-invocation"] = MouseActionBy.Default,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        window_mode: Literal["auto", "topmost", "noaction"] = WindowMode.Auto,
        timeout: int = 30,
        sleep_seconds: int = 2
    ) -> None:
    try:
        logger.debug('开始点击元素 - {}'.format(str(_locator)))
        cc.find_element(_locator, locator_variables, window_mode).click(mouse_button=mouse_button, mouse_location=mouse_location, by=by, modifier_key=modifier_key, timeout= timeout)
        logger.debug('结束元素点击 - {}'.format(str(_locator)))
        sleep(sleep_seconds)
        pass
    except:
        raise RpaException('点击{}失败，元素不存在'.format(str(_locator)))
    
def try_click(
        _locator,
        locator_variables: dict = {},
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        mouse_location: MouseLocation = MouseLocation(),
        by: Literal["default", "mouse-emulation", "control-invocation"] = MouseActionBy.Default,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        window_mode: Literal["auto", "topmost", "noaction"] = WindowMode.Auto,
        wait_timeout: int = 15,
        timeout: int = 30,
        sleep_seconds: int = 2
    ) -> bool:
    ele = wait_appear(_locator, locator_variables, wait_timeout=wait_timeout)
    if ele:
        logger.debug('开始点击元素 - {}'.format(str(_locator)))
        cc.find_element(_locator, locator_variables, window_mode).click(mouse_button=mouse_button, mouse_location=mouse_location, by=by, modifier_key=modifier_key, timeout= timeout)
        logger.debug('结束元素点击 - {}'.format(str(_locator)))
        sleep(sleep_seconds)
        return True
    else:
        logger.debug('元素不存在，忽略点击')
        return False
    
def find_elements(
        _locator,
        locator_variables: dict = {},
        timeout: int = 30
    ) -> List[UiElement]:
    logger.debug('开始获取相似元素 - {}'.format(str(_locator)))
    eles = cc.find_elements(_locator, locator_variables, timeout)
    logger.debug('结束获取相似元素 - 匹配{}个结果'.format(len(eles)))
    return eles

def set_text(
        _locator,
        locator_variables: dict = {},
        text: str = '',        
        by: Union[Literal["default", "set-text", "sendkey-after-click", "sendkey-after-focus"], InputTextBy]= InputTextBy.Default,
        overwrite: bool = True,
        timeout: int = 30,
        sleep_seconds: int = 2
    ) -> None:
    logger.debug('开始设置文本 - {}'.format(str(_locator)))
    logger.debug(text)
    try:
        cc.find_element(_locator, locator_variables).set_text(text, by, overwrite, timeout)
        logger.debug('结束设置文本 - {}'.format(str(_locator)))
        sleep(sleep_seconds)
        pass
    except Exception as ex:
        raise RpaException('设置文本{}失败，{}'.format(str(_locator), str(ex)))

def is_existing(
        _locator,
        locator_variables: dict = {},
        timeout: int = 30
    ) -> bool:
    logger.debug('开始检查元素是否存在 - {}'.format(str(_locator)))
    result = cc.is_existing(_locator, locator_variables, timeout)
    logger.debug('结束检查元素是否存在 - {}, 是否存在：{}'.format(str(_locator), ('是' if result else '否')))
    return result

def highlight(
        _locator = Union[_Locator, UiElement],
        locator_variables: dict = {},
        color: Union[str, Color] = Color.Yellow,
        duration: int = 3,        
        timeout: int = 30,
        sleep_seconds: int = 2
    ) -> None: 
    name = str(_locator)
    if isinstance(_locator, UiElement):
        name = 'obj'
    try:
        logger.debug('开始高亮元素 - {}'.format(name))
        if isinstance(_locator, _Locator):
            cc.find_element(_locator, locator_variables).highlight(color, duration, timeout)
            pass
        else:
            _locator.highlight(color, duration, timeout)
        logger.debug('结束高亮元素 - {}'.format(name))
        sleep(sleep_seconds)
        pass
    except Exception as ex:
        logger.warn('高亮元素失败：{}'.format(str(ex)))
        raise RpaException('高亮元素失败 - {}'.format(name))
    
def hover(
        _locator = Union[_Locator, UiElement],
        locator_variables: dict = {},
        timeout: int = 30,
        sleep_seconds: int = 2
    ) -> None: 
    name = str(_locator)
    if isinstance(_locator, UiElement):
        name = 'obj'
    try:
        logger.debug('开始悬停元素 - {}'.format(name))
        if isinstance(_locator, _Locator):
            cc.find_element(_locator, locator_variables).hover(timeout)
            pass
        else:
            _locator.hover(timeout)
        logger.debug('结束悬停元素 - {}'.format(name))
        sleep(sleep_seconds)
        pass
    except Exception as ex:
        logger.warn('悬停元素失败：{}'.format(str(ex)))
        raise RpaException('悬停元素失败 - {}'.format(name))
    
def get_text(
        _locator = Union[_Locator, UiElement],
        locator_variables: dict = {},
        timeout: int = 30
    ) -> str: 
    name = str(_locator)
    if isinstance(_locator, UiElement):
        name = 'obj'
    try:
        txt = None
        logger.debug('开始获取文本 - {}'.format(name))
        if isinstance(_locator, _Locator):
            txt = cc.find_element(_locator, locator_variables).get_text(timeout)
        else:
            txt = _locator.get_text(timeout)
        logger.debug('文本内容：' + txt)
        logger.debug('结束获取文本 - {}'.format(name))
        return txt
    except Exception as ex:
        logger.warn('获取文本失败：{}'.format(str(ex)))
        raise RpaException('获取文本失败 - {}'.format(name))

def set_checkbox(
        _locator = Union[_Locator, UiElement],
        check_type: Literal["check", "uncheck", "toggle"] = CheckType.Check,
        locator_variables: dict = {},
        timeout: int = 30,
        sleep_seconds = 2
    ): 
    name = str(_locator)
     
    try:
        logger.debug('开始设置复选框状态 - {} - {}'.format(str(_locator), check_type))
        cc.find_element(_locator, locator_variables).set_checkbox(check_type, timeout)
        logger.debug('结束设置复选框状态')
        sleep(sleep_seconds)
    except Exception as ex:
        logger.warn('设置复选框状态失败：{}'.format(str(ex)))
        raise RpaException('设置复选框状态失败 - {}'.format(name))
    pass

def send_hotkey(
        hotkey: str,
        sleep_seconds = 2
    ): 
    logger.debug('开始发送快捷键 - {}'.format(str(hotkey)))
    cc.send_hotkey(hotkey)
    logger.debug('结束发送快捷键')
    sleep(sleep_seconds)

def __main__():
    pass