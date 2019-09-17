import json


class Message(object):
    """A representation of a message object"""

    def __init__(self, msg_attrs=None, json_str=None):
        if json_str == None:
            if msg_attrs is not None and len(msg_attrs) == 4:
                self.msg_type = msg_attrs[0]
                self.pub_key = msg_attrs[1]
                self.signature = msg_attrs[2]
                self.content = msg_attrs[3]
            else:
                raise ValueError("Invalid init params")
        else:
            jdict = json.loads(json_str)
            try:
                self.msg_type = jdict["msg_type"]
                self.pub_key = jdict["pub_key"]
                self.signature = jdict["signature"]
                self.content = jdict["content"]
            except ValueError:
                raise ValueError("Invalid init params")

    def to_json(self):
        return json.dumps(vars(self))
