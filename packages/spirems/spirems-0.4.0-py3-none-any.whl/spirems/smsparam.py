#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2024-08-05

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


def is_valid_filepath(filepath):
    try:
        os.path.abspath(filepath)
        return True
    except Exception:
        return False


def list_callback(msg):
    pass


def _list(ip, port):
    pt = Parameter('_global', list_callback, ip=ip, port=port)
    params = pt.get_all_params()
    for key, val in params.items():
        print(key)
        print('  -> {}'.format(val))
    pt.kill()
    pt.join()


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
    req['data'] = 'param list'
    results = client.request_once(req)
    if 'data' in results:
        print_table(results['data'])


def _set(param_key: str, param_val: any, ip, port):
    assert isinstance(param_key, str), "The input param_key must be a string type!"
    assert can_be_jsonified(param_val), "The input param_value must be jsonified!"
    pt = Parameter('_global', list_callback, ip=ip, port=port, request_once=True)
    old_ = pt.get_param(param_key)
    if old_ is not None:
        tp_ = type(old_)
        if isinstance(old_, list) or isinstance(old_, dict):
            pt.set_param(param_key, tp_(json.loads(param_val)))
        elif isinstance(old_, bool):
            if param_val in ['True', 'true', '1']:
                pt.set_param(param_key, True)
            else:
                pt.set_param(param_key, False)
        else:
            pt.set_param(param_key, tp_(param_val))
    else:
        pt.set_param(param_key, param_val)
    pt.kill()
    pt.join()


def _export(file_name: str, ip, port):
    assert is_valid_filepath(file_name), "Please input the correct file path!"
    if not file_name.endswith('.json'):
        file_name += '.json'
    pt = Parameter('_global', list_callback, ip=ip, port=port, request_once=True)
    params = pt.get_all_params()
    with open(file_name, 'w') as f:
        json.dump(params, f, indent=4)
        print('Done!')
    pt.kill()
    pt.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'cmd',
        nargs='+',
        help='Your Command (list, set, export)')
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
    if args.cmd[0] in ['list', 'set', 'export']:
        if 'list' == args.cmd[0]:
            _list_v2(args.ip, args.port)
        if 'set' == args.cmd[0]:
            assert len(args.cmd) > 2, "Usage: smsparam set [param_key] [param_value]"
            _set(args.cmd[1], args.cmd[2], args.ip, args.port)
        if 'export' == args.cmd[0]:
            assert len(args.cmd) > 1, "Usage: smsparam export [output.json]"
            _export(args.cmd[1], args.ip, args.port)
    else:
        print('[ERROR] Supported command: list, set, export')


if __name__ == '__main__':
    main()
