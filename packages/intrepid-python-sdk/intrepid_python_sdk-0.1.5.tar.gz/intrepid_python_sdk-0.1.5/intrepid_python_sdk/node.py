from enum import Enum
import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class PrimitiveDataType:
    def __init__(self, type: str):
        self.type = type

    # def __str__(self):
    #     return {"data": self.type }

    def to_dict(self):
        return { "data": self.type }

class IntrepidType:
    def __init__(self, base_type, is_array=False):
        """
        Initialize a DataType.

        :param base_type: The base type, either a BaseDataType.
        :param container_type: Whether this is a container type like an array.
        """
        if not isinstance(base_type, Type):
            raise ValueError("base_type must be a BaseDataType")
        self.base_type = base_type
        self.container_type = is_array

    def is_array(self):
        """
        Check if this DataType is an array.
        """
        return self.container_type

    def to_dict(self):
        """
        Convert the IntrepidType to a dictionary representation.
        """
        base_dict = self.base_type.to_dict()
        result = {"type": base_dict}

        if not self.is_array():
            return result["type"]
        else:
            return result["type"]

    @classmethod
    def from_dict(cls, data):
        """
        Create a DataType from a dictionary representation.
        """
        if data.get("type") == "array":
            base_type = cls.from_dict(data.get("of"))
            return cls(base_type, container_type=True)
        else:
            base_type_name = data.get("type").upper()
            if base_type_name in Type.__members__:
                return cls(Type[base_type_name])
            raise ValueError(f"Invalid base type: {base_type_name}")

    def __str__(self):
        """
        String representation of the DataType.
        """
        if self.is_array():
            return f"array<{self.base_type}>"
        return self.base_type.name.lower()

    def __eq__(self, other):
        """
        Equality comparison for DataType.
        """
        return isinstance(other, IntrepidType) and self.base_type == other.base_type and self.container_type == other.container_type



class Type(Enum):
    INTEGER = 1
    FLOAT = 2
    STRING = 3
    FLOW = 4
    WILDCARD = 5
    ANY = 6
    ANY_OR_FLOW = 7
    BOOLEAN = 8
    VEC2 = 9
    VEC3 = 10
    BIVEC2 = 11
    BIVEC3 = 12
    ARRAY = 13

    def to_dict(self):
        if self == Type.FLOW:
            return "flow"

        elif self == Type.WILDCARD:
            return "wildcard"

        elif self == Type.ANY:
            return "any"

        elif self == Type.ANY_OR_FLOW:
            return "any_or_flow"

        else:
            return {"data": self.name.lower()}

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_dict(cls, data):
        for enum_member in cls:
            if enum_member.name.lower() == data.get("data"):
                return enum_member
        raise ValueError("Invalid data type")

    @classmethod
    def from_str(cls, data):
        try:
            return cls[data.upper()]
        except KeyError:
            raise ValueError("Invalid data type")

    # @classmethod
    # def from_dict(cls, data):
    #     return cls.from_str(data["data"])

class DataElement:
    """
     type PinSpec = {
        label:        string;
        description?: string;
        type:         { data: string} | 'flow' | 'wildcard' | 'any' | 'any_or_flow';
        container?:   'single' | 'option' | 'array' | 'any';
        count?:       'one' | 'zero_or_more';
        is_const?:    boolean;
    }
    """

    def __init__(self, label: str, type: IntrepidType):
        self.label = label
        self.type = type

    def to_dict(self):
        result = {}
        result["label"] = self.label
        result["type"] = self.type.to_dict()
        if self.type.is_array():
            result["container"] = "array"
        return result

class Node:
    """
    Intrepid Node spec
    -------------------------------

    type NodeSpec = {
        type:         string;
        label:        string;
        description?: string;
        inputs?:      PinSpec[];
        outputs?:     PinSpec[];
    }
    """

    def __init__(self, type: str):
        self.inputs = []
        self.outputs = []
        self.type = type
        self.description = ""
        self.label = ""

    def add_label(self, label: str):
        self.label = label

    def add_description(self, description: str):
        self.description = description

    def add_input(self, label: str, type: Type):
        element = DataElement(label, type)
        self.inputs.append(element)
        # self.inputs.sort(key=lambda x: x.name)

    def add_output(self, label: str, type: Type):
        element = DataElement(label, type)
        self.outputs.append(element)
        # self.outputs.sort(key=lambda x: x.name)

    def get_inputs(self):
        return [(index, element.label, element.type) for index, element in enumerate(self.inputs)]

    def get_outputs(self):
        return [(index, element.label, element.type) for index, element in enumerate(self.outputs)]

    def get_type(self) -> str:
        return self.type

    def to_json(self):
        inputs_json = [input_element.to_dict() for input_element in self.inputs]
        outputs_json = [output_element.to_dict() for output_element in self.outputs]
        res = {
            "inputs": inputs_json,
            "outputs": outputs_json,
            "type": self.type,
            "label": self.label,
            "description": self.description
            }

        return json.dumps(res, cls=CustomEncoder)

    def to_dict(self) -> dict:
        inputs_json = [input_element.to_dict() for input_element in self.inputs]
        outputs_json = [output_element.to_dict() for output_element in self.outputs]
        res = {
            "inputs": inputs_json,
            "outputs": outputs_json,
            "type": self.type,
            "label": self.label,
            "description": self.description
            }
        return res

if __name__ == '__main__':
    n0 = Node()

    n0.add_input("in1", IntrepidType(Type.INTEGER))
    n0.add_input("in2", IntrepidType(Type.FLOAT))
    n0.add_input("in3", IntrepidType(Type.VEC3, is_array=True))
    n0.add_output("out1", IntrepidType(Type.FLOAT))
    n0.get_inputs()

    print(n0)

