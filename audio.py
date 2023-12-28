from playsound import playsound
from threading import Thread
import time
from random import randint, random, shuffle
import os
import platform
# python -m pip install playsound==1.2.2
#https://pixabay.com/sound-effects/search/activation/
def play_sound(path, th=True):
    if th:
        Thread(target=lambda:playsound(path)).start()
    else:
        playsound(path)

def manage_path(path: str):
    preambule = os.getcwd()
    if platform.system() == "Windows":
        return preambule + path.replace("/", "\\")
    return preambule + path

def block():
    play_sound(manage_path("/res/audio/block.mp3"))

def hit_block():
    play_sound(manage_path("/res/audio/hit_block.mp3"))

def broke_block():
    play_sound(manage_path("/res/audio/broke_block.mp3"))

def collect_item():
    play_sound(manage_path("/res/audio/collect_item.mp3"))

def step():
    play_sound(manage_path(f"/res/audio/step-{randint(1, 3)}.mp3"))

def through_door():
    play_sound(manage_path(f"/res/audio/door-{randint(1, 2)}.mp3"))

def mine_explosion():
    play_sound(manage_path("/res/audio/mine_explosion.mp3"))

def mine_armed():
    play_sound(manage_path("/res/audio/mine_armed.mp3"))

def prepare():
    play_sound(manage_path("/res/audio/prepare.mp3"))

def jingle():
    play_sound(manage_path("/res/audio/jingle.mp3"), False)

if __name__ == "__main__":
    print(os.getcwd())
    print(platform.system())
    step()
    step()
    step()