import struct
from datetime import datetime
from enum import Enum
import json

from intrepid_python_sdk.node import CustomEncoder

class Opcode(Enum):
    READ = 1
    WRITE = 2
    INFO = 3
    STATUS = 4
    SPECS = 5
    STOP = 6
    PING = 9
    PONG = 10
    EXEC = 11


class IntrepidMessage:
    def __init__(self, opcode: Opcode, payload, timestamp: datetime, recipient: str, priority=int(0)):
        self.opcode = opcode
        self.payload = payload
        self.timestamp = timestamp
        self.recipient = recipient
        self.priority = priority

    def serialize(self, cdr=True) -> bytes:
        # TODO
        return bytes()

    def __str__(self):
        return f"IntrepidMessage(op={self.opcode}, payload={self.payload}, timestamp={self.timestamp}, recipient={self.recipient}, priority={self.priority})"

class Container(Enum):
    SINGLE = 0,
    OPTION = 1,
    ARRAY = 2,
    ANY = 3

class Count(Enum):
    ONE = 1,
    ZERO_OR_MORE = 2


class InitRequest:
    def __init__(self, node_id: str, node_type: str):
        self._node_id = node_id
        self._node_type = node_type
        self._exec_inputs = None
        self._exec_outputs = None
        self._inputs = None
        self._outputs = None

    @property
    def node_id(self):
        return self._node_id

    @property
    def node_type(self):
        return self._node_type

    @property
    def data_inputs(self):
        return self._inputs

    @property
    def data_outputs(self):
        return self._outputs

    @data_inputs.setter
    def data_inputs(self, value):
        if isinstance(value, list) and all(isinstance(x, dict) for x in value):
            self._inputs = value
        else:
            raise ValueError("data_inputs must be a list of dictionaries")

    @data_outputs.setter
    def data_outputs(self, value):
        if isinstance(value, list) and all(isinstance(x, dict) for x in value):
            self._outputs = value
        else:
            raise ValueError("data_outputs must be a list of dictionaries")


    @property
    def exec_inputs(self):
        return self._exec_inputs

    @exec_inputs.setter
    def exec_inputs(self, value):
        if isinstance(value, list) and all(isinstance(x, dict) for x in value):
            self._exec_inputs = value
        else:
            raise ValueError("exec_inputs must be a list of dictionaries")


    @property
    def exec_outputs(self):
        return self._exec_inputs

    @exec_outputs.setter
    def exec_outputs(self, value):
        if isinstance(value, list) and all(isinstance(x, dict) for x in value):
            self._exec_outputs = value
        else:
            raise ValueError("exec_outputs must be a list of dictionaries")


    def set_node_id(self, node_id: str):
        self.node_id = node_id

    def set_node_type(self, node_type: str):
        self.node_type = node_type

    def set_exec_inputs(self, exec_inputs):
        self.exec_inputs = exec_inputs

    def set_exec_outputs(self, exec_outputs):
        self.exec_outputs = exec_outputs

    def set_inputs(self, inputs):
        self.data_inputs = inputs

    def set_outputs(self, outputs):
        self.data_outputs = outputs




class ExecRequest:
    def __init__(self):
        self._exec_id = None
        self._time = None
        self._inputs = ()

    @property
    def exec_id(self):
        return self._exec_id

    @exec_id.setter
    def exec_id(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._exec_id = value
        else:
            raise ValueError("exec_id must be a number")

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._time = value
        else:
            raise ValueError("time must be a number")

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        if isinstance(value, list):
            self._inputs = value
        else:
            raise ValueError("inputs must be a list")



class ExecResponse:
    def __init__(self):
        self._exec_id = None
        self._time = None
        self._outputs = ()

    @property
    def exec_id(self):
        return self._exec_id

    @exec_id.setter
    def exec_id(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._exec_id = value
        else:
            raise ValueError("exec_id must be a number")

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._time = value
        else:
            raise ValueError("time must be a number")

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        if isinstance(value, tuple):
            self._outputs = value
        else:
            raise ValueError("outputs must be a list")

    def to_json(self):
        res = {
            "exec_id": self.exec_id,
            #"time": self.time,
            "outputs": self.outputs
            }

        return json.dumps(res, cls=CustomEncoder)

    def to_dict(self):
        return {
            "exec_id": self.exec_id,
            #"time": self.time,
            "outputs": self.outputs
        }
