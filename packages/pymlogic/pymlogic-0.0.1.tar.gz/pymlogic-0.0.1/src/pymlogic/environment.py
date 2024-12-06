import interpreter, instructions, variables, parser, time, blocks

class FullEnv: # a future class for a more feature rich environment
    pass

class Env: # a simple environment class that defines just the basic logic blocks
    def __init__(self):
        self.procs: list[interpreter.Interpreter] = []
        self.blocks: dict[blocks.Block] = {}
        self.halted = False

    def tick(self) -> bool:
        halt = True
        for proc in self.procs:
            proc.execute_tick()
            if not proc.halted:
                halt = False
        self.halted = halt

    def wait(self):
        try:
            start_time
        except NameError:
            start_time = time.time()
        elapsed_time = time.time() - start_time
        time.sleep(max(0, 1/60 - elapsed_time))
        start_time = time.time()

    def add(self, block: blocks.Block, pos: tuple[int, int]):
        self.blocks[pos] = block
        block.x, block.y = pos
        block._add_env(self)

    def get(self, pos: tuple[int, int]):
        try:
            return self.blocks[pos]
        except KeyError:
            return None

    def __repr__(self):
        return f"Environment(blocks = [{", ".join(self.blocks)}])"
