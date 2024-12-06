import variables, math, random, re, time, blocks, draw_call

class Instruction:
        def __init__(self):
            pass
        
        def new(args: list[str], **kwargs):
            pass

        def execute(self, interpreter):
            pass

        def __repr__(self):
            return " ".join([REVERSE_LOOKUP[self.__class__]] + [str(v) for k, v in vars(self).items() if k[0] != '_'])

class I_Noop(Instruction):
    def __init__(self):
        pass

    def new(args: list[str], **kwargs):
        return I_Noop()

    def execute(self, interpreter):
        pass

#Input & Output
class I_Read(Instruction):
    def __init__(self, output, cell, index):
        self.output: variables.Type = default_type(output, "result")
        self.cell: variables.Type = default_type(cell, "cell1")
        self.index: variables.Type = default_type(index, "0")

    def new(args: list[str], **kwargs):
        return I_Read(get_index_type(args, 0), get_index_type(args, 1), get_index_type(args, 2))

    def execute(self, interpreter):
        cell = self.cell.get_value(interpreter)
        index = self.index.get_coerced(interpreter)
        if isinstance(cell, blocks.MemoryCell) and int(index) in range(0, cell.memory_size):
            self.output.set_value(cell.memory[int(index)], interpreter)
        else:
            self.output.set_value(None, interpreter)

class I_Write(Instruction):
    def __init__(self, arg, cell, index):
        self.input: variables.Type = default_type(arg, "result")
        self.cell: variables.Type = default_type(cell, "cell1")
        self.index: variables.Type = default_type(index, "0")

    def new(args: list[str], **kwargs):
        return I_Write(get_index_type(args, 0), get_index_type(args, 1), get_index_type(args, 2))

    def execute(self, interpreter):
        value = self.input.get_coerced(interpreter)
        cell = self.cell.get_value(interpreter)
        index = self.index.get_coerced(interpreter)
        if isinstance(cell, blocks.MemoryCell) and int(index) in range(0, cell.memory_size):
            cell.memory[int(index)] = value

class I_Draw(Instruction):
    def __init__(self, command, arg1, arg2, arg3, arg4, arg5, arg6):
        self.command = default(command, "clear") #draw clear 0 0 0 0 0 0
        self.arg1 = default_type(arg1, "0")
        self.arg2 = default_type(arg2, "0")
        self.arg3 = default_type(arg3, "0")
        self.arg4 = default_type(arg4, "0")
        self.arg5 = default_type(arg5, "0")
        self.arg6 = default_type(arg6, "0")

    def new(args: list[str], **kwargs):
        return I_Draw(get_index(args, 0), get_index_type(args, 1), get_index_type(args, 2), get_index_type(args, 3), get_index_type(args, 4), get_index_type(args, 5), get_index_type(args, 6))
        
    def execute(self, interpreter):
        #if command in ["clear", "color", "col", "stroke", "line", "rect", "lineRect", "poly", "linePoly", "triangle", "image", "print", "translate", "scale", "rotate", "reset"]
        arg1 = self.arg1.get_coerced(interpreter)
        arg2 = self.arg2.get_coerced(interpreter)
        arg3 = self.arg3.get_coerced(interpreter)
        arg4 = self.arg4.get_coerced(interpreter)
        arg5 = self.arg5.get_coerced(interpreter)
        arg6 = self.arg6.get_coerced(interpreter)

        match self.command:
            case "clear":
                r = max(0, min(255, int(arg1)))
                g = max(0, min(255, int(arg2)))
                b = max(0, min(255, int(arg3)))
                draw = draw_call.Clear((r, g, b, 255))

            case "color":
                r = max(0, min(255, int(arg1)))
                g = max(0, min(255, int(arg2)))
                b = max(0, min(255, int(arg3)))
                a = max(0, min(255, int(arg4)))
                draw = draw_call.Color((r, g, b, a))
            
            case "col":
                r, g, b, a = variables.unpack_color(arg1)
                draw = draw_call.Color((r, g, b, a))

            case "stroke":
                draw = draw_call.Stroke(arg1)

            case "line":
                draw = draw_call.Line((arg1, arg2), (arg3, arg4))

            case "rect":
                draw = draw_call.Rect((arg1, arg2), (arg3, arg4))

            case "lineRect":
                draw = draw_call.LineRect((arg1, arg2), (arg3, arg4))

            case "poly":
                draw = draw_call.Poly((arg1, arg2), int(arg3), arg4, arg5)

            case "linePoly":
                draw = draw_call.LinePoly((arg1, arg2), int(arg3), arg4, arg5)

            case "triangle":
                draw = draw_call.Triangle((arg1, arg2), (arg3, arg4), (arg5, arg6))

            case "image":
                pass

            case "print":
                if isinstance(self.arg3, variables.Variable) and self.arg3.var_name in ["center", "top", "bottom", "left", "right", "topLeft", "topRight", "bottomLeft", "bottomRight"]:
                    align = self.arg3.var_name
                else:
                    align = "bottomLeft"

                draw = draw_call.Print((arg1, arg2), interpreter.print_buffer, align)
                interpreter.print_buffer = ""

            case "translate":
                draw = draw_call.Translate((arg1, arg2))

            case "scale":
                draw = draw_call.Scale((arg1, arg2))

            case "rotate":
                draw = draw_call.Rotate(arg3)

            case "reset":
                draw = draw_call.Reset()

            case _:
                r = max(0, min(255, int(arg1)))
                g = max(0, min(255, int(arg2)))
                b = max(0, min(255, int(arg3)))
                draw = draw_call.Clear((r, g, b, 255))
        interpreter.draw_buffer.append(draw)

class I_Print(Instruction):
    def __init__(self, text):
        self.text = default_type(text, '"frog"')

    def new(args: list[str], **kwargs):
        return I_Print(get_index_type(args, 0))

    def execute(self, interpreter):
        value = self.text.get_value(interpreter)
        if isinstance(value, float):
            interpreter.print_buffer += f"{value:.4f}".rstrip("0").rstrip(".")
        elif value is None:
            interpreter.print_buffer += "null"
        else:
            interpreter.print_buffer += str(value).replace(r"\n", "\n")

class I_Format(Instruction):
    def __init__(self, text):
        self.text = default_type(text, '"frog"')

    def new(args: list[str], **kwargs):
        return I_Format(get_index_type(args, 0))

    def execute(self, interpreter):
        value = self.text.get_value(interpreter)
        if isinstance(value, float):
            text = f"{value:.4f}".rstrip("0").rstrip(".")
        elif value is None:
            text = "null"
        else:
            text = str(value).replace(r"\n", "\n")

        for i in range(0,10):
            if re.search(r"\{" + str(i) + r"\}", interpreter.print_buffer):
                interpreter.print_buffer = re.sub(r"\{" + str(i) + r"\}", text, interpreter.print_buffer, 1)
                break
            

#Block Control
class I_Drawflush(Instruction):
    def __init__(self, display):
        self.display = default_type(display, "display1")

    def new(args: list[str], **kwargs):
        return I_Drawflush(get_index_type(args, 0))

    def execute(self, interpreter):
        display = self.display.get_value(interpreter)
        if isinstance(display, blocks.Display):
            display.draw_buffer.extend(interpreter.draw_buffer)
        interpreter.draw_buffer = []

class I_Printflush(Instruction):
    def __init__(self, message):
        self.message = default_type(message, "message1")

    def new(args: list[str], **kwargs):
        return I_Printflush(get_index_type(args, 0))

    def execute(self, interpreter):
        message = self.message.get_value(interpreter)
        if isinstance(message, blocks.Message):
            message.message = interpreter.print_buffer
        interpreter.print_buffer = ""

class I_Getlink(Instruction):
    def __init__(self, output, index):
        self.output = default_type(output, "result")
        self.index = default_type(index, "0")

    def new(args: list[str], **kwargs):
        return I_Getlink(get_index_type(args, 0), get_index_type(args, 1))

    def execute(self, interpreter):
        index = self.index.get_coerced(interpreter)
        if int(index) in range(0, len(interpreter.links)):
            self.output.set_value(interpreter.environment.get(list(interpreter.links.values())[int(index)]), interpreter)
        else:
            self.output.set_value(None, interpreter)

class I_Control(Instruction):
    def __init__(self, value, target, arg1, arg2, arg3, arg4): #control balls block1 0 0 0 0
        self.value = default(value, "enabled")
        self.target = default_type(target, "block1")
        self.arg1 = default_type(arg1, "0")
        self.arg2 = default_type(arg2, "0")
        self.arg3 = default_type(arg3, "0")
        self.arg4 = default_type(arg4, "0")

    def new(args: list[str], **kwargs):
        return I_Control(get_index(args, 0), get_index_type(args, 1), get_index_type(args, 2), get_index_type(args, 3), get_index_type(args, 4), get_index_type(args, 5))

    def execute(self, interpreter):
        target = self.target.get_value(interpreter)
        match self.value:
            case "enabled":
                if "enabled" in dir(target):
                    target.enabled = bool(self.arg1.get_coerced(interpreter))

class I_Sensor(Instruction):
    def __init__(self, output, target, sense): #sensor result block1 @copper
        self.output = default_type(output, "result")
        self.target = default_type(target, "block1")
        self.sense = default_type(sense, "@copper")

    def new(args: list[str], **kwargs):
        return I_Sensor(get_index_type(args, 0), get_index_type(args, 1), get_index_type(args, 2))

    def execute(self, interpreter):
        target = self.target.get_value(interpreter)
        sense = self.sense.get_value(interpreter)
        if isinstance(self.sense, variables.Sensable):
            self.output.set_value(sense(target), interpreter)
        else:
            self.output.set_value(None, interpreter)

#Operations
class I_Set(Instruction):
    def __init__(self, output, arg):
        self.output: variables.Type = default_type(output, "result")
        self.input: variables.Type = default_type(arg, "0")

    def new(args: list[str], **kwargs) -> Instruction:
        return I_Set(get_index_type(args, 0), get_index_type(args, 1))

    def execute(self, interpreter):
        self.output.set_value(self.input.get_value(interpreter), interpreter)

class I_Op(Instruction):
    def __init__(self, op, output, arg1, arg2):
        self.op: str = default(op, "add")
        self.output: variables.Type = default_type(output, "result")
        self.input1: variables.Type = default_type(arg1, "a")
        self.input2: variables.Type = default_type(arg2, "b")

    def new(args: list[str], **kwargs):
        return I_Op(get_index(args, 0), get_index_type(args, 1), get_index_type(args, 2), get_index_type(args, 3))

    def execute(self, interpreter):
        a_raw = self.input1.get_value(interpreter)
        a = self.input1.get_coerced(interpreter)
        b_raw = self.input2.get_value(interpreter)
        b = self.input2.get_coerced(interpreter)
        match self.op:
            case "add":
                result = a + b
            case "sub":
                result = a - b
            case "mul":
                result = a * b
            case "div":
                result = a / b
            case "idiv":
                result = a // b
            case "mod":
                result = a % b
            case "pow":
                result = pow(a,b)
            case "equal":
                if type(a_raw) == type(b_raw):
                    result = a_raw == b_raw
                else:
                    result = a == b
            case "notEqual":
                if type(a_raw) == type(b_raw):
                    result = a_raw != b_raw
                else:
                    result = a != b
            case "land":
                result = bool(a) and bool(b)
            case "lessThan":
                result = a < b
            case "lessThanEq":
                result = a <= b
            case "greaterThan":
                result = a > b
            case "greaterThanEq":
                result = a >= b
            case "strictEqual":
                if type(a_raw) == type(b_raw):
                    result = a_raw == b_raw
                else:
                    result = False
            case "shl":
                result = int(a) << int(b)
            case "shr":
                result = int(a) >> int(b)
            case "or":
                result = int(a) | int(b)
            case "and":
                result = int(a) & int(b)
            case "xor":
                result = int(a) ^ int(b)
            case "not":
                result = ~int(a)
            case "max":
                result = max(a, b)
            case "min":
                result = min(a, b)
            case "angle":
                result = math.degrees(math.atan2(a, b))
            case "angleDiff":
                a = ((a % 360) + 360) % 360
                b = ((b % 360) + 360) % 360
                result = min(a - b + 360 if (a - b) < 0 else a - b, b - a + 360 if (b - a) < 0 else b - a)
            case "len":
                result = math.hypot(a, b)
            case "noise":
                result = 0
            case "abs":
                result = abs(a)
            case "log":
                result = math.log(a)
            case "log10":
                result = math.log10(a)
            case "floor":
                result = math.floor(a)
            case "ceil":
                result = math.ceil(a)
            case "sqrt":
                result = math.sqrt(a)
            case "rand":
                result = random.uniform(0,a)
            case "sin":
                result = math.sin(a)
            case "cos":
                result = math.cos(a)
            case "tan":
                result = math.tan(a)
            case "asin":
                result = math.asin(a)
            case "acos":
                result = math.acos(a)
            case "atan":
                result = math.atan(a)
            case _:
                result = None
        self.output.set_value(result, interpreter)

class I_Packcolor(Instruction):
    def __init__(self, output, r, g, b, a):
        self.output = default_type(output, "result")
        self.r = default_type(r, "1")
        self.g = default_type(g, "0")
        self.b = default_type(b, "0")
        self.a = default_type(a, "1")

    def new(args: list[str], **kwargs):
        return I_Packcolor(get_index_type(args, 0), get_index_type(args, 1), get_index_type(args,2), get_index_type(args, 3), get_index_type(args, 4))

    def execute(self, interpreter):
        r = self.r.get_coerced(interpreter)
        g = self.g.get_coerced(interpreter)
        b = self.b.get_coerced(interpreter)
        a = self.a.get_coerced(interpreter)
        self.output.set_value(variables.pack_color_float(r, g, b, a), interpreter)

#Flow Control
class I_Wait(Instruction):
    def __init__(self, input_time):
        self.time = default_type(input_time, "0.5")

    def new(args: list[str], **kwargs):
        return I_Wait(get_index_type(args, 0))

    def execute(self, interpreter):
        interpreter.waiting = True
        interpreter.wait_until = time.time() + self.time.get_coerced(interpreter)

class I_Stop(Instruction):
    def __init__(self):
        pass

    def new(args: list[str], **kwargs):
        return I_Stop()

    def execute(self, interpreter):
        interpreter.halted = True

class I_End(Instruction):
    def __init__(self):
        pass

    def new(args: list[str], **kwargs):
        return I_End()

    def execute(self, interpreter):
        interpreter.counter = 0

class I_Jump(Instruction):
    def __init__(self, code_pos: int, condition: str, arg1, arg2):
        self.code_pos = default(code_pos, -1)
        self.condition = default(condition, "notEqual")
        self.input1 = default_type(arg1, "x")
        self.input2 = default_type(arg2, "false")

    def new(args: list[str], labels: dict[str, int], **kwargs):
        return I_Jump(get_label(get_index(args, 0), labels), get_index(args, 1), get_index_type(args, 2), get_index_type(args, 3))

    def execute(self, interpreter):
        a_raw = self.input1.get_value(interpreter)
        a = self.input1.get_coerced(interpreter)
        b_raw = self.input2.get_value(interpreter)
        b = self.input2.get_coerced(interpreter)
        result = False
        match self.condition:
            case "equal":
                if type(a_raw) == type(b_raw):
                    result = a_raw == b_raw
                else:
                    result = a == b
            case "notEqual":
                if type(a_raw) == type(b_raw):
                    result = a_raw != b_raw
                else:
                    result = a != b
            case "lessThan":
                result = a < b
            case "lessThanEq":
                result = a <= b
            case "greaterThan":
                result = a > b
            case "greaterThanEq":
                result = a >= b
            case "strictEqual":
                if type(a_raw) == type(b_raw):
                    result = a_raw == b_raw
                else:
                    result = False
            case "always":
                result = True
        
        if result and self.code_pos >= 0:
            interpreter.counter = self.code_pos

#World
class I_Setrate(Instruction):
    def __init__(self, rate):
        self.rate = default_type(rate, "10")

    def new(args: list[str], **kwargs):
        return I_Setrate(get_index_type(args, 0))

    def execute(self, interpreter):
        interpreter.ipt = int(self.rate.get_coerced(interpreter))

INSTRUCTION_LOOKUP = {
    'read': I_Read,
    'write': I_Write,
    'draw': I_Draw,
    'print': I_Print,
    'format': I_Format,
    'printflush': I_Printflush,
    'drawflush': I_Drawflush,
    'getlink': I_Getlink,
    'control': I_Control,
    'sensor': I_Sensor,
    'set': I_Set,
    'op': I_Op,
    'packcolor': I_Packcolor,
    'wait': I_Wait,
    'stop': I_Stop,
    'end': I_End,
    'jump': I_Jump,
    'setrate': I_Setrate,
}

REVERSE_LOOKUP = {}
for k, v in INSTRUCTION_LOOKUP.items():
    REVERSE_LOOKUP[v] = k

def get_label(value, labels):
    if value is None:
        return None 
    elif re.match(r"[0-9]+", value):
        return int(value)
    elif value in labels:
        return labels[value]
    else:
        return None

def get_index_type(l, i):
    try:
        return variables.to_type(l[i])
    except IndexError:
        return None

def get_index(l, i):
    try:
        return l[i]
    except IndexError:
        return None

def default_type(val, def_type):
    return variables.to_type(def_type) if val is None else val

def default(val, def_val):
    return def_val if val is None else val

#def add_instruction(name, arguments: list[tuple[str,bool,Any]], callback):
#    class NewInstruction(Instruction):
#        def new(args: list[str], **kwargs):
#            inst = NewInstruction()
#            for name, is_var, default_value in arguments:
#                setattr(inst, name, )