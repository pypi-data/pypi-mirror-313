#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os
import time
from datetime import datetime
from queue import Queue
import argparse
from spirems.publisher import Publisher
from spirems.subscriber import Subscriber
from spirems.msg_helper import QoS, Rate, def_msg
import threading
from enum import Enum


class LogType(Enum):
    STDLog = 1
    CSVLog = 2


class LoggerSaver(threading.Thread):
    def __init__(
        self,
        save_path: str = '',
        log_type: LogType = LogType.STDLog,
        name: str = 'default',
        ip: str = '127.0.0.1',
        port: int = 9094
    ):
        threading.Thread.__init__(self)
        assert len(name) > 0
        self.name = name
        self.log_type = log_type
        self.save_path = save_path

        topic_url = '/log/' + name
        if log_type == LogType.CSVLog:
            topic_url = '/csv_log/' + name

        self.sub = Subscriber(
            topic_url,
            'std_msgs::String',
            ip=ip,
            port=port,
            callback_func=self.log_callback,
            qos=QoS.Reliability
        )
        self.rate = Rate(1)
        self.log_queue = Queue()
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        if log_type == LogType.STDLog:
            self.file = open(os.path.join(self.save_path, 'sms-std-log_' + now_str + '.txt'), 'w')

        self.csv_init = False
        self.running = True
        self.start()

    def log_callback(self, msg):
        # print(msg)
        self.log_queue.put(msg['data'])

    def quit(self):
        self.sub.kill()
        self.running = False

    def run(self):
        while self.running:
            lines = []
            while not self.log_queue.empty():
                msg_data = self.log_queue.get()
                if self.log_type == LogType.CSVLog and '#-' == msg_data[:2]:
                    if self.csv_init:
                        self.file.close()
                    now = datetime.now()
                    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
                    self.file = open(os.path.join(self.save_path, 'sms-csv-log_' + now_str + '.csv'), 'w')
                    self.csv_init = True
                    lines.append(msg_data[2:] + '\n')
                else:
                    lines.append(msg_data + '\n')
            if len(lines):
                if ((self.log_type == LogType.CSVLog and self.csv_init)
                    or self.log_type == LogType.STDLog):
                    self.file.writelines(lines)
                    self.file.flush()
            self.rate.sleep()

        if ((self.log_type == LogType.CSVLog and self.csv_init)
            or self.log_type == LogType.STDLog):
            self.file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--save-path',
        type=str,
        default='',
        help='Log saving path.')
    parser.add_argument(
        '-l', '--log-type',
        type=int,
        default=1,
        help='Log type (e.g. 1: LogType.STDLog, 2: LogType.CSVLog).')
    parser.add_argument(
        '-n', '--name',
        type=str,
        default='default',
        help='Log topic name (e.g. default: /log/default).')
    parser.add_argument(
        '--ip',
        type=str,
        default='127.0.0.1',
        help='SpireMS Core IP')
    parser.add_argument(
        '--port',
        type=int,
        default=9094,
        help='SpireMS Core Port')
    args = parser.parse_args()

    assert args.log_type == 1 or args.log_type == 2
    ls = LoggerSaver(
        save_path=args.save_path,
        log_type=LogType(args.log_type),
        name=args.name,
        ip=args.ip,
        port=args.port
    )
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ls.quit()
            break


if __name__ == '__main__':
    main()
