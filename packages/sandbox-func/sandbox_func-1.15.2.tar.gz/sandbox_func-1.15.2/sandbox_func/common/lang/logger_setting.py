import os
import logging


def init():
    logging.basicConfig(
        level=logging.DEBUG,
        format=f"%(asctime)s.%(msecs)03d [%(levelname)s] [{os.getenv('BUSINESS_KEY')}] %(name)s:%(filename)s:%(lineno)s - %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S',
    )


def set_logger_formatter(request_id: str):
    """
    日志输出增加request_id
    :param request_id: 请求id
    :return:
    """
    logger = logging.getLogger()
    handlers = logger.handlers
    formatter = logging.Formatter(
        f"%(asctime)s.%(msecs)03d [%(levelname)s] [{os.getenv('BUSINESS_KEY')}] <{request_id}> %(name)s:%(filename)s:%(lineno)s - %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
    for handler in handlers:
        handler.setFormatter(formatter)
