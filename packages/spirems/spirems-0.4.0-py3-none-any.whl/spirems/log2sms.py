#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os
from datetime import datetime
from spirems.publisher import Publisher
from spirems.msg_helper import QoS, def_msg
from colorama import Fore


class Logger:
    def __init__(
        self,
        name: str = 'default',
        to_screen: bool = True,
        ip: str = '127.0.0.1',
        port: int = 9094
    ):
        assert len(name) > 0
        self.name = name
        self.to_screen = to_screen

        self.pub = Publisher(
            '/log/' + name,
            'std_msgs::String',
            ip=ip,
            port=port,
            qos=QoS.Reliability
        )

    def __del__(self):
        self.pub.kill()

    def quit(self):
        self.pub.kill()

    def _format_msg(self, msg: str, msg_type: str = 'INFO'):
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_msg = "[{}] {} - {}".format(msg_type, formatted_now, msg)
        sms_msg = def_msg('std_msgs::String')
        sms_msg['data'] = formatted_msg
        self.pub.publish(sms_msg)
        return formatted_msg

    def info(self, msg: str):
        f_msg = self._format_msg(msg, 'INFO')
        if self.to_screen:
            print(Fore.GREEN + f_msg + Fore.RESET)

    def warn(self, msg: str):
        f_msg = self._format_msg(msg, 'WARN')
        if self.to_screen:
            print(Fore.YELLOW + f_msg + Fore.RESET)

    def error(self, msg: str):
        f_msg = self._format_msg(msg, 'ERROR')
        if self.to_screen:
            print(Fore.RED + f_msg + Fore.RESET)

    def debug(self, msg: str):
        f_msg = self._format_msg(msg, 'DEBUG')
        if self.to_screen:
            print(Fore.WHITE + f_msg + Fore.RESET)


class CSVLogger:
    def __init__(
        self,
        columns: list,
        name: str = 'default',
        ip: str = '127.0.0.1',
        port: int = 9094
    ):
        assert len(name) > 0
        self.name = name
        for c in columns:
            assert isinstance(c, str)
        self.columns = columns

        self.pub = Publisher(
            '/csv_log/' + name,
            'std_msgs::String',
            ip=ip,
            port=port,
            qos=QoS.Reliability
        )
        sms_msg = def_msg('std_msgs::String')
        sms_msg['data'] = '#-' + ','.join(columns)
        self.pub.publish(sms_msg)

    def __del__(self):
        self.pub.kill()

    def quit(self):
        self.pub.kill()

    def append(self, values: list):
        assert len(values) == len(self.columns), \
            ("The number ({}) of input data must be consistent with the number ({}) of column names."
             .format(len(values), len(self.columns)))
        sms_msg = def_msg('std_msgs::String')
        sms_msg['data'] = ','.join([str(v) for v in values])
        self.pub.publish(sms_msg)


if __name__ == '__main__':
    logger = CSVLogger(['time', 'x', 'y'])
    logger.append([1, 2, 3])
    logger.quit()
