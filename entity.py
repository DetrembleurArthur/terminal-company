

from tile import Tile


class Entity:

    def __init__(self, hp, char, position) -> None:
        self.hp = hp
        self.char = char
        self.position = position

    def hit(self, dmg):
        self.hp = max(0, self.hp - dmg)