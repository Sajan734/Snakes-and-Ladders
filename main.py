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

line_width = 3
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

blue = (0, 0, 255)
white = (255, 255, 255)

pg.font.init()
font = pg.font.Font(None, 27)
fontM = pg.font.Font(None, 40)
fontXL = pg.font.Font(None, 50)

screen = pg.display.set_mode((1000, 600))
pg.display.set_caption("Snakes and Ladders")


clock = pg.time.Clock()
gride = []
scale_y = (600 - SCREEN_HEIGHT)/2
scale_x = (1000 - SCREEN_WIDTH)/2


def create_grid_():
    global scale_y, scale_x
    bg = (150, 255, 255)
    grid = (50, 50, 50)
    screen.fill(bg)

    for x in range(0, 11):
        pg.draw.line(screen, grid, (0 + scale_x, x * 50 + scale_y ), (SCREEN_WIDTH + scale_x, x * 50 + scale_y), line_width)
        pg.draw.line(screen, grid, (x * 50 + scale_x, 0 + scale_y), (x * 50 + scale_x, SCREEN_HEIGHT + scale_y), line_width)

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

run = True
while run:
    x_list, y_list, x_width, y_width = create_grid(screen, 10, 10, x= (scale_x, scale_x + SCREEN_WIDTH), y = (scale_y, scale_y + SCREEN_HEIGHT))
    
    create_numbers()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.QUIT

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
                