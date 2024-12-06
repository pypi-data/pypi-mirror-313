class DrawCall:
    pass

class Clear(DrawCall):
    def __init__(self, color: tuple[int, int, int, int]):
        self.color = color

class Color(DrawCall): #used for both 'color' and 'col'
    def __init__(self, color: tuple[int, int, int, int]):
        self.color = color

class Stroke(DrawCall):
    def __init__(self, width: float):
        self.width = width

class Line(DrawCall):
    def __init__(self, start: tuple[float, float], end: tuple[float, float]):
        self.start = start
        self.end = end

class Rect(DrawCall):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.pos = pos
        self.size = size

class LineRect(DrawCall):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.pos = pos
        self.size = size

class Poly(DrawCall):
    def __init__(self, pos: tuple[float, float], sides: int, radius: float, rotation: float):
        self.pos = pos
        self.sides = sides
        self.radius = radius
        self.rotation = rotation

class LinePoly(DrawCall):
    def __init__(self, pos: tuple[float, float], sides: int, radius: float, rotation: float):
        self.pos = pos
        self.sides = sides
        self.radius = radius
        self.rotation = rotation

class Triangle(DrawCall):
    def __init__(self, pos1: tuple[float, float], pos2: tuple[float, float], pos3: tuple[float, float]):
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos3 = pos3

class Image(DrawCall):
    pass #unimplemented

class Print(DrawCall):
    def __init__(self, pos: tuple[float, float], text: str, align: str):
        self.pos = pos
        self.text = text
        self.align = align

class Translate(DrawCall):
    def __init__(self, offset: tuple[float, float]):
        self.offset = offset

class Scale(DrawCall):
    def __init__(self, scale: tuple[float, float]):
        self.scale = scale

class Rotate(DrawCall):
    def __init__(self, rotation: float):
        self.rotation = rotation

class Reset(DrawCall):
    pass