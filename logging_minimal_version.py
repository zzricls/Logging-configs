import logging
import sys
from logging.handlers import RotatingFileHandler
#上面引用了所需函数
#开始配置logging
def setup_logging() -> logging.Logger:
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        #防止多次设置，多次输出
        return logger
    #用户层面设置
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    #文件层面设置
    fileh = RotatingFileHandler(
        "root.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    fileh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-9s | %(funcName)s:%(lineno)d | %(message)s",
                                         datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console)
    logger.addHandler(fileh)
    return logger