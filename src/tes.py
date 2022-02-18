from src.utils  import serializeMessage


if __name__ == "__main__":
    args = {"method" : "SUBSCRIBE", "topic" : "weather"}
    _format = s.Serializer.XML
    s.serializeMessage(args,_format)
