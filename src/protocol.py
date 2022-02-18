import pickle
from socket import socket
import enum, json, pickle
import xml.etree.ElementTree as ET

class Serializer(enum.Enum):
    """Possible message serializers."""

    JSON = 0
    XML = 1
    PICKLE = 2


class Message:
    """Message Type."""
    def __init__(self,method: str = None):
        self.method = method

class SubscribeMessage(Message):
    """Message to join a chat channel."""
    def __init__(self, topic: str = None):
        super().__init__("SUBSCRIBE")
        self.topic = topic

    def __repr__( self ) -> str:
        return '{{ "method" : {} , "topic" : {} }}'.format(self.method, self.topic)

    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())


class UnsubscribeMessage(Message):
    """Message to unregister from certain topic"""
    def __init__(self,topic: str = "topic_name"):
        super().__init__("UNSUBSCRIBE")
        self.topic = topic
    #end
    def __repr__( self ) -> str:
        return '{{ "method" : {}, "topic" : {} }}'.format(self.method, self.topic )

    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())


class ListRep(Message):
    """List of all topics. help"""
    def __init__(self, listOfTopics : [str] = ["weather2", "weather"]):
        super().__init__("ACK_LIST")
        self.topics = listOfTopics


    def __repr__( self ) -> str:
        return '{{ "method" : {}, "topics" : {} }}'.format(self.method, self.topics)

    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())

class List(Message):
    """Listt all topics"""
    def __init__(self):
        super().__init__("LIST_TOPICS")


    def __repr__( self ) -> str:
        return '{{ "method" : {} }}'.format(self.method)

    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())


class PutTopic(Message):
    """Add a new topic"""
    def __init__(self, topic: str = "topic_name", value : str = "Hello World!" ):
        super().__init__("PUT_TOPIC")
        self.topic = topic
        self.value = value

    def __repr__( self ) -> str:
        return '{{ "method" : {}, "topic" : {}, "value" : {} }}'.format(self.method,self.topic,self.value)
    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())

class GetTopicRep(Message):
    """Message to chat with other clients."""
    def __init__(self,topic: str = "topic_name", value : str = "Hello World!" ):
        super().__init__("ACK_GET")
        self.topic = topic
        self.value = value

    def __repr__( self ) -> str:
        return '{{ "method" : {}, "topic" : {}, "value" : {} }}'.format(self.method,self.topic,self.value)

    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())

class GetTopic(Message):
    """Message to chat with other clients."""
    def __init__(self,topic: str = "topic_name"):
        super().__init__("GET_TOPIC")
        self.topic = topic

    def __repr__( self ) -> str:
        return '{{ "method" : {}, "topic" : {} }}'.format(self.method, self.topic)

    def __str__( self ) -> str:
        return self.__repr__()

    def __len__ ( self ) -> int:
        return len(self.__str__())



class CDProto:
    """Computação Distribuida Protocol."""

    @classmethod
    def subscribe(cls, topic: str) -> SubscribeMessage:
        return SubscribeMessage(topic)

    @classmethod
    def unsubscribe(cls, topic: str) -> UnsubscribeMessage:
        return UnsubscribeMessage(channel)

    @classmethod
    def listRep(cls, listTopics: [str] = ["weather2", "weather"] ) -> ListRep:
        return ListRep(listTopics)

    @classmethod
    def listReq(cls) -> List:
        return List()

    @classmethod
    def putTopic(cls,topic : str = "/weather", value : str = "20") -> PutTopic:
        return PutTopic(topic, value)

    @classmethod
    def getTopic(cls,topic : str = "/weather",) -> GetTopic:
        return GetTopic(topic )

    @classmethod
    def getTopicRep(cls,topic : str = "/weather", value : str = "20") -> GetTopicRep:
        return GetTopicRep(topic, value)

    @classmethod
    def serializeMsg(cls, msg: Message, _format = Serializer.JSON):

        if _format == Serializer.JSON:
            msg_serialized = json.dumps(msg.__dict__)
            return msg_serialized

        elif _format == Serializer.XML:
            if msg.method == "GET_TOPIC":
                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\"></message>".format( msg.method,
                                                                                              msg.topic
                                                                                             )

            elif msg.method == "ACK_GET":
                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\" value=\"{}\"></message>".format( msg.method,
                                                                                                       msg.topic,
                                                                                                       msg.value
                                                                                                      )

            elif msg.method == "PUT_TOPIC":
                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\"></message>".format( msg.method,
                                                                                             msg.topic
                                                                                             )

            elif msg.method == "ACK_PUT":
                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\"></message>".format( msg.method,
                                                                                                      )


            elif msg.method == "LIST_TOPICS":
                msg_serialized = "<?xml version=\"1.0\"?><message  method=\"{}\"></message>".format( msg.method,msg.topics
                                                                                     )


            elif msg.method == "ACK_LIST":
                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\" topics_list=\"{}\" ></message>".format( msg.method,
                                                                                                     msg.topic_list
                                                                                                    )

            elif msg.method == "SUBSCRIBE":

                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\" ></message>".format( msg.method,
                                                                                                      msg.topic,
                                                                                                     )

            elif msg.method == "UNSUBSCRIBE":
                msg_serialized = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\"</topic></message>".format( msg.method,
                                                                                                     msg.topic
                                                                                                    )
            return msg_serialized
        elif _format == Serializer.PICKLE:

            if msg.method == "GET_TOPIC":
                msg_serialized = pickle.dumps({"method":msg.method, "topic" : msg.topic })

            elif msg.method == "ACK_GET":
                msg_serialized = pickle.dumps({"method":msg.method, "topic" : msg.topic, "value": msg.value })

            elif msg.method == "PUT_TOPIC":
                msg_serialized = pickle.dumps({"method":msg.method, "topic" : msg.topic, "value" : msg.value})

            elif msg.method == "ACK_PUT":
                msg_serialized = pickle.dumps({"method":msg.method, "topic" : msg.topic })

            elif msg.method == "LIST_TOPICS":
                msg_serialized = pickle.dumps({"method":msg.method })

            elif msg.method == "ACK_LIST":
                msg_serialized = pickle.dumps({"method":msg.method, "topics" : msg.topics })

            elif msg.method == "SUBSCRIBE":
                msg_serialized =  pickle.dumps({"method":msg.method, "topic" : msg.topic })

            elif msg.method == "UNSUBSCRIBE":
                msg_serialized = pickle.dumps({"method":msg.method, "topic" : msg.topic })
            return msg_serialized
        else:
            return None


    @classmethod
    def send_msg(cls, connection: socket, msg ):
        """Sends through a connection a Message or a string if it's a String then it must be a QUEUE
        informing the broker of what serializer it uses"""

        if isinstance(msg, str):
            msg_bytes = msg.encode("utf8")
        else:
            msg_bytes = msg
        if msg == b'':
            pass

        total_len = len(msg_bytes)
        if total_len <= 65535:
            msg_bytes_and_len = len(msg_bytes).to_bytes(2, byteorder='big') + msg_bytes
            connection.send(msg_bytes_and_len)




    @classmethod
    def recv_msg(cls, connection: socket, _format : Serializer=Serializer.JSON) -> Message:
        """ If no _format Is Specified it's probablye not needed"""
        """Receives through a connection a Message object."""

        a = connection.recv(2)

        msg_length = int.from_bytes( a, byteorder='big')
        msg=b''
        while msg_length != 0:
            data = connection.recv(min(msg_length,2048))
            msg_length = msg_length - len(data)
            msg = msg + data

        try:
            msg_decoded = msg.decode("utf-8").strip(" ")
            if msg_decoded == "JSON":
                return "JSON"
            if msg_decoded == "XML":
                return "XML"
            if msg_decoded == "PICKLE":
                return "PICKLE"
        except UnicodeDecodeError as e:
            pass

        output = None
        if msg == b'':
            return None

        if _format == Serializer.PICKLE:
            output = pickle.loads(msg)
        if _format == Serializer.JSON:
            output = json.loads(msg)
        if _format == Serializer.XML:
            output = {}
            root = ET.fromstring(msg_decoded) # message part of the xml
            for k in root.keys():     # goes through every key and assigns in args each value to a key
                output[k] = root.get(k)

        if output is None:
            return None
        else:
            return output

        return None


class CDProtoBadFormat(Exception):
    """Exception when source message is not CDProto."""

    def __init__(self, original_msg: bytes=None) :
        """Store original message that triggered exception."""
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        """Retrieve original message as a string."""
        return self._original.encode('utf-8').decode("utf-8")
