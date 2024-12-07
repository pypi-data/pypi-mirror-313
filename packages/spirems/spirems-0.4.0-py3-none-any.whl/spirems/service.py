#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2024-08-27

import socket
import threading
import time
import random
from spirems.log import get_logger
from spirems.error_code import ec2str
from spirems.msg_helper import (get_all_msg_types, def_msg, encode_msg, check_topic_url, decode_msg, check_msg,
                                index_msg_header, decode_msg_header)


logger = get_logger('Service')


class Service(threading.Thread):

    def __init__(
        self,
        request_url: str,
        request_type: str,
        response_type: str,
        callback_func: callable,
        ip: str = '127.0.0.1',
        port: int = 9094
    ):
        threading.Thread.__init__(self)
        self.request_url = request_url
        self.request_type = request_type
        self.response_type = response_type
        self.ip = ip
        self.port = port
        self.callback_func = callback_func
        self._send_lock = threading.Lock()

        all_types = get_all_msg_types()
        if self.request_type not in all_types.keys():
            raise ValueError('The request type is not available, please check...')
        if self.response_type not in all_types.keys():
            raise ValueError('The response type is not available, please check...')
        url_state = check_topic_url(self.request_url)
        if url_state != 0:
            raise ValueError('The input topic_url is invalid, please verify...')

        self.last_send_time = 0.0
        self.force_quit = False
        self.heartbeat_thread = None
        self.heartbeat_running = False
        self.running = True
        try:
            self._link()
        except Exception as e:
            logger.warning("({}) __init__: {}".format(self.request_url, e))
        self.start()

    def kill(self):
        self.force_quit = True

    def wait_key(self):
        try:
            while not self.force_quit:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info('stopped by keyboard')
            self.kill()
            self.join()

    def heartbeat(self):
        while self.heartbeat_running:
            try:
                if time.time() - self.last_send_time >= 2.0:
                    apply_topic = def_msg('_sys_msgs::Service')
                    apply_topic['request_type'] = self.request_type
                    apply_topic['response_type'] = self.response_type
                    apply_topic['url'] = self.request_url
                    with self._send_lock:
                        self.client_socket.sendall(encode_msg(apply_topic))
                    self.last_send_time = time.time()
            except Exception as e:
                logger.warning("({}) heartbeat: {}".format(self.request_url, e))

            time.sleep(random.randint(1, 3))
            if self.force_quit:
                self.heartbeat_running = False
                break

    def _link(self):
        self.heartbeat_running = False
        if self.heartbeat_thread is not None:
            self.heartbeat_thread.join()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536 * 16)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536 * 16)
        self.client_socket.settimeout(5)
        self.client_socket.connect((self.ip, self.port))
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_running = True
        self.heartbeat_thread.start()

    def _parse_msg(self, msg):
        success, decode_data = decode_msg(msg)
        if success and decode_data['type'] == '_sys_msgs::Request':
            # print("{:.3f}: {}".format(time.time() - decode_data['timestamp'], decode_data))
            resp_msg = self.callback_func(decode_data['msg'])
            if 'timestamp' in resp_msg and resp_msg['timestamp'] == 0.0:
                resp_msg['timestamp'] = time.time()
            if 'type' in resp_msg and resp_msg['type'] == self.response_type:
                response = def_msg('_sys_msgs::Response')
                response['id'] = decode_data['id']
                response['client_key'] = decode_data['client_key']
                response['msg'] = resp_msg
                with self._send_lock:
                    self.client_socket.sendall(encode_msg(response))
                self.last_send_time = time.time()
            else:
                logger.error(ec2str(229))
        elif success and decode_data['type'] == '_sys_msgs::Result':
            if decode_data['error_code'] > 0:
                logger.error(ec2str(decode_data['error_code']))
        elif not success:
            logger.debug(msg)

    def run(self):
        data = b''
        last_data = b''
        big_msg = 0
        while self.running:
            if self.force_quit:
                self.running = False
                break
            try:
                data = self.client_socket.recv(65536 * 8)  # 64K, 65536
                if not data:
                    raise TimeoutError('No data arrived.')
                # print('data: {}'.format(data))
            except TimeoutError as e:
                logger.warning("({}) recv(1): {}".format(self.request_url, e))
                # print(time.time() - tt1)
                self.running = False
                data = b''
            except Exception as e:
                logger.warning("({}) recv(2): {}".format(self.request_url, e))
                self.running = False
                data = b''

            try:
                recv_msgs = []
                checked_msgs, parted_msgs, parted_lens = check_msg(data)

                if len(parted_msgs) > 0:
                    for parted_msg, parted_len in zip(parted_msgs, parted_lens):
                        if parted_len > 0:
                            last_data = parted_msg
                            big_msg = parted_len
                        else:
                            last_data += parted_msg
                            if 0 < big_msg <= len(last_data):
                                recv_msgs.append(last_data[:big_msg])
                                big_msg = 0
                                last_data = b''

                recv_msgs.extend(checked_msgs)
                if len(recv_msgs) > 0:
                    for msg in recv_msgs:
                        self._parse_msg(msg)

            except Exception as e:
                logger.warning("({}) parse: {}".format(self.request_url, e))
                self.running = False

            while not self.running:
                if self.force_quit:
                    break
                # logger.info('(1) running=False, heartbeat_running=False')
                self.heartbeat_running = False
                try:
                    self.client_socket.close()
                    # logger.info('(2) client_socket closed')
                except Exception as e:
                    logger.warning("({}) socket_close: {}".format(self.request_url, e))
                time.sleep(5)
                # logger.info('(3) start re-linking ...')
                try:
                    self._link()
                    self.running = True
                    # logger.info('(4) running=True, suspended=False')
                except Exception as e:
                    logger.warning("({}) relink: {}".format(self.request_url, e))
                logger.info('Running={}, Wait ...'.format(self.running))
                data = b''
                last_data = b''
                big_msg = 0


max_dt = 0


def callback_f(msg):
    print(msg)
    res_msg = def_msg('std_msgs::Number')
    res_msg['data'] = len(msg['data'])
    return res_msg


if __name__ == '__main__':
    ss = Service('/service1', 'std_msgs::String', 'std_msgs::Number', callback_f)
