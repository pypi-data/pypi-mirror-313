import re, struct, time, blocks, sensable

class Type:
    def get_value(self, interpreter):
        if isinstance(self, Variable):
            return interpreter.get_var(self.var_name)
        else:
            return self.value

    def set_value(self, value, interpreter):
        if isinstance(self, Variable):
            interpreter.set_var(self.var_name, value)

    def get_coerced(self, interpreter):
        value = self.get_value(interpreter)
        if isinstance(value, float):
            return value
        elif value is None:
            return 0.0
        else:
            return 1.0

class Number(Type):
    def __init__(self, value):
        self.value: float = float(value)

    def __repr__(self):
        return f"{self.value:.4g}"

class String(Type):
    def __init__(self, value):
        self.value: str = value

    def __repr__(self):
        return f'"{self.value}"'

class BlockType(Type):
    def __init__(self, value):
        self.value = value

class Sensable(Type):
    def __init__(self, value):
        self.value = value

class Null(Type):
    def __init__(self, *args):
        self.value = None

    def __repr__(self):
        return "null"

class Variable(Type):
    def __init__(self, var_name):
        self.var_name: str = var_name

    def __repr__(self):
        return self.var_name

def get_type(var):
    if isinstance(var, int) or isinstance(var, float):
        return Number
    elif isinstance(var, str):
        return String
    elif isinstance(var, blocks.Block):
        return BlockType
    elif var is None:
        return Null

def to_type(value: str):
    if re.match(r'^".*"$', value):
        return String(value[1:-1])

    elif re.match(r"^-?(?:[0-9]*\.[0-9]+|[0-9]+)$", value):
        return Number(value)

    elif re.match(r"^0x[0-9a-fA-F]+$", value):
        return Number(int(value[2:], 16))

    elif re.match(r"^0b[01]+$", value):
        return Number(int(value[2:], 2))

    elif re.match(r"^-?[0-9]+e-?[0-9]+$", value):
        return Number(value)

    elif re.match(r"^%[0-9a-fA-F]{6}$", value):
        return Number(pack_color(int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16), 255))

    elif re.match(r"^%[0-9a-fA-F]{8}$", value):
        return Number(pack_color(int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16), int(value[7:9], 16)))

    elif re.match(r"^@.+$", value) and value[1:] in [x for x in dir(sensable.Sense) if x[0] != "_"]:
        return Sensable(getattr(sensable.Sense, value[1:]))

    elif value == "true":
        return Number(1)

    elif value == "false":
        return Number(0)

    elif value == "null":
        return Null()

    else:
        return Variable(value)

def pack_color(r: int, g: int, b: int, a: int) -> float:
    col = (min(255, max(0, r)) << 24) | (min(255, max(0, g)) << 16) | (min(255, max(0, b)) << 8) | min(255, max(0, a))
    col = struct.pack('Q', col)
    return struct.unpack('d', col)[0]

def unpack_color(color: float) -> tuple[int, int, int, int]:
    col = struct.pack('d', color)
    col = struct.unpack('q', col)[0]
    r = (col & 0xff000000) >> 24
    g = (col & 0xff0000) >> 16
    b = (col & 0xff00) >> 8
    a = col & 0xff
    return (r, g, b, a)

def pack_color_float(r: float, g: float, b: float, a: float) -> float:
    return pack_color(r * 255, g * 255, b * 255, a * 255)

def unpack_color_float(color: float) -> tuple[float, float, float, float]:
    return tuple(map(lambda x: x / 255, unpack_color(color)))
