# -*- coding:utf-8 -*-
import logging
import logging.handlers
import os
import sys
from typing import Any


class BaseQuantLog:
    """基础日志类，提供公共配置方法"""

    def __init__(self, console_output: bool = True, file_output: bool = False):
        """
        初始化日志配置

        Args:
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
        """
        self.console_output = console_output
        self.file_output = file_output
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.logs_dir = os.path.join(self.root_path, '../logs')

        # 确保日志目录存在
        os.makedirs(self.logs_dir, exist_ok=True)

        # 日志格式
        self.formatter = logging.Formatter(
            fmt="[%(asctime)s]-[%(filename)s]-[%(levelname)s]-[%(message)s]"
        )

        # 初始化所有日志记录器
        self._init_loggers()

    def _init_loggers(self):
        """初始化所有日志记录器"""
        self._init_info_logger()
        self._init_debug_logger()  # 新增debug日志记录器
        self._init_error_logger()
        self._init_profile_logger()
        self._init_holding_logger()
        self._init_adjust_logger()
        self._init_trader_check_logger()

    def _add_handler(self, logger: logging.Logger, handler: logging.Handler):
        """为日志记录器添加处理器（避免重复添加）"""
        if not logger.handlers:
            logger.addHandler(handler)

    def _create_file_handler(self, filename: str, when: str = 'D') -> logging.Handler:
        """创建文件处理器"""
        file_path = os.path.join(self.logs_dir, filename)
        handler = logging.handlers.TimedRotatingFileHandler(
            file_path, when=when, interval=1, encoding='UTF-8'
        )
        handler.setFormatter(self.formatter)
        return handler

    def _create_console_handler(self) -> logging.Handler:
        """创建控制台处理器"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        return handler

    def _init_info_logger(self):
        """初始化信息日志记录器"""
        self.logger = logging.getLogger("info")
        self.logger.setLevel(logging.INFO)

        if self.file_output:
            file_handler = self._create_file_handler('info.log')
            self._add_handler(self.logger, file_handler)

        if self.console_output:
            console_handler = self._create_console_handler()
            self._add_handler(self.logger, console_handler)

    def _init_debug_logger(self):
        """初始化调试日志记录器"""
        self.debug_logger = logging.getLogger('debug')
        self.debug_logger.setLevel(logging.DEBUG)

        if self.file_output:
            debug_file_handler = self._create_file_handler('debug.log')
            self._add_handler(self.debug_logger, debug_file_handler)

        if self.console_output:
            debug_console_handler = self._create_console_handler()
            self._add_handler(self.debug_logger, debug_console_handler)

    def _init_error_logger(self):
        """初始化错误日志记录器"""
        self.error_logger = logging.getLogger('error')
        self.error_logger.setLevel(logging.ERROR)

        error_handler = self._create_file_handler('错误日志.log')
        self._add_handler(self.error_logger, error_handler)

    def _init_profile_logger(self):
        """初始化性能日志记录器"""
        self.profile_logger = logging.getLogger('profile')
        self.profile_logger.setLevel(logging.INFO)

        profile_handler = self._create_file_handler('性能日志.log')
        self._add_handler(self.profile_logger, profile_handler)

    def _init_holding_logger(self):
        """初始化持仓日志记录器"""
        self.holding_logger = logging.getLogger('holding')
        self.holding_logger.setLevel(logging.INFO)

        holding_handler = self._create_file_handler('持仓日志.log')
        self._add_handler(self.holding_logger, holding_handler)

    def _init_adjust_logger(self):
        """初始化买卖日志记录器"""
        self.adjust_logger = logging.getLogger('adjust')
        self.adjust_logger.setLevel(logging.INFO)

        adjust_handler = self._create_file_handler('买卖日志.log')
        self._add_handler(self.adjust_logger, adjust_handler)

    def _init_trader_check_logger(self):
        """初始化交易检测日志记录器"""
        self.trader_check_logger = logging.getLogger('trader_check')
        self.trader_check_logger.setLevel(logging.INFO)

        trader_check_handler = self._create_file_handler('交易检测日志.log')
        self._add_handler(self.trader_check_logger, trader_check_handler)

    def info(self, message: str, *args: Any):
        """
        info级别日志

        Args:
            message: 消息内容
            *args: 格式化参数
        """
        self.logger.info(message, *args)

    def debug(self, message: str, *args: Any):
        """
        debug级别日志

        Args:
            message: 消息内容
            *args: 格式化参数
        """
        self.debug_logger.debug(message, *args)

    def profile(self, message: str):
        """
        性能日志

        Args:
            message: 消息内容
        """
        self.profile_logger.info(message)

    def warning(self, message: str, *args: Any):
        """
        警告日志

        Args:
            message: 消息内容
            *args: 格式化参数
        """
        self.logger.warning(message, *args)

    def error(self, message: str, exc_info: bool = False):
        """
        错误日志

        Args:
            message: 消息内容
            exc_info: 是否包含异常信息
        """
        self.error_logger.error(message, exc_info=exc_info)

    def holding(self, message: str):
        """
        持仓调整日志

        Args:
            message: 消息内容
        """
        self.holding_logger.info(message)

    def adjust(self, message: str):
        """
        买卖日志

        Args:
            message: 消息内容
        """
        self.adjust_logger.info(message)

    def trader_check(self, message: str):
        """
        交易检测日志

        Args:
            message: 消息内容
        """
        self.trader_check_logger.info(message)


class QuantLog(BaseQuantLog):
    """量化日志类（输出到控制台）"""

    def __init__(self):
        super().__init__(console_output=True, file_output=False)

    def debug(self, message: str, *args: Any):
        """
        debug级别日志 - 输出到控制台
        Args:
            message: 消息内容
            *args: 格式化参数
        """
        self.debug_logger.debug(message, *args)

    def profile(self, message: str):
        """性能日志 - 输出到控制台"""
        self.logger.info(message)

    def warning(self, message: str, *args: Any):
        """警告日志 - 输出到控制台"""
        self.logger.warning(message, *args)

    def error(self, message: str, exc_info: bool = False):
        """错误日志 - 输出到控制台"""
        self.logger.error(message, exc_info=exc_info)

    def holding(self, message: str):
        """持仓调整日志 - 输出到控制台"""
        self.logger.info(message)

    def adjust(self, message: str):
        """买卖日志 - 输出到控制台"""
        self.logger.info(message)

    def trader_check(self, message: str):
        """交易检测日志 - 输出到控制台"""
        self.logger.info(message)


class QuantLogV2(BaseQuantLog):
    """量化日志类V2（输出到文件）"""

    def __init__(self):
        super().__init__(console_output=False, file_output=True)


# 创建全局日志实例
default_logger = QuantLog()  # 默认使用控制台输出

# 如果需要文件输出，可以这样使用：
# default_logger = QuantLogV2()


if __name__ == '__main__':
    # 测试日志功能
    logger = QuantLog()
    logger.info('This is an info message')
    logger.debug('This is a debug message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.profile('This is a profile message')
    logger.holding('This is a holding message')
    logger.adjust('This is an adjust message')
    logger.trader_check('This is a trader check message')

    # 测试文件输出
    file_logger = QuantLogV2()
    file_logger.info('File info log test')
    file_logger.debug('File debug log test')
