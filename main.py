import pygame as pg
import pygame_menu
import pygame_gui
from pygame.locals import *
import pygame_menu
import time 
import os
import json
from datetime import datetime, timezone

#Initialize Pygame window
pg.init()

screen = pg.display.set_mode((600, 400))

def open_customize():
  menu._open(customize_menu)

def main_screen():
    print('main_screen') # add the pygame code here


main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.widget_font = pygame_menu.font.FONT_MUNRO


menu = pygame_menu.Menu('Snakes and Ladders', 600, 400,
                       theme=main_theme) # decorate this later
customization = menu.add.button('Customize', open_customize)
menu.add.button('PLAY', main_screen)
menu.add.button('Quit', pygame_menu.events.EXIT)

# decorator = customization.get_decorator()
# decorator.add_polygon([(1, 1), (1, 10), (10, 1)], color=(255, 0, 0))

# # If the widget needs a bigger margin
# customization.set_padding((25, 25, 10, 10))

# decorator = menu.get_decorator()
# decorator.add_line((10, 10), (100, 100), color=(45, 180, 34), width=10)


customize_menu = pygame_menu.Menu('Customize', 600, 400,
                       theme=main_theme)
customize_menu.add.button('Customize')

clock = pg.time.Clock()

running = True
while running:
    time_delta = clock.tick(60)/1000
    events = pg.event.get()
    # Causes game to quit when necessary
    for event in events:
      if event.type == pg.QUIT:
          pg.quit()
          quit()
    # Menu appears if it is enabled
    if menu.is_enabled():
      menu.update(events)
      menu.draw(screen)
    pg.display.update()




