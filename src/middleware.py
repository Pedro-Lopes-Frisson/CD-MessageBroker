"""Middleware to communicate with PubSub Message Broker."""
from collections.abc import Callable
from enum import Enum
from queue import LifoQueue, Empty
import socket
import pickle
import selectors
import sys
from   random import randint

from .protocol import CDProto, CDProtoBadFormat, Serializer
from typing import Dict, List, Any, Tuple
from src.log import get_logger


class MiddlewareType(Enum):
    """Middleware Type."""

    CONSUMER = 1
    PRODUCER = 2


class Queue:
    """Representation of Queue interface for both Consumers and Producers."""
    HOST=''
    PORT=3001

    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        """Create Queue."""
        self.log = get_logger(topic + str(_type))
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Sets  special socket options making the socket to not enter the WAIT state
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.connect((self.HOST,self.PORT ))  #connect
        self.topic = topic
        self.type = _type
        self.values = []


    def push(self, value):
        """ Sends data to broker. """
        if self.type == MiddlewareType.CONSUMER:
            return
        msg = CDProto.putTopic(self.topic, value)
        msg_s = CDProto.serializeMsg(msg, self._format)
        try:
            CDProto.send_msg(self.sock, msg_s)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)



    def pull(self) -> (str, Any):
        """Waits for (topic, data) from broker. """
        try:
            args = CDProto.recv_msg(self.sock,self._format)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)

        self.log.info("Message ARGS %s", str(args))
        if args:
            return (args["topic"], args["value"])




    def list_topics(self, callback: Callable):
        """Lists all topics available in the broker."""
        msg = CDProto.listReq()
        msg_s = CDProto.serializeMsg(msg, self._format)

        try:
            CDProto.send_msg(self.sock, msg_s)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)

        args = None
        try:
            args = CDProto.recv_msg(self.sock,self._format)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)

        if args:
            print("Message List %s", str(args))
            list_topic = list(args["topics"])
            idx = randint(0, len(list_topic)-1)
            callback(list_topic[idx])
            print(list_topic)
            self.log.info("Message List %s", str(args))



    def subscribe(self, topic):
        print(topic)
        msg = CDProto.subscribe(topic)
        msg_s = CDProto.serializeMsg(msg, self._format)
        print(msg_s)
        self.log.error(msg_s)
        try:
            CDProto.send_msg(self.sock, msg_s)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)


    def cancel(self):
        """Cancel subscription."""
        msg = CDProto.unsubscribe(self.topic)
        msg_s = CDProto.serializeMsg(msg, self._format)

        try:
            CDProto.send_msg(self.sock, msg_s)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)

    def __str__(self):
        return self.sock.__str__()




class JSONQueue(Queue):
    """Queue implementation with JSON based serialization."""
    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        super().__init__(topic,_type)
        self._format = Serializer.JSON
        msg = "JSON"

        try:
            CDProto.send_msg(self.sock, msg)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)


        if _type == MiddlewareType.CONSUMER:
            msg = CDProto.subscribe(topic)
            msg_s = CDProto.serializeMsg(msg, self._format)
            self.log.error(msg_s)
            try:
                CDProto.send_msg(self.sock, msg_s)
            except ConnectionResetError as e:
                sys.exit(-1)
            except BrokenPipeError as e:
                sys.exit(-1)

class XMLQueue(Queue):
    """Queue implementation with XML based serialization."""
    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        super().__init__(topic,_type)
        self._format = Serializer.XML
        msg = "XML"

        try:
            CDProto.send_msg(self.sock, msg)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)


        if _type == MiddlewareType.CONSUMER:
            msg = CDProto.subscribe(topic)
            msg_s = CDProto.serializeMsg(msg, self._format)
            self.log.error(msg_s)
            try:
                CDProto.send_msg(self.sock, msg_s)
            except ConnectionResetError as e:
                sys.exit(-1)
            except BrokenPipeError as e:
                sys.exit(-1)

class PickleQueue(Queue):
    """Queue implementation with Pickle based serialization."""
    def __init__(self, topic, _type=MiddlewareType.CONSUMER):
        super().__init__(topic,_type)
        self._format = Serializer.PICKLE
        msg="PICKLE"

        try:
            CDProto.send_msg(self.sock, msg)
        except ConnectionResetError as e:
            sys.exit(-1)
        except BrokenPipeError as e:
            sys.exit(-1)


        if _type == MiddlewareType.CONSUMER:
            msg = CDProto.subscribe(topic)
            msg_s = CDProto.serializeMsg(msg, self._format)
            self.log.error(msg_s)
            try:
                CDProto.send_msg(self.sock, msg_s)
            except ConnectionResetError as e:
                sys.exit(-1)
            except BrokenPipeError as e:
                sys.exit(-1)
