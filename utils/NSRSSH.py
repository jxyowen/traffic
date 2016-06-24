#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, traceback
import pexpect

import logging
import logging.handlers

LOG_LEVEL = logging.INFO
FORMATTER = '%(asctime)s %(message)s'

MAIN_LOG_PATH = r'c:/nsr.log'

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
        “D”: Dayszc11
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

log_root = nsr_logger(logger_name='')

log_hw_s5700 = nsr_logger(logger_name='hw_s5700',
                          is_console_enabled=True,
                          # log_file_path_list=[r'/var/www/nsr/resource/vswitches/hw_s5700.log'],
                          log_file_path_list=[],
                          log_format=FORMATTER,
                          log_level=LOG_LEVEL)


class NSRSSH(object):

    def __init__(self, timeout=30, try_login_max_times=3):
        self._cmd_exec_result = -2
        self.__timeout = timeout
        self.__try_login_max_times = try_login_max_times
        self._child = None

    def get_cmd_exec_result(self):
        return self._cmd_exec_result

    def connect(self, login_info, logged_in_symbol=''):
        '''
        建立ssh连接
        :param login_info:登录信息，包括目标主机ip,用户名，密码
        :return:ssh连接实例

        '''

        ssh_newkey = 'Are you sure you want to continue connecting'

        is_logged_in = False
        try_login_times = 0
        is_try_login = True
        while not is_logged_in:
            #1.ssh命令登录
            if is_try_login:
                try_login_times += 1
                os.system('sudo ssh-keygen -f "/root/.ssh/known_hosts" -R ' + login_info['methip'])
                self._child = pexpect.spawn('ssh -l ' + login_info['user'] + ' ' + login_info['methip'],
                                      timeout=self.__timeout)
                is_try_login = False

            i = self._child.expect([pexpect.TIMEOUT, pexpect.EOF, ssh_newkey, 'assword: ', logged_in_symbol])

            if 0 == i or 1 == i:
                self._print_error()

                if try_login_times < self.__try_login_max_times:
                    is_try_login = True
                else:
                    if 0 == i:
                        self._cmd_exec_result = -1
                    elif 1 == i:
                        self._cmd_exec_result = -2
                    return self
            elif 2 == i:  # SSH does not have the public key. Just accept it.
                self._child.sendline('yes')
            elif 3 == i:
                self._child.sendline(login_info['password'])
            elif 4 == i:
                self._print_debug_info()
                self._cmd_exec_result = 0
                return self


    def disconnect(self):
        if self._cmd_exec_result != 0:
            log_hw_s5700.info('SSH Error!')
        else:
            self._child.sendline('quit')
        return self

    def _exec_command_sequence(self, input_expect_pairs_list):
        '''
        执行命令序列
        :param self._child: ssh实例
        :param input_expect_pairs_list: 待执行的命令序列
        :param timeout: 超时时间设置
        :param break_flag:
        :return:
        '''
        if self._cmd_exec_result != 0:
            log_hw_s5700.info('SSH Error!')
        else:
            #1.取出每一个命令序列
            for each_pair in input_expect_pairs_list:
                self._child.sendline(each_pair[0])
                #2.执行命令，并等待系统反馈执行结果
                i = self._child.expect([pexpect.TIMEOUT, pexpect.EOF, each_pair[1]], timeout=self.__timeout)
                self._print_debug_info(each_pair)
                if 0 == i:
                    self._print_error()
                    self._cmd_exec_result = -1
                    break
                elif 1 == i:
                    self._print_error()
                    self._cmd_exec_result = -2
                    break
                elif 2 == i:
                    log_hw_s5700.info('command < %s > exec successful' % each_pair[0])
            log_hw_s5700.info('exec command sequence cmd exec result = %d' % self._cmd_exec_result)

        return self

    def _print_error(self):
        log_hw_s5700.info('########ERROR START########')
        log_hw_s5700.info('Here is what SSH said:')
        log_hw_s5700.info(self._child.before)
        log_hw_s5700.info(self._child.after)
        log_hw_s5700.info('########ERROR END########')

    def _print_debug_info(self, each_pair='nil'):
        log_hw_s5700.info('########DEBUG INFO START########')
        log_hw_s5700.info('EACH PAIR:')
        log_hw_s5700.info(each_pair)
        log_hw_s5700.info('EXPECT BUFFER:')
        log_hw_s5700.info(self._child.before)
        log_hw_s5700.info(self._child.after)
        log_hw_s5700.info('########DEBUG INFO END########')

if __name__ == '__main__':
    print(132)
    d = NSRSSH()
    try:
        log_hw_s5700.info(132123123123)
        d.connect(login_info=dict(user='abc',methip='192.168.1.1',password='1233321'),logged_in_symbol='aa')
    except Exception, e:

        log_hw_s5700.info(traceback.format_exc())
        log_hw_s5700.info(e)
        log_hw_s5700.info('error errorerrorerrorerrorerrorerror')


