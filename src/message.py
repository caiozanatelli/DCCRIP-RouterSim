import json

class Message:
    __src  = None
    __dest = None
    __type = None

    def __init__(self, src, dest, msg_type):
        self.__src  = src
        self.__dest = dest
        self.__type = msg_type

    def to_dict(self):
        d = dict()
        d["type"] = self.__type
        d["source"] = self.__src
        d["desination"] = self.__dest
        return d

    def get_destination(self):
        return self.__dest

    def get_source(self):
        return self.__src

    def get_type(self):
        return self.__type

class Data(Message):
    __payload   = None

    def __init__(self, src, dest, msg_type, payload):
        Message.__init__(self, src, dest, msg_type)
        self.__payload      = payload

    def to_dict(self):
        d = super().to_dict(self)
        d["payload"] = self.__payload
        return d

class Update(Message):
    __distances = None

    def __init__(self, src, dest, msg_type, distances):
        Message.__init__(self, src, dest, msg_type)
        self.__distances = distances

    def to_dict(self):
        d = super().to_dict(self)
        d["distances"] = self.__distances
        return d

    def get_distances(self):
        return self.__distances

class Trace(Message):
    __hops  = None

    def __init__(self, src, dest, msg_type, hops):
        Message.__init__(self, src, dest, msg_type)
        self.__hops = hops

    def to_dict(self):
        d = super().to_dict(self)
        d["hops"] = self.__hops
        return d

    def get_hops(self):
        return self.__hops