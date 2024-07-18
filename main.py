import pygame as pg
import pygame_menu
import pygame_gui
from pygame.locals import *
import pygame_menu
import time 
import os
import json
from datetime import datetime, timezone

clock = pg.time.Clock()
gride = []
scale_y = (600 - GRID_HEIGHT)/2
scale_x = (1000 - GRID_WIDTH)/2


def create_grid_():
    global scale_y, scale_x
    bg = (150, 255, 255)
    grid = (50, 50, 50)
    screen.fill(bg)

    for x in range(0, 11):
        pg.draw.line(screen, grid, (0 + scale_x, x * 50 + scale_y ), (GRID_WIDTH + scale_x, x * 50 + scale_y), line_width)
        pg.draw.line(screen, grid, (x * 50 + scale_x, 0 + scale_y), (x * 50 + scale_x, GRID_HEIGHT + scale_y), line_width)

for i in range(10):
    row = [0] * 10
    gride.append(row)

def create_numbers():
    global scale_x, scale_y
    x_pos = 0
    for x in range(1, 11):
        y_pos = 0
        if y_pos % 2 == 0:
            for y in range(1, 11):
                number = (y-1)* 10 + (x-1)
                num_text = str(100 - number)
                num_img = font.render(num_text, True, white)
                screen.blit(num_img, (x_pos * 50 + 12 + scale_x, y_pos * 50 + 12 + scale_y))
                y_pos += 1
            x_pos += 1
            
        else:
            for y in range(10, 0, -1):
                number = (y-1)* 10 + (x-1) + 11
                num_text = str(100 - number)
                num_img = font.render(num_text, True, white)
                screen.blit(num_img, (x_pos * 50 + 12 + scale_x, y_pos * 50 + 12 + scale_y))
                y_pos += 1
            x_pos += 1

#A function that generates a grid based on the start and end coordinates, number of squares
# Inputs: Screen, number of squares in the x and y directions, colour, start and end coordinates in the x and y directions
# Outputs: list of x_coordinates, list of y_coordinates, width and height of boxes
def create_grid(screen, x_squares, y_squares, colour = (255, 255, 255), x = (50, 350), y = (100, 400)):
  #Calculate width of each box
  x_width = (x[1] - x[0])/ x_squares
  #Initialize x list
  x_list = []
  #Add the coordinates for the vertical lines to the x list, and draw the line on the screen
  for i in range(x_squares + 1):
    x_coord = x[0] + i * x_width
    x_list.append(x_coord)
    pg.draw.line(screen, colour, (x_coord, y[0]), (x_coord, y[1]), line_width)

  #Do the same process for the y-values
  y_width = (y[1] -y[0])/ y_squares
  y_list = []
  for i in range(y_squares + 1):
    y_coord = y[0] + i * y_width
    pg.draw.line(screen, colour, (x[0], y_coord), (x[1], y_coord), line_width)
    y_list.append(y_coord)
  
  return x_list, y_list, x_width, y_width


screen = pg.display.set_mode((600, 400))

def open_customize():
  menu._open(customize_menu)

def main_screen():
    run = True
    screen = pg.display.set_mode((1000, 600))
    while run:
        x_list, y_list, x_width, y_width = create_grid(screen, 10, 10, x= (scale_x, scale_x + GRID_WIDTH), y = (scale_y, scale_y + GRID_HEIGHT))
        create_numbers()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.QUIT()

        pg.display.update()


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

#Initialize Pygame window
pg.init()

line_width = 3

GRID_HEIGHT = 500
GRID_WIDTH = 1000

blue = (0, 0, 255)
pg.font.init()
font = pg.font.Font(None, 20)
fontM = pg.font.Font(None, 40)
fontXL = pg.font.Font(None, 50)

screen = pg.display.set_mode((1000, 600))
pg.display.set_caption("Snakes and Ladders")
clock = pg.time.Clock()
    
run = True
while run:
    create_grid(0, 0, 500)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.QUIT
                