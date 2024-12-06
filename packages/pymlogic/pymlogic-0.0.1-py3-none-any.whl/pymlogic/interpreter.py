import variables, time, blocks
from collections import OrderedDict

class Interpreter:
    def __init__(self, insts):
        self.instructions = insts
        self.instruction_pointer: int = 0
        self.variables: dict[str, variables.Type] = {}
        self.environment = None
        self.proc = None
        self.links = OrderedDict()
        self.link_names = {}

        self.ipt: int = 1000
        self.counter: int = 0

        self.halted = False

        self.waiting = False
        self.wait_until = 0

        self.print_buffer = ""
        self.draw_buffer = []

    def execute_tick(self):
        self.verify_links()
        if self.waiting and self.wait_until <= time.time():
            self.waiting = False
        for i in range(self.ipt):
            self.execute_instruction()
            if self.halted or self.waiting:
                break

    def execute_instruction(self):
        if not self.halted and not self.waiting:
            self.counter = 0 if self.instruction_pointer + 1 >= len(self.instructions) else self.instruction_pointer + 1
            self.instructions[self.instruction_pointer].execute(self)
            self.instruction_pointer = self.counter

    def verify_links(self):
        for name, pos in self.links.copy().items():
            if not self.environment.blocks[pos].LINK_NAME == name.rstrip("0123456789"):
                self.links.pop(name)
                self.add_link(pos)

    def add_link(self, link: [tuple[int, int], blocks.Block]):
        if isinstance(link, tuple):
            link_pos = link
        elif isinstance(link, blocks.Block):
            if link.environment is self.environment:
                link_pos = (link.x, link.y)
            else:
                raise Exception("Blocks must be in the same environment to link")
        else:
            raise Exception("Unlinkable object")
        if link_pos not in self.links:
            block_lname = self.environment.blocks[link_pos].LINK_NAME
    
            if block_lname not in self.link_names:
                self.link_names[block_lname] = 0
            self.link_names[block_lname] += 1
    
            self.links[f"{block_lname}{self.link_names[block_lname]}"] = link_pos

    def get_var(self, var_name):
        match var_name:
            case "@counter":
                return self.counter
            case "@ipt":
                return self.ipt
            case "@time":
                return time.time() * 1000
            case "@tick":
                return time.time() * 60
            case "@second":
                return time.time()
            case "@minute":
                return time.time() / 60
            case "@links":
                return len(self.links)
            case _:
                if var_name in self.links:
                    return self.environment.blocks[self.links[var_name]]
                elif var_name in self.variables:
                    return self.variables[var_name].get_value(self)
                else:
                    return None

    def set_var(self, var_name, value):
        match var_name:
            case "@counter":
                try:
                    self.counter = int(value)
                except ValueError:
                    pass
            case _:
                if var_name not in self.links:
                    self.variables[var_name] = variables.get_type(value)(value)