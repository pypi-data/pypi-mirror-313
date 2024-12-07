#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2024-08-27

import logging
import socket
import threading
import time
import random
from queue import Queue
from spirems.error_code import ec2str
from jsonschema import validate
from spirems.log import get_logger
from spirems.msg_helper import (get_all_msg_types, get_all_msg_schemas, def_msg, encode_msg, check_topic_url,
                                decode_msg, check_msg,
                                index_msg_header, decode_msg_header)


logger = get_logger('Client')


class Client(threading.Thread):

    def __init__(
        self,
        request_url: str,
        request_type: str,
        response_type: str,
        ip: str = '127.0.0.1',
        port: int = 9094,
        request_once: bool = False
    ):
        threading.Thread.__init__(self)
        self.request_url = request_url
        self.request_type = request_type
        self.response_type = response_type
        self.ip = ip
        self.port = port
        self._response_queue = Queue()

        all_types = get_all_msg_types()
        if self.request_type not in all_types.keys():
            raise ValueError('The request type is not available, please check...')
        if self.response_type not in all_types.keys():
            raise ValueError('The response type is not available, please check...')
        url_state = check_topic_url(self.request_url)
        if url_state != 0:
            raise ValueError('The input topic_url is invalid, please verify...')

        self.upload_id = 0
        self.last_send_time = 0.0
        self._request_once = request_once
        self._send_lock = threading.Lock()
        self.force_quit = False
        self.heartbeat_thread = None
        self.heartbeat_running = False
        self.running = True
        try:
            self._link()
        except Exception as e:
            logger.warning("({}) __init__: {}".format(self.request_url, e))
        self.suspended = False
        self.err_cnt = 0
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
                apply_topic = def_msg('_sys_msgs::Client')
                apply_topic['request_type'] = self.request_type
                apply_topic['response_type'] = self.response_type
                apply_topic['url'] = self.request_url
                if time.time() - self.last_send_time >= 2.0:
                    with self._send_lock:
                        self.client_socket.sendall(encode_msg(apply_topic))
                    self.last_send_time = time.time()
            except Exception as e:
                logger.warning("({}) heartbeat: {}".format(self.request_url, e))

            if self._request_once:
                time.sleep(0.1)
            else:
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

    def request(self, msg: dict, timeout: int = 5) -> dict:
        if self.suspended:
            return {}
        assert msg['type'] == self.request_type
        if msg['type'] in get_all_msg_schemas():
            validate(instance=msg, schema=get_all_msg_schemas()[msg['type']])
        try:
            msg = msg.copy()
            if 'timestamp' in msg.keys() and msg['timestamp'] == 0.0:
                msg['timestamp'] = time.time()
            msg_request = def_msg('_sys_msgs::Request')
            msg_request['msg'] = msg
            self.upload_id += 1
            if self.upload_id > 1e6:
                self.upload_id = 1
            msg_request['id'] = self.upload_id
            with self._send_lock:
                self.client_socket.sendall(encode_msg(msg_request))
            self.last_send_time = time.time()
            response = self._response_queue.get(block=True, timeout=timeout)
            return response
        except Exception as e:
            if self._request_once:
                self.force_quit = True
            # logger.warning("({}) request {}".format(self.request_url, e))
            return {}

    def request_once(self, msg: dict, timeout: int = 5) -> dict:
        self._request_once = True
        return self.request(msg, timeout)

    def _parse_msg(self, msg) -> bool:
        success, decode_data = decode_msg(msg)
        if success and decode_data['type'] == '_sys_msgs::Response':
            self._response_queue.put(decode_data['msg'])
            if self._request_once:
                self.force_quit = True
                return True
        elif success and decode_data['type'] == '_sys_msgs::Result':
            if decode_data['id'] > 0:
                self.err_cnt = 0
            if decode_data['error_code'] > 0:
                logger.error(ec2str(decode_data['error_code']))
                self.err_cnt += 1
                if self.err_cnt > 5:
                    self.suspended = True
        elif success and decode_data['type'] != '_sys_msgs::HeartBeat':
            logger.debug(decode_data)
        return False

    def run(self):
        data = b''
        last_data = b''
        big_msg = 0
        while self.running:
            if self.force_quit:
                self.running = False
                break
            try:
                data = self.client_socket.recv(65536 * 8)  # 4096
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
                        if self._parse_msg(msg):
                            continue

            except Exception as e:
                logger.warning("({}) parse: {}".format(self.request_url, e))
                self.running = False

            while not self.running:
                if self._request_once:
                    self.force_quit = True
                if self.force_quit:
                    break
                # logger.info("(1) running=False, suspended=True, heartbeat_running=False")
                self.suspended = True
                self.heartbeat_running = False
                try:
                    self.client_socket.close()
                    # logger.info("(2) client_socket closed")
                except Exception as e:
                    logger.warning("({}) socket_close: {}".format(self.request_url, e))
                time.sleep(5)
                # logger.info("(3) start re-linking ...")
                try:
                    self._link()
                    self.running = True
                    self.suspended = False
                    # logger.info("(4) running=True, suspended=False")
                except Exception as e:
                    logger.warning("({}) relink: {}".format(self.request_url, e))
                logger.info('Running={}, Wait ...'.format(self.running))
                data = b''
                last_data = b''
                big_msg = 0


if __name__ == '__main__':
    cc = Client('/service1', 'std_msgs::String', 'std_msgs::Number')
    while 1:
        req = def_msg('std_msgs::String')
        req['data'] = 'hello world!'
        print(cc.request(req))
        time.sleep(1)
