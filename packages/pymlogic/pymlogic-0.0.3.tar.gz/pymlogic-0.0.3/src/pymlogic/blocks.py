class Block:
    LINK_NAME = "block"
    def __init__(self):
        self.x = None
        self.y = None
        self.environment = None

    def _add_env(self, env):
        self.environment = env

    def __repr__(self):
        return "block"

class Switch(Block):
    LINK_NAME = "switch"
    def __init__(self):
        super().__init__()
        self.enabled = True

    def __repr__(self):
        return "switch"

class Message(Block):
    LINK_NAME = "message"
    def __init__(self):
        super().__init__()
        self.message = ""

    def __repr__(self):
        return "message"

class Display(Block):
    LINK_NAME = "display"
    def __init__(self):
        super().__init__()
        self.draw_buffer = []

    def __repr__(self):
        return "logic-display"

class MemoryCell(Block):
    LINK_NAME = "cell"
    def __init__(self, size: int = 64):
        super().__init__()
        self.memory_size = size
        self.memory: list[float] = [0.0 for _ in range(size)]

    def __repr__(self):
        return "memory-cell"

class Processor(Block):
    LINK_NAME = "processor"
    def __init__(self, code: str, links: list[[tuple[int, int], Block]] = []):
        super().__init__()
        import pymlogic.interpreter as interpreter
        import pymlogic.parser as parser
        self.interpreter = interpreter.Interpreter(parser.parse(code))
        self.interpreter.proc = self
        self.to_be_linked = links

    def __repr__(self):
        return "processor"

    def _add_env(self, env):
        super()._add_env(env)
        self.interpreter.environment = env
        env.procs.append(self.interpreter)
        for link in self.to_be_linked:
            self.link(link)

    def link(self, link: [tuple[int, int], Block]):
        self.interpreter.add_link(link)