#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2024-08-30

import os.path
import socket
import time

from spirems.msg_helper import (encode_msg, decode_msg, get_all_msg_types, def_msg, check_msg,
                                index_msg_header, decode_msg_header, can_be_jsonified, print_table)
import sys
import argparse
import json
from spirems.subscriber import Subscriber
from spirems.parameter import Parameter
from spirems.client import Client


def _list_v2(ip, port):
    client = Client(
        '/system/service',
        'std_msgs::String',
        'std_msgs::StringMultiArray',
        ip=ip,
        port=port,
        request_once=True
    )
    req = def_msg('std_msgs::String')
    req['data'] = 'service list'
    results = client.request_once(req)
    if 'data' in results:
        print_table(results['data'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'cmd',
        nargs='+',
        help='Your Command (list)')
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
    # print(args.ip)
    # print(args.port)
    # print(args.cmd)
    if args.cmd[0] in ['list']:
        if 'list' == args.cmd[0]:
            _list_v2(args.ip, args.port)
    else:
        print('[ERROR] Supported command: list')


if __name__ == '__main__':
    main()
