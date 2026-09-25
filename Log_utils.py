# log_utils.py
"""
通用日志配置模块。
用法：
    from log_utils import get_logger
    logger = get_logger(__name__)
    logger.info("程序启动")
"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

# ---------- 全局开关（想改默认行为，改这里就行） ----------
DEFAULT_LEVEL = logging.INFO          # 控制台默认级别
DEFAULT_FILE_LEVEL = logging.DEBUG    # 文件默认级别（文件记得更细）
DEFAULT_LOG_DIR = "logs"              # 日志文件夹
DEFAULT_LOG_FILE = "app.log"          # 日志文件名
MAX_BYTES = 10 * 1024 * 1024          # 单个日志文件最大 10MB
BACKUP_COUNT = 5                      # 保留 5 个历史备份

# 格式模板
CONSOLE_FORMAT = "%(asctime)s | %(levelname)-9s | %(name)s | %(message)s"
FILE_FORMAT = "%(asctime)s | %(levelname)-9s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(
    name: str = "app",
    level: Optional[int] = None,
    file_level: Optional[int] = None,
    log_dir: str = DEFAULT_LOG_DIR,
    log_file: str = DEFAULT_LOG_FILE,
    console: bool = True,
) -> logging.Logger:
    """
    获取一个配置好的 Logger。

    :param name:        logger 名字，推荐传 __name__
    :param level:       控制台日志级别， None 默认 INFO
    :param file_level:  文件日志级别， None 默认 DEBUG
    :param log_dir:     日志文件夹
    :param log_file:    日志文件名
    :param console:     是否输出到控制台
    :return:            logging.Logger
    """
    level = level if level is not None else DEFAULT_LEVEL
    file_level = file_level if file_level is not None else DEFAULT_FILE_LEVEL

    logger = logging.getLogger(name)
    logger.setLevel(min(level, file_level))   # 设成两者最低，保证不被提前过滤

    # ---- 关键：防止重复添加 handler（模块被多次 import 时） ----
    if logger.handlers:
        return logger

    # 允许日志向 root 传播（多模块统一收集用），这里关掉避免重复
    logger.propagate = False

    fmt_console = logging.Formatter(CONSOLE_FORMAT, datefmt=DATE_FORMAT)
    fmt_file = logging.Formatter(FILE_FORMAT, datefmt=DATE_FORMAT)

    # ---- Handler 1：控制台 ----
    if console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(fmt_console)
        logger.addHandler(ch)

    # ---- Handler 2：文件（自动切割） ----
    try:
        os.makedirs(log_dir, exist_ok=True)     # 文件夹不存在就建
        log_path = os.path.join(log_dir, log_file)
        fh = RotatingFileHandler(
            log_path,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        fh.setLevel(file_level)
        fh.setFormatter(fmt_file)
        logger.addHandler(fh)
    except Exception as e:
        # 文件写不了（比如没权限），至少保证控制台能用
        logger.warning("文件日志初始化失败，仅输出到控制台: %s", e)

    return logger