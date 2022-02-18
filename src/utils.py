import enum, json, pickle
import xml.etree.ElementTree as ET



class Serializer(enum.Enum):
    """Possible message serializers."""

    JSON = 0
    XML = 1
    PICKLE = 2


def serializeMessage(args, _format : Serializer = Serializer.JSON):
    """
    Receives a list of Parameteres such as method, topic, value....
    Returns a serialized message according to _format with the header included
    """

    if _format == Serializer.JSON:
        msg = json.dumps(args)
    elif _format == Serializer.XML:
        print("XML")
        if args["method"] == "GET_TOPIC":
            msg = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\"></message>".format( args["method"],
                                                                                          args["topic"]
                                                                                         )

        elif args["method"] == "ACK_GET":
            msg = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\" value=\"{}\"></message>".format( args["method"],
                                                                                                   args["topic"],
                                                                                                   args["value"]
                                                                                                  )

        elif args["method"] == "PUT_TOPIC":
            msg = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\"></message>".format( args["method"],
                                                                                         args["topic"]
                                                                                         )

        elif args["method"] == "ACK_PUT":
            msg = "<?xml version=\"1.0\"?><message method=\"{}\"></message>".format( args["method"],
                                                                                                  )


        elif args["method"] == "LIST_TOPICS":
            msg = "<?xml version=\"1.0\"?><message  method=\"{}\"></message>".format( args["method"],
                                                                                 )


        elif args["method"] == "ACK_LIST":
            msg = "<?xml version=\"1.0\"?><message method=\"{}\" topics_list=\"{}\" ></message>".format( args["method"],
                                                                                                 args["topic_list"]
                                                                                                )

        elif args["method"] == "SUBSCRIBE":

            msg = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\" ></message>".format( args["method"],
                                                                                                  args["topic"],
                                                                                                 )

        elif args["method"] == "UNSUBSCRIBE":
            msg = "<?xml version=\"1.0\"?><message method=\"{}\" topic=\"{}\"</topic></message>".format( args["method"],
                                                                                                 args["topic"]
                                                                                                )
        else:
            print(args["method"])
            print("Pretty sure that thats illegal")

        print (msg)


    elif _format == Serializer.PICKLE:
        msg = pickle.dumps(args)
    else:
        print("Illegal Serializer")
        return None

    msg_bytes = bytearray(str(msg),'utf-8')
    total_len = len(msg_bytes)
    msg_bytes_and_len = len(msg_bytes).to_bytes(2, byteorder='big') + msg_bytes
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa ", total_len)
    return msg_bytes_and_len, total_len


def readSerializedMessage(msg: bytes=None, _format: Serializer = Serializer.JSON ):
    """ msg is just the message there's no header here only the xml one i guess it should be coded as bytes
        returns a dict that contains message specific values specified in PROTOCOLO.md
    """
    print(msg)

    msg = msg.decode("utf-8") # decode bytes
    args = { }

    if _format == Serializer.JSON:
        args = json.loads(msg) # loads as json works cause there wont be any serialization problems that this can t load
                               # if something like : {args : {}} changes will be necessary
    elif _format == Serializer.XML:
        """
            XML Is weird only way i got it to work as intend was to give properties
            to the root node which is message in all cases

        """
        root = ET.fromstring(msg) # message part of the xml
        for k in root.keys():     # goes through every key and assigns in args each value to a key
            args[k] = root.get(k)

    elif _format == Serializer.PICKLE:
        args = pickle.loads(msg) # works well cause pickle

    else:
        print("Illegal Serializer") # invalid serializer
        return None

    return args

def encodeSerializedMessage(msg: bytes=None, _format: Serializer = Serializer.JSON ):
    
    print(msg)

    msg = msg.encode("utf-8") # decode bytes
    args = { }

    if _format == Serializer.JSON:
        args = json.dumps(msg).encode('utf-8') 

    elif _format == Serializer.XML:
        """
            XML Is weird only way i got it to work as intend was to give properties
            to the root node which is message in all cases

        """
        root = ET.fromstring(msg) # message part of the xml
        for k in root.keys():     # goes through every key and assigns in args each value to a key
            args[k] = root.get(k)

    elif _format == Serializer.PICKLE:
        args = pickle.loads(msg) # works well cause pickle

    else:
        print("Illegal Serializer") # invalid serializer
        return None

    return args
