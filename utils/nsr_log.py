# -*- coding:utf-8 -*-
__author__ = 'jxy'

import logging
import logging.handlers

LOG_LEVEL = logging.INFO
FORMATTER = '%(asctime)s %(name)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s'

MAIN_LOG_PATH = r'c:/nsr.log'

# class NSRLog(object):
#
#     __formatter = logging.Formatter(FORMATTER)
#
#     __console = logging.StreamHandler()
#     __console.setFormatter(__formatter)
#
#     def __init__(self, logger_name='', log_file_path='default.log', log_level=logging.DEBUG):
#         self.__logger_name = logger_name
#         self.__log_file_path = log_file_path
#         self.__log_file = logging.FileHandler(log_file_path)
#         self.__log_file.setFormatter(self.__formatter)
#
#         self.__logger = logging.getLogger(logger_name)
#         self.__logger.setLevel(log_level)
#         self.__logger.addHandler(self.__log_file)
#         self.__logger.addHandler(self.__console)
#
#     def __del__(self):
#         # self.__logger.removeHandler(self.__log_file)
#         # self.__logger.removeHandler(self.__console)
#         pass
#
#     def get_logger(self):
#         return self.__logger


def nsr_logger(logger_name='', is_console_enabled=False, log_file_path_list=[], log_format=FORMATTER, log_level=logging.DEBUG):
    '''
    日志配置器
    :param logger_name:日志名称
    :param log_file_path_list:日志文件保存路径
    :param log_format:日志格式
    :param log_level:日志等级
    :return:logger对象
    '''

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(log_format)

    if is_console_enabled:
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    for log_file in log_file_path_list:
        # filehandler = logging.FileHandler(log_file)
        # filehandler.setFormatter(formatter)
        # logger.addHandler(filehandler)

        '''
        “S”: Seconds
        “M”: Minutes
        “H”: Hours
        “D”: Days
        “W”: Week day (0=Monday)
        “midnight”: Roll over at midnight
        '''
        filehandler = logging.handlers.TimedRotatingFileHandler(
        log_file, 'D', 1, 0)
        # 设置后缀名称，跟strftime的格式一样
        filehandler.suffix = "%Y%m%d-%H%M%S.log"
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    return logger

log_root = nsr_logger(logger_name='nsr')

# log_hw_s5700 = nsr_logger(logger_name='hw_s5700',
#                           log_file_path_list=[r'/var/www/nsr/resource/vswitches/hw_s5700.log'],
#                           log_format=FORMATTER,
#                           log_level=LOG_LEVEL)

log_hw_s5700 = nsr_logger(logger_name='hw_s5700',
                          is_console_enabled=False,
                          log_file_path_list=[r'/home/restful_test/switch.log'],
                          log_format=FORMATTER,
                          log_level=LOG_LEVEL)

log_nsr_service = nsr_logger(logger_name='service',
                             # log_file_path_list=[r'c:/service.log'],
                             log_file_path_list=[r'/home/restful_test/service.log'],
                             # log_file_path_list=[r'/Users/jixiaoyu/Desktop/github_clone/traffic.log'],
                             log_format=FORMATTER,
                             log_level=LOG_LEVEL)
#
# log_nsr_service_tnodedeployer = nsr_logger(logger_name='nsr.service.tnodedeployer',
#                                            log_file_path_list=[r'c:/nsr.service.tnodedeployer.log'],
#                                            log_format=FORMATTER,
#                                            log_level=LOG_LEVEL)

