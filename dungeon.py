from random import randint
from utils import Position, Vector
from math import sqrt
import sys
from player import *
import audio
from tile import Tile
from room import Room
from commands import Commands


class Dungeon:

    def __init__(self, player, room_number=20, difficulty=5) -> None:
        self.room_number = room_number
        self.difficulty = difficulty
        self.current_tile: Tile = None
        self.player: Player = player
    
    def init(self):
        self.items = Item.dispatch(item_number=randint(15 + self.difficulty, 20 + self.difficulty), factor=self.difficulty**2)
        self.items_pool = Item.split_items(self.items, self.room_number, sqrt(1/self.room_number))
        self.main_room = Room(doors_to_achieve=self.room_number - 1, depth=0, items_pool=self.items_pool)
        self.current_room = self.main_room
        self.current_tile = self.current_room.at_door_placement(self.player.position, self.current_room.main_exit_position)
    
    def show(self):
        self.current_room.show(self.player)
        print(f"Total items {len(self.items)}")
        print(f"Remain items {len(self.items) - len([item for item in self.player.items if item in self.items])}")
    
    def entity_move_on(self, tile, entity, new_position):
        self.current_tile.override_off()
        tile.override_by(entity.char)
        entity.position = new_position
        if self.current_tile.id == Tile.MINE:
            audio.mine_explosion()
            self.player.hit(100)
            self.current_tile.as_empty()
        elif self.current_tile.id == Tile.ITEM:
            self.current_tile.as_empty()
        self.current_tile = tile
    
    def move(self, new_position: Vector):
        tile: Tile = self.current_room.tiles[new_position.y][new_position.x]
        if tile.id == Tile.EMPTY:
            audio.step()
            self.entity_move_on(tile, self.player, new_position)
        elif tile.id == Tile.MINE:
            audio.step()
            self.entity_move_on(tile, self.player, new_position)
            audio.mine_armed()
        elif tile.id == Tile.DOOR:
            audio.through_door()
            self.current_tile.override_off()
            child_room_info: dict = self.current_room.child_rooms[new_position.to_tuple()]
            self.current_tile = child_room_info["room"].at_door_placement(self.player.position, child_room_info["door_pos"])
            self.current_room = child_room_info["room"]
        elif tile.id == Tile.EXIT:
            print("\033cYour inventory")
            self.player.show()
            sys.exit(0)
        elif tile.id == Tile.ITEM:
            audio.step()
            audio.collect_item()
            self.player.items.extend(tile.resource)
            self.entity_move_on(tile, self.player, new_position)
        else:
            audio.block()
    
    def is_breakable(self, block_position: Position):
        tile = self.current_room.tile_at(block_position)
        return tile.id == Tile.INTERNAL_WALL

    def break_block(self, block_position: Position):
        audio.broke_block()
        tile = self.current_room.tile_at(block_position)
        tile.id = Tile.EMPTY
        tile.char = " "




if __name__ == "__main__":
    dungeon = Dungeon()
    dungeon.init()
    dungeon.test_loop()