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

GRID_HEIGHT = 500
GRID_WIDTH = 500

#Getting the colours in a list
colourlist = [('Red', (0, 0, 0)),
          ('Orange', (0, 0, 255)),
          ('Yellow', (0, 255, 255)),
          ('Green', (255, 0, 255)),
          ('Blue', (0, 255, 0)),
          ('Purple', (255, 0, 0)),
          ('Pink', (255, 255, 0))]
#Making the sprites for the players
red = "game_pieces/red.png"
orange = "game_pieces/orange.png"
yellow = "game_pieces/yellow.png"
green = "game_pieces/green.png"
blue = "game_pieces/blue.png"
purple = "game_pieces/purple.png"
pink = "game_pieces/pink.png"
spriteslist = [red, orange, yellow, green, blue, purple, pink]

blue = (0, 0, 255)
pg.font.init()
font = pg.font.Font(None, 20)
fontM = pg.font.Font(None, 40)
fontXL = pg.font.Font(None, 50)

screen = pg.display.set_mode((1000, 600))
pg.display.set_caption("Snakes and Ladders")
clock = pg.time.Clock()
    
white = (255, 255, 255)
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


screen = pg.display.set_mode((1000, 600))

def open_customize():
  menu._open(customize_menu)

def main_screen():
    global scale_x, scale_y, GRID_WIDTH, GRID_HEIGHT
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


menu = pygame_menu.Menu('Snakes and Ladders', 1000, 600,
                       theme=main_theme) # decorate this later
menu.add.button('GET STARTED', open_customize)
menu.add.button('Quit', pygame_menu.events.EXIT)

# decorator = customization.get_decorator()
# decorator.add_polygon([(1, 1), (1, 10), (10, 1)], color=(255, 0, 0))

# # If the widget needs a bigger margin
# customization.set_padding((25, 25, 10, 10))

# decorator = menu.get_decorator()
# decorator.add_line((10, 10), (100, 100), color=(45, 180, 34), width=10)

# def numberofplayerfunc():
#    for i in range(customize_menu)

customize_menu = pygame_menu.Menu('Customize', 1000, 600,
                       theme=main_theme)

player_number_options = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6'}
numberofplayerslider = customize_menu.add.range_slider('# of Players', 0, list(player_number_options.keys()),
                      slider_text_value_enabled=False,
                      value_format=lambda x: player_number_options[x])

p1_colour = (0, 0, 0)
p2_colour = (0, 0, 0)
p3_colour = (0, 0, 0)
p4_colour = (0, 0, 0)
p5_colour = (0, 0, 0)
p6_colour = (0, 0, 0)

p1_name = 'p1'
p2_name = 'p2'
p3_name = 'p3'
p4_name = 'p4'
p5_name = 'p5'
p6_name = 'p6'

p1avatar = spriteslist[0]
p2avatar = spriteslist[0]
p3avatar = spriteslist[0]
p4avatar = spriteslist[0]
p5avatar = spriteslist[0]
p6avatar = spriteslist[0]

def p1_colour_selection(key, value):
  global p1_colour
  global p1avatar
  p1_colour = key
  p1avatar = spriteslist[key[1]]
  print(p1_colour)
def p2_colour_selection(key, value):
  global p2_colour
  global p2avatar
  p2_colour = key
  p2avatar = spriteslist[key[1]]
  print(p2_colour)
def p3_colour_selection(key, value):
  global p3_colour
  global p3avatar
  p3_colour = key
  p3avatar = spriteslist[key[1]]
  print(p3_colour)
def p4_colour_selection(key, value):
  global p4_colour
  global p4avatar
  p4_colour = key
  p4avatar = spriteslist[key[1]]
  print(p4_colour)
def p5_colour_selection(key, value):
  global p5_colour
  global p5avatar
  p5_colour = key
  p5avatar = spriteslist[key[1]]
  print(p5_colour)
def p6_colour_selection(key, value):
  global p6_colour
  global p6avatar
  p6_colour = key
  p6avatar = spriteslist[key[1]]
  print(p6_colour)

def p1_name_selection(value):
  global p1_name
  p1_name = value
  print(p1_name)
def p2_name_selection(value):
  global p2_name
  p2_name = value
  print(p2_name)
def p3_name_selection(value):
  global p3_name
  p3_name = value
  print(p3_name)
def p4_name_selection(value):
  global p4_name
  p4_name = value
  print(p4_name)
def p5_name_selection(value):
  global p5_name
  p5_name = value
  print(p5_name)
def p6_name_selection(value):
  global p6_name
  p6_name = value
  print(p6_name)

#Getting all the player information sorted
playersinfo = []
playersinfo.append([p1_name, p1avatar])
playersinfo.append([p2_name, p2avatar])
playersinfo.append([p3_name, p3avatar])
playersinfo.append([p4_name, p4avatar])
playersinfo.append([p5_name, p5avatar])
playersinfo.append([p6_name, p6avatar])

# ******** WE NEED TO CHANGE THE RGB VALUES BELOW; THEY'RE RANDOM FOR NOW**********
p1_name_selector = customize_menu.add.text_input('Player 1: ', default='<EDIT>', onchange=p1_name_selection, maxchar=10)
p1_colour_selector = customize_menu.add.dropselect(
    title='Player 1',
    items= colourlist,
    placeholder='Scroll to see colours'
)

p2_name_selector = customize_menu.add.text_input('Player 2: ', default='<EDIT>', onchange=p2_name_selection, maxchar=10)
p2_colour_selector = customize_menu.add.dropselect(
    title='Player 2',
    items= colourlist,
    placeholder='Scroll to see colours'
)

p3_name_selector = customize_menu.add.text_input('Player 3: ', default='<EDIT>', onchange=p3_name_selection, maxchar=10)
p3_colour_selector = customize_menu.add.dropselect(
    title='Player 3',
    items= colourlist,
    placeholder='Scroll to see colours'
)

p4_name_selector = customize_menu.add.text_input('Player 4: ', default='<EDIT>', onchange=p4_name_selection, maxchar=10)
p4_colour_selector = customize_menu.add.dropselect(
    title='Player 4',
    items= colourlist,
    placeholder='Scroll to see colours',
)

p5_name_selector = customize_menu.add.text_input('Player 5: ', default='<EDIT>', onchange=p5_name_selection, maxchar=10)
p5_colour_selector = customize_menu.add.dropselect(
    title='Player 5',
    items= colourlist,
    placeholder='Scroll to see colours',
)

p6_name_selector = customize_menu.add.text_input('Player 6: ', default='<EDIT>', onchange=p6_name_selection, maxchar=10)
p6_colour_selector = customize_menu.add.dropselect(
    title='Player 6',
    items= colourlist,
    placeholder='Scroll to see colours'
)



p3_colour_selector.hide()
p4_colour_selector.hide()
p5_colour_selector.hide()
p6_colour_selector.hide()
p3_name_selector.hide()
p4_name_selector.hide()
p5_name_selector.hide()
p6_name_selector.hide()


number_of_players = 2
def numberofplayerslider_change(value):
  global number_of_players
  number_of_players = value + 2
  if number_of_players == 3:
    p3_name_selector.show()    
    p3_colour_selector.show()
  elif number_of_players == 4:
    p4_name_selector.show()
    p4_colour_selector.show()
  elif number_of_players == 5:
    p5_name_selector.show()
    p5_colour_selector.show()
  elif number_of_players == 6:
    p6_name_selector.show()
    p6_colour_selector.show()
  
  if number_of_players < 3:
     p3_name_selector.hide()
     p3_colour_selector.hide()
  elif number_of_players < 4:
     p4_name_selector.hide()
     p4_colour_selector.hide()
  elif number_of_players < 5:
     p5_name_selector.hide()
     p5_colour_selector.hide()
  elif number_of_players < 6:
     p6_name_selector.hide()
     p6_colour_selector.hide()

numberofplayerslider.set_onchange(numberofplayerslider_change)
p1_colour_selector.set_onchange(p1_colour_selection)
p2_colour_selector.set_onchange(p2_colour_selection)
p3_colour_selector.set_onchange(p3_colour_selection)
p4_colour_selector.set_onchange(p4_colour_selection)
p5_colour_selector.set_onchange(p5_colour_selection)
p6_colour_selector.set_onchange(p6_colour_selection)

customize_menu.add.button('PLAY', main_screen, font_size=40)

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

