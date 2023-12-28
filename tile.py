from random import randint

class Tile:

    EMPTY = 0
    WALL = 1
    DOOR = 2
    INTERNAL_WALL = 3
    EXIT = 4
    ITEM = 5
    MINE = 6
    FOG = ["░", "▒", "▓"]

    class Char:
        
        H_MAIN_DOOR = f"\033[98m─\033[0m"
        V_MAIN_DOOR = f"\033[98m|\033[0m"
        H_PARENT_DOOR = f"\033[95m─\033[0m"
        V_PARENT_DOOR = f"\033[95m|\033[0m"
        H_CHILD_DOOR = f"\033[94m─\033[0m"
        V_CHILD_DOOR = f"\033[94m|\033[0m"

        UP_LEFT_WALL = "\033[90m╔\033[0m"
        UP_RIGHT_WALL = "\033[90m╗\033[0m"
        DOWN_LEFT_WALL = "\033[90m╚\033[0m"
        DOWN_RIGHT_WALL = "\033[90m╝\033[0m"
        H_WALL = "\033[90m═\033[0m"
        V_WALL = "\033[90m║\033[0m"

        ITEMS = "\033[93m■\033[0m"
        ITEM = "\033[93m·\033[0m"

        INTERNAL_WALL = "\033[90m#\033[0m"
        MINE = "\033[91;5m·\033[0m"

        PLAYER = "\033[98m×\033[0m"

    def __init__(self, id=0) -> None:
        self.id = id
        self.char = " "
        self.entity_on = None
        self.resource = None
        self.visible = True
    
    def as_parent_door(self, door_y, height):
        self.char = Tile.Char.H_PARENT_DOOR if door_y in [0, height - 1] else Tile.Char.V_PARENT_DOOR 
        self.id = Tile.DOOR
    
    def as_exit_door(self, door_y, height):
        self.char = Tile.Char.H_MAIN_DOOR if door_y in [0, height - 1] else Tile.Char.V_MAIN_DOOR 
        self.id = Tile.EXIT

    def as_child_door(self, door_y, height):
        self.char = Tile.Char.H_CHILD_DOOR if door_y in [0, height - 1] else Tile.Char.V_CHILD_DOOR 
        self.id = Tile.DOOR
    
    def as_item(self, resource):
        if self.id == Tile.ITEM:
            if type(self.resource) == list:
                self.resource.append(resource)
            self.char = Tile.Char.ITEMS
        else:
            self.id = Tile.ITEM
            self.char = Tile.Char.ITEM
            self.resource = [resource]
    
    def as_internal_wall(self):
        self.id = Tile.INTERNAL_WALL
        self.char = Tile.Char.INTERNAL_WALL
    
    def as_mine(self):
        self.id = Tile.MINE
        self.char = Tile.Char.MINE
    
    def as_wall(self, i, j, width, height):
        self.id = Tile.WALL
        if i == 0 and j == 0: self.char = Tile.Char.UP_LEFT_WALL
        elif i == 0 and j == width - 1: self.char = Tile.Char.UP_RIGHT_WALL
        elif i == height - 1 and j == 0: self.char = Tile.Char.DOWN_LEFT_WALL
        elif i == height - 1 and j == width - 1: self.char = Tile.Char.DOWN_RIGHT_WALL
        elif i == 0 or i == height - 1: self.char = Tile.Char.H_WALL
        else: self.char = Tile.Char.V_WALL
    
    def as_empty(self):
        self.id = Tile.EMPTY
        self.char = " "
        self.resource = None
    
    def override_by(self, entity_char):
        self.entity_on = entity_char
    
    def override_off(self, clear=False):
        self.entity_on = None
        if clear:
            self.char = " "
            self.id = Tile.EMPTY
            self.resource = None
    
    def __repr__(self) -> str:
        if self.visible:
            if self.entity_on != None:
                return self.entity_on
            return self.char
        return Tile.FOG[randint(0, 2)]
