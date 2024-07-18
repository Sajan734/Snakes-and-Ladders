import pygame as pg
import pygame_menu
import pygame_gui
from pygame.locals import *
import pygame_menu
import time 
import os
import json
from datetime import datetime, timezone



SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000

blue = (0, 0, 255)
pg.font.init()
font = pg.font.Font(None, 20)
fontM = pg.font.Font(None, 40)
fontXL = pg.font.Font(None, 50)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Snakes and Ladders")


clock = pg.time.Clock()

def create_grid(start_margin_x, start_margin_y, side_length):
    box_length = side_length/10
    for i in range(0, 100):
        """[100][99][98][97]
        [93][94][95]     [96]"""
        scale = i % 11
        if i % 11 == 0:
          start_margin_x *= -1
          if scale < 0:
            scale = -10
          else:
            scale = 0
        
        side_margin = start_margin_x + scale * (box_length )
        top_margin = start_margin_y + i // 11 * (box_length)

        num = str(100 - i)
        num_img = font.render(num, True, blue, (255, 255, 255))
        rectangle = pg.Rect(0, 0, box_length, box_length) 
        screen.blit(num_img, (side_margin, top_margin ), rectangle)

    
run = True
while run:
    create_grid(0, 0, 500)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.QUIT
                