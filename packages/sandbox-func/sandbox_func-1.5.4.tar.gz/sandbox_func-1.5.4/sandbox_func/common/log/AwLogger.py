import logging
import os
from collections import UserDict
from enum import Enum

from sandbox_func.common.util.pathutil import get_log_file_path
from sandbox_func.common.config.LoginConfig import DefaultLoginConfig
from sandbox_func.service.cybotron.log_accessor import LogAccessor


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Log(UserDict):
    trace_id: str
    app_id: str
    app_version_id: str
    func_id: str
    creator: str
    level: str
    message: str


class LogRecord(UserDict):
    trace_id: str


class AwLogger:
    """autowork log warapper"""

    cybotron_access_info: dict = {}

    @classmethod
    def getLogger(cls, filename: str, level: LogLevel = LogLevel.INFO):
        logger = logging.getLogger(filename)
        if level is None:
            logger.setLevel('INFO')
        else:
            logger.setLevel(level.value)

        logfile = get_log_file_path()
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d [%(levelname)s] %(filename)s:%(lineno)s - %(""message)s",
            datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 如果是debug模式，信息入库metabase.mb_sandbox_debug_log
        if DefaultLoginConfig.get_debug():
            db_handler = DBLogHandler()
            db_handler.setFormatter(formatter)
            logger.addHandler(db_handler)

        return logger

    # @staticmethod
    # def init_logger(trace_id: str, info: dict):
    #     AwLogger.cybotron_access_info[trace_id] = Log(trace_id=trace_id, **info)
    #     return LogRecord(trace_id=trace_id)


class DBLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record: logging.LogRecord):
        msg = record.getMessage()
        trace_id = record.args.get("trace_id")
        cybotron_access_info = AwLogger.cybotron_access_info[trace_id]
        log = Log(
            trace_id=cybotron_access_info['trace_id'],
            app_id=cybotron_access_info['app_id'],
            func_id=cybotron_access_info['func_id'],
            level=record.levelno,
            message=msg
        )

        try:
            LogAccessor.send_log(log.data)
        except Exception as e:
            print(e)
