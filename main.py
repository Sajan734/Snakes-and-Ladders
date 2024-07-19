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

def open_end():
  menu._open(end_menu)


main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.widget_font = pygame_menu.font.FONT_MUNRO


menu = pygame_menu.Menu('Snakes and Ladders', 600, 400,
                       theme=main_theme) # decorate this later
customization = menu.add.button('Customize', open_customize)
menu.add.button('PLAY', main_screen)
menu.add.button('END MENU', open_end)
menu.add.button('Quit', pygame_menu.events.EXIT)



customize_menu = pygame_menu.Menu('Customize', 600, 400,
                       theme=main_theme)
customize_menu.add.button('Customize')

end_menu = pygame_menu.Menu('Game Over!', 600, 400,
                       theme=main_theme)
end_menu.add.label(f'{str("winner_username")} wins!', font_size=48)
end_menu.add.button('Leaderboard')
end_menu.add.button('Game Log')
end_menu.add.button('Quit')

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
                