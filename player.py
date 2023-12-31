from item import Item
from utils import *
import audio
from tile import Tile
from entity import Entity



class Player:

    def __init__(self) -> None:
        Entity.__init__(self, 100, Tile.Char.PLAYER_UP, Position(0, 0))
        self.items = []
        self.equipments = []
        self.render_distance = 2
        self.mine_armed = False
        self.on_mine = False
    
    def hit(self, dmg):
        self.hp = max(0, self.hp - dmg)
    
    def step_on_mine(self, is_mine):
        if is_mine:
            audio.mine_armed()
            self.mine_armed = True
            self.on_mine = True
        elif self.mine_armed:
            self.on_mine = False
    
    def must_explode(self):
        return self.mine_armed and not self.on_mine
    
    def get_weight(self):
        return sum(map(lambda item: item.weight, self.items))
    
    def show(self):
        print("\nItems:")
        for item in self.items:
            print(item)
        print(f"Total price: {sum(map(lambda item: item.price, self.items)):.2f}$")
        print(f"Total weight: {sum(map(lambda item: item.weight, self.items))}Kg")

if __name__ == "__main__":
    pass