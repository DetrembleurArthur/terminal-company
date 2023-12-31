from dungeon import Dungeon
from player import Player
from commands import Commands
from tile import Tile
from utils import Vector
import time
import audio
import sys

class Game:

    def __init__(self) -> None:
        self.player = Player()
        self.dungeon = Dungeon(self.player, room_number=50, difficulty=5)
        self.dungeon.init(self.player.char)
        self.player.render_distance = 2
        self.commands = Commands()
        self.last_direction = ("up", Vector(0, -1))
        self.wait_commands = []
        self.init_commands()
    
    def init_commands(self):
        self.commands["_default"] = lambda: self.commands.exec(self.last_direction[0])
        self.commands["up"] = lambda: self.weight_slowness(self.cmd_move_up)
        self.commands["down"] = lambda: self.weight_slowness(self.cmd_move_down)
        self.commands["right"] = lambda: self.weight_slowness(self.cmd_move_right)
        self.commands["left"] = lambda: self.weight_slowness(self.cmd_move_left)
        self.commands["break"] = self.cmd_break
        self.commands["start"] = self.cmd_start
        self.commands["exit"] = self.cmd_exit
        self.commands["inventory"] = self.cmd_inventory
    
    def weight_slowness(self, move_func):
        weight = self.player.get_weight()
        if weight >= 15:
            self.wait(lambda: audio.step(), weight // 30)
            self.wait(move_func)
        else:
            move_func()
    
    def cmd_move_up(self):
        self.last_direction = ("up", Vector(0, -1))
        self.player.char = Tile.Char.PLAYER_UP
        new_position = self.player.position.translate(Vector(0, -1))
        self.dungeon.move_player(new_position)
    
    def cmd_move_down(self):
        self.last_direction = ("down", Vector(0, 1))
        self.player.char = Tile.Char.PLAYER_DOWN
        new_position = self.player.position.translate(Vector(0, 1))
        self.dungeon.move_player(new_position)
    
    def cmd_move_right(self):
        self.last_direction = ("right", Vector(1, 0))
        self.player.char = Tile.Char.PLAYER_RIGHT
        new_position = self.player.position.translate(Vector(1, 0))
        self.dungeon.move_player(new_position)
    
    def cmd_move_left(self):
        self.last_direction = ("left", Vector(-1, 0))
        self.player.char = Tile.Char.PLAYER_LEFT
        new_position = self.player.position.translate(Vector(-1, 0))
        self.dungeon.move_player(new_position)
    
    def wait(self, callback, tick_number=1):
        self.wait_commands.extend([callback]*tick_number)

    
    def cmd_break(self):
        if self.last_direction != None:
            block_position = self.player.position.translate(self.last_direction[1])
            if self.dungeon.is_breakable(block_position):
                audio.prepare()
                self.wait(audio.hit_block, 2)
                self.wait(lambda: self.dungeon.break_block(block_position))

    def cmd_start(self):
        self.dungeon.init(self.player.char)

    def cmd_exit(self):
        print("\033c")
        sys.exit(0)

    def cmd_inventory(self):
        print("\033c")
        self.player.show()
        input("(enter)> ")
    
    def loop(self):
        self.dungeon.show()
        audio.jingle()
        self.running = True
        self.ticks = 0
        while self.running and self.player.hp > 0:
            self.dungeon.show()
            print(f"last direction {self.last_direction[0] if self.last_direction != None else 'none'}")
            if len(self.wait_commands) > 0:
                print(f"\033[H! {len(self.wait_commands) * '■'}")
                time.sleep(0.60)
                self.wait_commands.pop(0)()
            else:
                self.commands.exec(input(f"\033[H(turn.{self.ticks})> "))
            self.ticks += 1


if __name__ == "__main__":
    game = Game()
    game.loop()