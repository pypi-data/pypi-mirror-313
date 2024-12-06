import logging
import sys


def setup_logger(log_level="info"):
    # 日志格式
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    # 创建 logger
    logger1 = logging.getLogger()

    # 日志级别字典
    log_level_dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
    }

    # 设置日志级别
    logger1.setLevel(log_level_dict.get(log_level, logging.ERROR))

    # 创建控制台处理器
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setFormatter(formatter)
    logger1.addHandler(ch)

    return logger1  # 返回 logger 实例


# 设置 logger 并接收返回值
logger = setup_logger("info")  # 可以根据需要更改日志级别

# fastapi_log_config = fastapi_log_config()
