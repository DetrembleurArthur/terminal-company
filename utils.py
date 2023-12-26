from datetime import datetime
from os import get_terminal_size

DEBUG = True

def debug(text):
    print(f"\033[93m[DEBUG {datetime.now()}]\033[0m {text}")

class Dimensions:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
    
    def __repr__(self) -> str:
        return f"{self.width}x{self.height}"

class Position:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def translate(self, vector):
        return Position(self.x + vector.x, self.y + vector.y)
    
    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

def terminal_dimensions():
    return Dimensions(*get_terminal_size())

Vector = Position

if __name__ == "__main__":
    print(terminal_dimensions())
