from random import randint, random, shuffle
from utils import debug, Dimensions, terminal_dimensions, Position, Vector
from math import ceil
from player import *
from tile import Tile

class Room:

    counter = 1

    def __init__(self, doors_to_achieve, depth, items_pool, previous_door_position=None, parent_room=None) -> None:
        debug(f"doors to achieve: {doors_to_achieve}")
        self.wall_placement_rate = min(random(), 0.80) ** 2
        self.mine_placement_rate = 0.02
        self.light_on = random() < 0.30
        self.content_generation = [
            (self.wall_placement_rate, Tile.as_internal_wall, Tile.adapt_internal_walls),
            (self.mine_placement_rate, Tile.as_mine, None)
        ]
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
        self.doors_to_achieve = doors_to_achieve
        self.child_rooms = {}
        self.parent_room = parent_room
        self.main_exit_position = Position(0, 0)
        self.__init_tiles()
        self.__build_tiles()
    
    def __init_dimensions(self):
        rows = randint(3 if len(self.items) == 0 else 5, 17)
        cols = randint(3 if len(self.items) == 0 else 5, 17)
        rows += int(rows % 2 == 0)
        cols += int(cols % 2 == 0)
        self.dimensions = Dimensions(width=cols, height=rows)
        debug(f"room dimensions : {cols}x{rows} : {cols} columns & {rows} rows")
    
    def __init_tiles(self):
        [self.tiles.append([Tile() for _ in range(self.dimensions.width)]) for _ in range(self.dimensions.height)]

    def tile_at(self, position: Position):
        return self.tiles[position.y][position.x]

    def __build_tiles(self):
        self.__build_doors()
        self.__build_external_walls()
        # internal wall + items placement
        placements = self.__get_available_content_placements()
        self.__build_items(placements)
        self.__build_content(placements)

    def __build_doors(self):
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
            if i == 0:
                if self.parent_room != None: # parent room
                    self.child_rooms[door.to_tuple()] = {"room": self.parent_room, "door_pos" : self.previous_door_position}
                    self.tiles[door.y][door.x].as_parent_door(door.y, self.dimensions.height)
                else: # main exit
                    self.main_exit_position = door
                    self.child_rooms[door.to_tuple()] = {"room": None, "door_pos" : None}
                    self.tiles[door.y][door.x].as_exit_door(door.y, self.dimensions.height)
            else: # basic child doors
                doors_to_achieve = ceil(self.remaining_doors * (random()**2)) if i < self.door_number - 1 else self.remaining_doors
                self.remaining_doors -= doors_to_achieve
                child_room = Room(doors_to_achieve=doors_to_achieve, depth=self.depth+1, items_pool=self.items_pool, previous_door_position=door.to_tuple(), parent_room=self)
                self.child_rooms[door.to_tuple()] = {"room": child_room, "door_pos" : child_room.doors[0].to_tuple()}
                self.tiles[door.y][door.x].as_child_door(door.y, self.dimensions.height)
            i += 1
    
    def __build_external_walls(self):
        for i in range(self.dimensions.height):
            for j in range(self.dimensions.width):
                if i == 0 or i == self.dimensions.height - 1 or j == 0 or j == self.dimensions.width - 1:
                    if self.tiles[i][j].id == Tile.EMPTY:
                        self.tiles[i][j].as_wall(i, j, self.dimensions.width, self.dimensions.height)
    
    def __get_available_content_placements(self):
        placements = []
        for i in range(1, self.dimensions.height - 1):
            for j in range(1, self.dimensions.width - 1):
                if self.tiles[i][j].id == Tile.EMPTY:
                    potential_doors = [self.tiles[i - 1][j].id, self.tiles[i + 1][j].id, self.tiles[i][j - 1].id, self.tiles[i][j + 1].id]
                    if not Tile.DOOR in potential_doors and not Tile.EXIT in potential_doors:
                        placements.append(Position(j, i))
        shuffle(placements)
        return placements

    def __build_items(self, placements: list):
        for item in self.items:
            i = randint(0, len(placements) - 1)
            pos = placements.pop(i)
            tile: Tile = self.tiles[pos.y][pos.x]
            tile.as_item(item)
    
    def __build_content(self, placements: list):
        for pos in placements: 
            tile: Tile = self.tiles[pos.y][pos.x]
            for generator in self.content_generation:
                if random() < generator[0]:
                    generator[1](tile)
        for pos in placements: 
            tile: Tile = self.tiles[pos.y][pos.x]
            for generator in self.content_generation:
                if generator[2] != None:
                    generator[2](tile,self.tiles, pos)
        placements = [place for place in placements if self.tiles[place.y][place.x].id == Tile.EMPTY]
    
    def count_rooms(self):
        counter = 1
        for room in self.child_rooms.values():
            if room["room"] != self.parent_room:
                counter += room.count_rooms()
        return counter
    
    def at_door_placement(self, player_position, door_pos, entity_char):
        pos = door_pos if type(door_pos) == Position else Position(door_pos[0], door_pos[1])
        if pos.x == 0: player_position.x = pos.x + 1
        elif pos.x == self.dimensions.width - 1: player_position.x = self.dimensions.width - 2
        else: player_position.x = pos.x
        if pos.y == 0: player_position.y = pos.y + 1
        elif pos.y == self.dimensions.height - 1: player_position.y = self.dimensions.height - 2
        else: player_position.y = pos.y
        self.tiles[player_position.y][player_position.x].override_by(entity_char)
        return self.tiles[player_position.y][player_position.x]
    
    def show(self, player):
        term_dim = terminal_dimensions()
        x = term_dim.width // 2 - self.dimensions.width # car une case prend 2 caractères (la case + le vide)
        y = term_dim.height // 2 - self.dimensions.height // 2
        print("\033c")
        print(f"Room {self.id} (light {'on' if self.light_on else 'off'})")
        print(f"Items {len(self.items)}")
        print(f"Remain items {len(self.items) - len([item for item in player.items if item in self.items])}")
        i = 0
        for row in self.tiles:
            j = 0
            #print(f"\033[{i + y};{x-3}H{i}", end="")
            for col in row:
                if self.light_on:
                    col.visible = True
                else:
                    col.visible = dist(player.position.x, j//2, player.position.y, i) < player.render_distance
                print(f"\033[{i + y};{j + x}H{col}", end="")
                j += 2
            i += 1
            print()
        i = 0
        '''for col in row:
            print(f"\033[{y + self.dimensions.height};{i*2 + x}H{i}", end="")
            i += 1'''
        print("\n")
