import json
import random
import threading
import time
from typing import Callable, Dict, FrozenSet, NewType
from unittest.mock import DEFAULT

from foxglove_websocket.types import ChannelWithoutId
from spirems import Client, def_msg, Subscriber, get_all_foxglove_schemas
from queue import Queue
from spirems.log import get_logger


logger = get_logger('SpireMSMiddlewareThread')


DEFAULT_SMS_IP = '127.0.0.1'
DEFAULT_SMS_PORT = 9094
MiddlewareChannelId = NewType("MiddlewareChannelId", int)
MessageDict = dict()
MessageDictLock = threading.Lock()


def callback_f(msg, chan):
    with MessageDictLock:
        if chan not in MessageDict:
            MessageDict[chan] = Queue()
        MessageDict[chan].put(msg)


class SpireMSMiddlewareThread(threading.Thread):
    """
    This class simulates a pub/sub middleware that provides callbacks in a separate thread. The
    implementation details are not meant to be realistic, but just to simulate an environment where
    channels are appearing and disappearing and messages are arriving at random times.

    Calling code can provide callbacks which will be called from the middleware thread. To do so,
    set the `on_add_channel`, `on_remove_channel`, and `on_message` properties.

    This is a subclass of threading.Thread, so to launch the thread, use the `start()` method.
    """

    # The middleware will call these callbacks from the middleware thread.
    on_add_channel: Callable[[MiddlewareChannelId, ChannelWithoutId], None]
    on_remove_channel: Callable[[MiddlewareChannelId], None]
    on_message: Callable[[MiddlewareChannelId, int, bytes], None]

    # When the server subscribes to a channel, we'll get called in the server thread (the main
    # thread). This lock is used to manage the set of subscribed channels safely across multiple
    # threads.
    #
    # We use a frozenset to indicate that we won't mutate the data structure, we'll just replace it
    # when subscriptions change. This allows the thread's main loop to briefly acquire the lock,
    # grab a reference to the set of channels, and release the lock, knowing that the referenced set
    # is safe to use from the thread, even if another thread happens to replace it.
    _lock: threading.Lock
    _subscribed_channels: FrozenSet[MiddlewareChannelId]

    def __init__(self, ip=DEFAULT_SMS_IP, port=DEFAULT_SMS_PORT):
        super().__init__()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._stopped = False
        self._subscribed_channels = frozenset()
        self.sms_ip = ip
        self.sms_port = port
        self._sms = Client(
            '/system/service',
            'std_msgs::String',
            'std_msgs::StringMultiArray',
            ip=self.sms_ip,
            port=self.sms_port
        )
        self._last_time = 0.0
        self._sms_list = dict()
        self._ids_to_topic = dict()
        self._sms_subscribes = dict()

    def handle_subscribe_threadsafe(self, chan: MiddlewareChannelId):
        """
        Handle an added subscription from a WebSocket client. This method is thread-safe because it
        uses a lock to access internal data structures. It will be called on the WebSocket server
        thread.
        """
        with self._lock:
            self._subscribed_channels = self._subscribed_channels | {chan}

    def handle_unsubscribe_threadsafe(self, chan: MiddlewareChannelId):
        """
        Handle a removed subscription from a WebSocket client. This method is thread-safe because it
        uses a lock to access internal data structures. It will be called on the WebSocket server
        thread.
        """
        with self._lock:
            self._subscribed_channels = self._subscribed_channels - {chan}

    def stop_threadsafe(self):
        """
        Inform the thread that it should finish any active work and stop running. This method is
        thread-safe because the threading.Event class is thread-safe.
        """
        self._stop_event.set()
        for subs in self._sms_subscribes.values():
            subs.kill()
        self._sms.kill()

    def run(self):
        """
        This function provides the main entry point which will be executed in a new thread. It
        periodically calls the on_add_channel, on_remove_channel, and on_message callbacks in the
        middleware thread, simulating an active pub/sub graph.
        """
        logger.info("Middleware thread started")

        # The lowest channel ID we'll use -- this illustrates mapping between native channels and
        # FoxgloveServer channels.
        start_id = MiddlewareChannelId(100)

        # Last value published on each channel
        active_channels: Dict[MiddlewareChannelId, int] = {}

        json_schemas = get_all_foxglove_schemas()

        def next_channel_id() -> MiddlewareChannelId:
            """
            Choose an available channel ID for creating a new channel.
            """
            i = start_id
            while MiddlewareChannelId(i) in active_channels:
                i += 1
            return MiddlewareChannelId(i)

        # Simulate some random events happening until we're asked to stop.
        while not self._stop_event.wait(0.05):
            # Take a reference to the current set of subscribed channels. Because this internal
            # state may be accessed from multiple threads, we need to hold the lock while we access
            # it. Once we release the lock, we know it's safe to continue using the reference during
            # the rest of the loop because the set is never mutated by another thread -- it's only
            # ever replaced with a completely new set.
            with self._lock:
                subscribed_channels = self._subscribed_channels

            if time.time() - self._last_time > 1.0:
                req = def_msg('std_msgs::String')
                req['data'] = 'topic list'
                response = self._sms.request(req)
                sms_list = dict()
                if 'data' in response and len(response['data']) > 1:
                    for i in range(1, len(response['data'])):
                        sms_list[response['data'][i][0]] = response['data'][i][1]

                    to_del = []
                    for i, topic in enumerate(self._sms_list.keys()):
                        if topic not in sms_list:
                            # Remove a random channel
                            channel_id = self._sms_list[topic]["channelId"]
                            self.on_remove_channel(channel_id)
                            del active_channels[channel_id]
                            with self._lock:
                                # Remove the channel from subscribed_channels so we don't try to publish a message to it.
                                self._subscribed_channels = self._subscribed_channels - {channel_id}
                            to_del.append(topic)

                    for topic in to_del:
                        del self._sms_list[topic]

                    for i, topic in enumerate(sms_list.keys()):
                        if topic not in self._sms_list:
                            # Add a new channel
                            id = next_channel_id()
                            schema_name = 'foxglove.' + sms_list[topic].split('::')[-1]
                            if schema_name in json_schemas:
                                schema = json_schemas[schema_name]
                            else:
                                schema = {
                                    "type": "object",
                                    "properties": {},
                                }
                            self.on_add_channel(
                                id,
                                {
                                    "topic": topic,
                                    "encoding": "json",
                                    "schemaName": schema_name,
                                    "schema": json.dumps(schema),
                                    "schemaEncoding": "jsonschema",
                                },
                            )
                            active_channels[id] = 0
                            self._sms_list[topic] = {
                                "channelId": id,
                                "schemaName": sms_list[topic]
                            }
                            self._ids_to_topic[id] = topic
                self._last_time = time.time()

            for chan in list(subscribed_channels):
                topic = self._ids_to_topic[chan]
                if chan not in self._sms_subscribes:
                    subs = Subscriber(
                        topic,
                        self._sms_list[topic]['schemaName'],
                        lambda arg1, arg2=chan: callback_f(arg1, arg2),
                        ip=self.sms_ip,
                        port=self.sms_port
                    )
                    self._sms_subscribes[chan] = subs
                with MessageDictLock:
                    if chan in MessageDict and not MessageDict[chan].empty():
                        while not MessageDict[chan].empty():
                            msg = MessageDict[chan].get()
                        t1 = msg['timestamp']
                        msg['timestamp'] = {}
                        msg['timestamp']['sec'] = int(t1)
                        msg['timestamp']['nsec'] = int((t1 - int(t1)) * 1e9)
                        now = time.time_ns()
                        active_channels[chan] += 1
                        self.on_message(
                            chan,
                            now,
                            json.dumps(msg).encode(
                                "utf8"
                            ),
                        )

            to_del = []
            for chan in self._sms_subscribes.keys():
                if chan not in list(subscribed_channels):
                    self._sms_subscribes[chan].kill()
                    to_del.append(chan)

            for chan in to_del:
                del self._sms_subscribes[chan]
                with MessageDictLock:
                    if chan in MessageDict:
                        del MessageDict[chan]

        # Clean up channels when shutting down
        for id in active_channels:
            self.on_remove_channel(id)
        logger.info("Middleware thread finished")
