from playsound import playsound
from threading import Thread
import time
from random import randint, random, shuffle

#https://pixabay.com/sound-effects/search/activation/
def play_sound(path):
	Thread(target=lambda:playsound(path)).start()

def block():
    play_sound("./res/audio/block.mp3")

def hit_block():
    play_sound("./res/audio/hit_block.mp3")

def broke_block():
    play_sound("./res/audio/broke_block.mp3")

def collect_item():
    play_sound("./res/audio/collect_item.mp3")

def step():
    play_sound(f"./res/audio/step-{randint(1, 3)}.mp3")

def through_door():
    play_sound(f"./res/audio/door-{randint(1, 2)}.mp3")

def mine_explosion():
    play_sound(f"./res/audio/mine_explosion.mp3")

def mine_armed():
    play_sound(f"./res/audio/mine_armed.mp3")
