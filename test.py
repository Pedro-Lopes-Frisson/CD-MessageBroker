import src.utils as s
args = {"method" : "SUBSCRIBE", "topic" : "weather"}
_format = s.Serializer.XML
s.serializeMessage(args,_format)
