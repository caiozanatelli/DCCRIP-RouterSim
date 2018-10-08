import json

class Packet:

    def json_encoding(json_dict):
        json_str = json.dumps(json_dict)
        return json_str

    def json_decoding(json_str):
        json_dict = json.loads(json_str)
        return json_dict

    def to_struct(json_str):
        data = bytes(json_str, 'ascii')
        return data

    def to_string(data):
        json_str = data.decode('ascii')
        return json_str
    