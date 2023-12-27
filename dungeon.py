from random import randint, random, shuffle
from utils import debug, Dimensions, terminal_dimensions, Position, Vector
from math import ceil, sqrt
import sys
from player import *

class Tile:

    EMPTY = 0
    WALL = 1
    DOOR = 2
    EXIT = 4
    INTERNAL_WALL = 3
    ITEM = 5

    FOG = ["░", "▒", "▓"]


    def __init__(self, id=0) -> None:
        self.id = id
        self.char = " "
        self.player_on = False
        self.resource = None
        self.visible = True
    
    def __repr__(self) -> str:
        if self.visible:
            return self.char if not self.player_on else "×"
        return Tile.FOG[randint(0, 2)]

class Room:

    counter = 1

    def __init__(self, doors_to_achieve, depth, items_pool, previous_door_position=None, parent_room=None) -> None:
        debug(f"doors to achieve: {doors_to_achieve}")
        self.items_pool: list = items_pool
        self.items = self.items_pool.pop()
        self.depth = depth
        self.id = Room.counter
        debug(f"{self.id} has {self.items}")

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
        self.doors_to_achieve = doors_to_achieve
        self.child_rooms = {}
        self.parent_room = parent_room
        self.main_exit_position = Position(0, 0)
        self.__init_tiles()
        self.__build_tiles()
    
    def __init_dimensions(self):
        rows = randint(3 if len(self.items) == 0 else 5, 11)
        cols = randint(3 if len(self.items) == 0 else 5, 11)
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
                child_room = Room(doors_to_achieve=doors_to_achieve, depth=self.depth+1, items_pool=self.items_pool, previous_door_position=door.to_tuple(), parent_room=self)
                self.child_rooms[door.to_tuple()] = {"room": child_room, "door_pos" : child_room.doors[0].to_tuple()}
                color = "94"
                self.tiles[door.y][door.x].id = Tile.DOOR
            
            if door.y == 0 or door.y == self.dimensions.height - 1:
                self.tiles[door.y][door.x].char = f"\033[{color}m─\033[0m"
            else:
                self.tiles[door.y][door.x].char = f"\033[{color}m|\033[0m"
            
            i += 1
        
        # item pick up
        
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
        # internal wall + items placement
        placements = []
        for i in range(2, self.dimensions.height - 2):
            for j in range(2, self.dimensions.width - 2):
                if self.tiles[i][j].id == Tile.EMPTY:
                    placements.append(Position(j, i))
        shuffle(placements)
        for item in self.items:
            pos = placements[randint(0, len(placements) - 1)]
            tile: Tile = self.tiles[pos.y][pos.x]
            tile.id = Tile.ITEM
            if type(tile.resource) == list:
                tile.resource.append(item)
                tile.char = "\033[93m■\033[0m"
            else:
                tile.char = "\033[93m·\033[0m"
                tile.resource = [item]
        for pos in placements: 
            tile: Tile = self.tiles[pos.y][pos.x]
            if tile.id == Tile.EMPTY and random() < self.wall_placement_rate:
                tile.id = Tile.INTERNAL_WALL
                tile.char = "\033[90m#\033[0m"

    
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
    
    def show(self, player_pos=None, player=None):
        term_dim = terminal_dimensions()
        x = term_dim.width // 2 - self.dimensions.width # car une case prend 2 caractères (la case + le vide)
        y = term_dim.height // 2 - self.dimensions.height // 2
        print("\033c")
        print(f"Room {self.id}")
        print(f"Items {len(self.items)}")
        i = 0
        for row in self.tiles:
            j = 0
            print(f"\033[{i + y};{x-3}H{i}", end="")
            for col in row:
                if player_pos != None:
                    d = sqrt((player_pos.x - j//2)**2 + (player_pos.y - i)**2)
                    col.visible = d < player.render_distance
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

    def __init__(self, room_number=20, difficulty=5) -> None:
        self.room_number = room_number
        self.difficulty = difficulty
        self.player = Player()
    
    def start(self):
        self.items = Item.dispatch(item_number=randint(15 + self.difficulty, 20 + self.difficulty), factor=self.difficulty**2)
        self.items_pool = Item.split_items(self.items, self.room_number, sqrt(1/self.room_number))
        self.main_room = Room(doors_to_achieve=self.room_number - 1, depth=0, items_pool=self.items_pool)
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
        wait_ticks = -1
        last_command = ""
        last_direction = "none"
        while self.running:
            self.current_room.show(self.player_position, self.player)
            print(f"last direction {last_direction}")
            print(f"Total items {len(self.items)}")
            print(f"Remain items {len(self.items) - len([item for item in self.player.items if item in self.items])}")
            if wait_ticks < 0:
                command = input(f"\033[H(turn.{ticks})> ")
                if len(command) == 0 and last_command in movements.keys(): command = last_command
                if command in movements.keys():
                    last_direction = command
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
                        self.player.items.extend(tile.resource)
                        tile.player_on = True
                        tile.id = Tile.EMPTY
                        tile.char = " "
                        self.current_room.tiles[self.player_position.y][self.player_position.x].player_on = False
                        self.player_position = new_player_position
                elif command == "break":
                    if last_command in movements.keys():
                        break_block_position = self.player_position.translate(movements[last_command])
                        tile = self.current_room.tiles[break_block_position.y][break_block_position.x]
                        if tile.id == Tile.INTERNAL_WALL:
                            wait_ticks = 3
                elif command == "restart":
                    self.start()
                elif command == "inv":
                    print("\033c")
                    self.player.show()
                    input("(enter)> ")
                if len(command) != 0:
                    last_command = command
            elif wait_ticks > 0:
                print(f"\033[H(turn.{ticks})> [wait {wait_ticks}]")
                time.sleep(0.75)
                wait_ticks -= 1
            elif wait_ticks == 0:
                if last_command == "break":
                    break_block_position = self.player_position.translate(movements[last_direction])
                    tile = self.current_room.tiles[break_block_position.y][break_block_position.x]
                    if tile.id == Tile.INTERNAL_WALL:
                        tile.id = Tile.EMPTY
                        tile.char = " "
                wait_ticks = -1
                continue
            ticks += 1

import time

if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.start()
    dungeon.loop()