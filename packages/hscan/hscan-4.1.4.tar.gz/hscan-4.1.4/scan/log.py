import sys


def get_logger(name=None, log_to_file=False, log_file_path="logfile.log", default_level="DEBUG"):
    from loguru import logger

    # 移除所有现有的处理器
    logger.remove()

    # 添加输出到控制台的处理器，默认级别为 default_level
    logger.add(sys.stdout, colorize=True, level=default_level, format="<green>{time}</green> <level>{message}</level>")
    return logger
