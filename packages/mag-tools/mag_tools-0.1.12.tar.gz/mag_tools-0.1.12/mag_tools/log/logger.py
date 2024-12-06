import logging
import logging.config
import os

from mag_tools.model.common.log_type import LogType
from mag_tools.utils.common.string_utils import StringUtils


class Logger:
    __instance = None

    def __init__(self, app):
        app_name = os.path.splitext(os.path.basename(app))[0]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__root_dir = os.path.abspath(os.path.join(current_dir, '..\\..'))

        log_dir = os.path.join(self.__root_dir, "data", app_name, "logs")
        os.makedirs(log_dir, exist_ok=True)

        logging.config.fileConfig(f"{self.__root_dir}\\data\\logging.conf", defaults={'logdir': log_dir})

        self.root_logger = logging.getLogger()

        self.frame_logger = logging.getLogger('frame')
        self.__set_log_file(self.frame_logger, app_name)

        self.service_logger = logging.getLogger('service')
        self.__set_log_file(self.service_logger, app_name)

        self.performance_logger = logging.getLogger('performance')
        self.__set_log_file(self.performance_logger, app_name)

        Logger.__instance = self

    @staticmethod
    def initialize(app):
        if Logger.__instance is None:
            Logger(app)

    @staticmethod
    def debug(*args):
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = args[0]
            Logger.__instance.__debug(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            Logger.__instance.__debug(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @staticmethod
    def info(*args):
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = args[0]
            Logger.__instance.__info(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            Logger.__instance.__info(logger_type, message)
        elif len(args) == 3:
            logger_type, message, is_highlight = args
            if is_highlight:
                Logger.__instance.__info(logger_type, '*'*(StringUtils.get_print_width(message)+8))
                Logger.__instance.__info(logger_type, f'*** {message} ***')
                Logger.__instance.__info(logger_type, '*'*(StringUtils.get_print_width(message)+8))
            else:
                Logger.__instance.__info(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    @staticmethod
    def error(*args):
        if Logger.__instance is None:
            raise ValueError("Logger not initialized. Please call initialize first.")

        if len(args) == 1:
            message = str(args[0]) if isinstance(args[0], Exception) else args[0]
            Logger.__instance.__error(LogType.FRAME, message)
        elif len(args) == 2:
            logger_type, message = args
            message = str(message) if isinstance(message, Exception) else message
            Logger.__instance.__error(logger_type, message)
        else:
            raise ValueError("Invalid number of arguments")

    def __debug(self, logger_type, message):
        self.root_logger.debug(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.debug(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.debug(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.debug(message)

    def __info(self, logger_type, message):
        self.root_logger.info(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.info(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.info(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.info(message)

    def __error(self, logger_type, message):
        self.root_logger.error(message)

        if logger_type == LogType.FRAME:
            self.frame_logger.error(message)
        elif logger_type == LogType.SERVICE:
            self.service_logger.error(message)
        elif logger_type == LogType.PERFORMANCE:
            self.performance_logger.error(message)

    def __set_log_file(self, logger, app_name):
        # handler = logger.handlers[0]
        # log_file = f"{self._data_dir}\\{app_name}\\logs\\{logger.name}.log"
        # handler.baseFilename = log_file
        # handler.stream = open(log_file, 'a')
        pass