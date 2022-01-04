import pygame as pg
from Matrix_Class import Matrix,V
import numpy as np
from pygame import gfxdraw
from Tile_Class import Tile
from random import choice
debug=False

class Player():
    def __init__(self,name="nameless"):
        self.name=name
        self.score=0
        self.hand=[None for i in range(6)]
    # def draw(self,bag=["apple"]):
    #     if debug:
    #         assert bag
    #     tile_index=choice(range(len(bag)))
    #     self.hand.append(bag[tile_index])
    #     del bag[tile_index]
    #     return self.hand[-1]
    def draw_hand(self,bag):
        for i in range(len(self.hand)):
            self.draw(i,bag)
    def draw(self,i,bag=["apple"]):
        if bag:
            tile_index=choice(range(len(bag)))
            self.hand[i]=bag[tile_index]
            self.hand[i].set_hand_pos(i)
            self.hand[i]
            del bag[tile_index]
            return self.hand[i]
