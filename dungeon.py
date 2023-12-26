from random import randint, random, shuffle
from utils import debug, Dimensions, terminal_dimensions, Position, Vector
from math import ceil
import sys
from player import *

class Tile:

    EMPTY = 0
    WALL = 1
    DOOR = 2
    EXIT = 4
    INTERNAL_WALL = 3
    ITEM = 5


    def __init__(self, id=0) -> None:
        self.id = id
        self.char = " "
        self.player_on = False
        self.resource = None
    
    def __repr__(self) -> str:
        return self.char if not self.player_on else "×"

class Room:

    counter = 1

    def __init__(self, doors_to_achieve, previous_door_position=None, parent_room=None) -> None:
        debug(f"doors to achieve: {doors_to_achieve}")
        self.items = []
        self.id = Room.counter
        Room.counter += 1
        self.previous_door_position = previous_door_position
        self.dimensions = None
        self.tiles = []
        self.__init_dimensions()
        self.doors = []
        self.door_number = randint(1, (self.dimensions.width // 2) * 2 + (self.dimensions.height // 2) * 2)
        if self.door_number > doors_to_achieve:
            self.door_number = doors_to_achieve + 1
        elif self.door_number == 1 and doors_to_achieve > 0:
            self.door_number += 1
        self.remaining_doors = doors_to_achieve - (self.door_number - 1)
        debug(f"remaining doors: {self.remaining_doors}")
        self.wall_placement_rate = random()
        self.item_placement_rate = random() ** 4
        self.doors_to_achieve = doors_to_achieve
        self.child_rooms = {}
        self.parent_room = parent_room
        self.main_exit_position = Position(0, 0)
        self.__init_tiles()
        self.__build_tiles()
    
    def __init_dimensions(self):
        rows = randint(3, 11)
        cols = randint(3, 11)
        rows += int(rows % 2 == 0)
        cols += int(cols % 2 == 0)
        self.dimensions = Dimensions(width=cols, height=rows)
        debug(f"room dimensions : {cols}x{rows} : {cols} columns & {rows} rows")
    
    def __init_tiles(self):
        [self.tiles.append([Tile() for _ in range(self.dimensions.width)]) for _ in range(self.dimensions.height)]

    def __build_tiles(self):
        debug(f"doors: {self.door_number} for {self.dimensions}")
        xpos = [x for x in range(1, self.dimensions.width, 2)]
        ypos = [y for y in range(1, self.dimensions.height, 2)]
        [self.doors.extend([Position(x=x, y=0), Position(x=x, y=self.dimensions.height - 1)]) for x in xpos]
        [self.doors.extend([Position(x=0, y=y), Position(x=self.dimensions.width - 1, y=y)]) for y in ypos]
        shuffle(self.doors)
        i = 0
        # doors placement
        for door in self.doors:
            if i >= self.door_number: break
            color = None
            if i == 0:
                if self.parent_room != None: # parent room
                    self.child_rooms[door.to_tuple()] = {"room": self.parent_room, "door_pos" : self.previous_door_position}
                    color = "95"
                    self.tiles[door.y][door.x].id = Tile.DOOR
                else: # main exit
                    self.main_exit_position = door
                    self.child_rooms[door.to_tuple()] = {"room": None, "door_pos" : None}
                    color = "98"
                    self.tiles[door.y][door.x].id = Tile.EXIT
            else: # basic child doors
                doors_to_achieve = ceil(self.remaining_doors * (random()**2)) if i < self.door_number - 1 else self.remaining_doors
                self.remaining_doors -= doors_to_achieve
                child_room = Room(doors_to_achieve=doors_to_achieve, previous_door_position=door.to_tuple(), parent_room=self)
                self.child_rooms[door.to_tuple()] = {"room": child_room, "door_pos" : child_room.doors[0].to_tuple()}
                color = "94"
                self.tiles[door.y][door.x].id = Tile.DOOR
            
            if door.y == 0 or door.y == self.dimensions.height - 1:
                self.tiles[door.y][door.x].char = f"\033[{color}m─\033[0m"
            else:
                self.tiles[door.y][door.x].char = f"\033[{color}m|\033[0m"
            
            i += 1
        # external wall placements
        for i in range(self.dimensions.height):
            for j in range(self.dimensions.width):
                if i == 0 or i == self.dimensions.height - 1 or j == 0 or j == self.dimensions.width - 1:
                    if self.tiles[i][j].id == Tile.EMPTY:
                        self.tiles[i][j].id = Tile.WALL
                        if i == 0 and j == 0: self.tiles[i][j].char = "\033[90m╔\033[0m"
                        elif i == 0 and j == self.dimensions.width - 1: self.tiles[i][j].char = "\033[90m╗\033[0m"
                        elif i == self.dimensions.height - 1 and j == 0: self.tiles[i][j].char = "\033[90m╚\033[0m"
                        elif i == self.dimensions.height - 1 and j == self.dimensions.width - 1: self.tiles[i][j].char = "\033[90m╝\033[0m"
                        elif i == 0 or i == self.dimensions.height - 1: self.tiles[i][j].char = "\033[90m═\033[0m"
                        else: self.tiles[i][j].char = "\033[90m║\033[0m"
                elif self.tiles[i][j].id == Tile.EMPTY:
                    if i > 1 and i < self.dimensions.height - 2 and j > 1 and j < self.dimensions.width - 2:
                        if random() < self.wall_placement_rate:
                            self.tiles[i][j].id = Tile.INTERNAL_WALL
                            self.tiles[i][j].char = "\033[90m■\033[0m"
                        elif random() < self.item_placement_rate:
                            self.tiles[i][j].id = Tile.ITEM
                            self.tiles[i][j].char = "\033[93m·\033[0m"
                            self.tiles[i][j].resource = Item(randint(5, 150), randint(1, 50))

    
    def count_rooms(self):
        counter = 1
        for room in self.child_rooms.values():
            if room["room"] != self.parent_room:
                counter += room.count_rooms()
        return counter
    
    def at_door_placement(self, player_position, door_pos):
        pos = door_pos if type(door_pos) == Position else Position(door_pos[0], door_pos[1])
        if pos.x == 0: player_position.x = pos.x + 1
        elif pos.x == self.dimensions.width - 1: player_position.x = self.dimensions.width - 2
        else: player_position.x = pos.x
        if pos.y == 0: player_position.y = pos.y + 1
        elif pos.y == self.dimensions.height - 1: player_position.y = self.dimensions.height - 2
        else: player_position.y = pos.y
        self.tiles[player_position.y][player_position.x].player_on = True
    
    def show(self):
        term_dim = terminal_dimensions()
        x = term_dim.width // 2 - self.dimensions.width # car une case prend 2 caractères (la case + le vide)
        y = term_dim.height // 4 - self.dimensions.height // 2
        print("\033c")
        print(f"Room {self.id}")
        print(f"Rarity {self.item_placement_rate:.2f}%")
        i = 0
        for row in self.tiles:
            j = 0
            print(f"\033[{i + y};{x-3}H{i}", end="")
            for col in row:
                print(f"\033[{i + y};{j + x}H{col}", end="")
                j += 2
            i += 1
            print()
        i = 0
        for col in row:
            print(f"\033[{y + self.dimensions.height};{i*2 + x}H{i}", end="")
            i += 1
        print("\n")


class Dungeon:

    def __init__(self, room_number=50) -> None:
        self.room_number = room_number
        self.player = Player()
    
    def start(self):
        self.main_room = Room(doors_to_achieve=self.room_number - 1)
        self.current_room = self.main_room
        self.player_position = Position(0, 0)
        self.current_room.at_door_placement(self.player_position, self.current_room.main_exit_position)
    
    def loop(self):
        movements = {
            "u" : Vector(0, -1),
            "d" : Vector(0, 1),
            "r" : Vector(1, 0),
            "l" : Vector(-1, 0)
        }
        self.running = True
        ticks = 0
        while self.running:
            self.current_room.show()
            command = input(f"\033[H(turn.{ticks})> ")
            if command in movements.keys():
                new_player_position = self.player_position.translate(movements[command])
                tile = self.current_room.tiles[new_player_position.y][new_player_position.x]
                if tile.id == Tile.EMPTY:
                    tile.player_on = True
                    self.current_room.tiles[self.player_position.y][self.player_position.x].player_on = False
                    self.player_position = new_player_position
                elif tile.id == Tile.DOOR:
                    self.current_room.tiles[self.player_position.y][self.player_position.x].player_on = False
                    child_room_info: dict = self.current_room.child_rooms[new_player_position.to_tuple()]
                    child_room_info["room"].at_door_placement(self.player_position, child_room_info["door_pos"])
                    self.current_room = child_room_info["room"]
                elif tile.id == Tile.EXIT:
                    print("\033cYour inventory")
                    self.player.show()
                    time.sleep(5)
                    sys.exit(0)
                elif tile.id == Tile.ITEM:
                    self.player.items.append(tile.resource)
                    tile.player_on = True
                    tile.id = Tile.EMPTY
                    tile.char = " "
                    self.current_room.tiles[self.player_position.y][self.player_position.x].player_on = False
                    self.player_position = new_player_position
            elif command == "restart":
                self.start()
            elif command == "inv":
                print("\033c")
                self.player.show()
                input("(enter)> ")
            ticks += 1

import time

if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.start()
    dungeon.loop()