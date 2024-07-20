# Import libraries
import pygame as pg
import pygame_menu
import pygame_gui
from pygame.locals import *
import pygame_menu
import time 
import os
import json
from datetime import datetime, timezone
import random
import math
from collections import deque

#Initialize Pygame window
pg.init()

line_width = 3

# Game board dimensions
GRID_HEIGHT = 500
GRID_WIDTH = 500

# ---------------------------------COORDS-----------------------------------------
x_vals = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
y_vals = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

coords = []
counter = 100

# Create coordinate list
for y_counter in range(0,10):
    for i in x_vals:
        coords.append({counter : (i, y_vals[y_counter])})
        counter -= 1

coords.append({0: (550, 500)})

# Getting the colours in a list
colourlist = [('Red', (255, 0, 0)),
          ('Orange', (255, 132, 0)),
          ('Yellow', (255, 213, 0)),
          ('Green', (16, 161, 35)),
          ('Blue', (0, 119, 255)),
          ('Purple', (69, 0, 217)),
          ('Pink', (188, 0, 217))]

# Making the sprites for the players
red = "game_pieces/red.png"
orange = "game_pieces/orange.png"
yellow = "game_pieces/yellow.png"
green = "game_pieces/green.png"
blue = "game_pieces/blue.png"
purple = "game_pieces/purple.png"
pink = "game_pieces/pink.png"
spriteslist = [red, orange, yellow, green, blue, purple, pink]

# Background colours
blackBg = (0, 0, 0)
blue = (51, 102, 255)

# Initialize fonts (different sizes)
pg.font.init()
font = pg.font.Font(None, 20)
fontM = pg.font.Font(None, 40)
fontXL = pg.font.Font(None, 50)

# Screen Setup
screen = pg.display.set_mode((1000, 600))
pg.display.set_caption("Snakes and Ladders")
clock = pg.time.Clock()

# Initialize variables
white = (255, 255, 255)
gride = []
scale_y = (600 - GRID_HEIGHT)/2
scale_x = 50
width = 0
turn = 0
dice_value = 0
winner_name = ""

# Create 10x10 grid gameboard (2D array)
for i in range(10):
    row = [0] * 10
    gride.append(row)


# CREATE NUMBERS ON GAMEBOARD
# Input: None
# Output: Generate numbers on the 10x10 gameboard (1-100)
def create_numbers():
    #Obtain global scale_x and scale_y which is used to create margins
    global scale_x, scale_y
    
    # Counter to increment the x value
    x_pos = 0
    
    # Iterate through various values of x, which will be the ones value of the number
    for x in range(1, 11):
      #Counter to increment to the y value
        y_pos = 0
        # 
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
  width = (x[1] - x[0])/ x_squares

  #Initialize x list
  x_list = []

  #Add the coordinates for the vertical lines to the x list, and draw the line on the screen
  for i in range(x_squares + 1):
    x_coord = x[0] + i * width
    x_list.append(x_coord)
    pg.draw.line(screen, colour, (x_coord, y[0]), (x_coord, y[1]), line_width)

    # Game headings for mainscreen
    gameTitle = "Snakes and Ladders"
    gameTitle_img = fontXL.render(gameTitle, True, blue)
    labelTitle = "Press space to roll a die"
    labelTitle_img = fontM.render(labelTitle, True, white)
    screen.blit(gameTitle_img, (600, 50))
    screen.blit(labelTitle_img, (600, 90))

  #Do the same process for the y-values
  y_list = []
  for i in range(y_squares + 1):
    y_coord = y[0] + i * width
    pg.draw.line(screen, colour, (x[0], y_coord), (x[1], y_coord), line_width)
    y_list.append(y_coord)
  return x_list, y_list, width,


# PLACE GAME PIECES
# Input: Player Entry
# Output: Positions pieces at set coordinates
def place_game_pieces(player_entry):
  global coords, image, turn, playersinfo
  image = pg.image.load(player_entry[1])
  pg.transform.scale(image, (30, 30))
  player_icon = font.render(str(turn + 1), True,  player_entry[3]) # <== playersinfo[turn][3]
  screen.blit(image, coords[100 - player_entry[2]][player_entry[2]])
  screen.blit(player_icon, (coords[100 - player_entry[2]][player_entry[2]][0]+30, coords[100 - player_entry[2]][player_entry[2]][1]))


# MOVE PIECES
# Input: Player entry, and previous value of piece
# Output: Transport game pieces based on dice roll
def transport_piece(player_entry, old_value):
  image = pg.image.load(str(player_entry[1]))
  image.fill((0,0,0, 255))
  
  screen.blit(image, (coords[100 - old_value][old_value][0]+10, coords[100 - old_value][old_value][1]))
  create_grid(screen, 10, 10, x= (scale_x, scale_x + GRID_WIDTH), y = (scale_y, scale_y + GRID_HEIGHT))
  
  place_game_pieces(player_entry)


# BEGIN SNAKES AND LADDERS GAME
# Input: Player information
# Output: None
def snakes_and_ladders(player_entry):
  #obtain global turn pointer, number of players, winner name and end menu
  global turn, number_of_players, winner_name, end_menu
  
  #Get all of events using pygame's function
  for event in pg.event.get():
    #If the user clicks the spacebar
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_SPACE:
        #Get a randomly generated value
        dice = get_dice_value()

        #Get user's current position
        old_value = player_entry[2]

        #Increment by dice value
        player_entry[2] += dice

        #Ensure player has not surpassed the max count of 100
        if player_entry[2] < 100:

          #Call transport piece to blit the piece to a new position
          transport_piece(player_entry, old_value)

          #Check if the player is on a snake's mouth or ladder's beginning
          generate_S_and_L(playersinfo[turn])

          #increment turn
          turn += 1

          #If the turn counter is as much as the number of players, reset to player 1
          if turn == number_of_players:
            turn = 0
          
          #Format Player's name with message
          playerTurnTitle = f"{playersinfo[turn][0]}'s turn"
          nextMessage = "NEXT: "

          #Format next player image and blit 
          nextMessage_img = fontM.render(nextMessage, True, white)
          playerTurnTitle_img = fontM.render(playerTurnTitle, True, playersinfo[turn][3])
          pg.draw.rect(screen, (0,0,0), (600, 500, 520, 50))
          screen.blit(nextMessage_img, (600, 520))
          screen.blit(playerTurnTitle_img, (700, 520))
          
          #Break the loop
          break
        
        #If the player surpasses the max count of 100
        elif player_entry[2] >= 100:
          #Set to the max
          player_entry[2] = 100

          #Obtain winner's name
          winner_name = player_entry[0]

          #Transport piece to the last square
          transport_piece(player_entry, old_value)

          #Check if theres a snake mouth or ladder b
          generate_S_and_L(playersinfo[turn])
          turn += 1
          
          if turn == number_of_players:
            turn = 0

          #Reset other people's scores

          for i in range(number_of_players):
          
                      playersinfo[i][2] = 0

          #Create loop for the end menu
          runny = True
          while runny:
            #Game over menu, with various options
            end_menu = pygame_menu.Menu('Game Over!', 1000, 600,
                                  theme=main_theme)
            end_menu.add.label(f'{str(winner_name)} wins!', font_size=48)
            end_menu.add.button('Play Again', main_screen)
            end_menu.add.button('Customize', end_open_customize)
            end_menu.add.button('Quit', pygame_menu.events.EXIT)
            end_menu.mainloop(screen)
            
            #Update display
            pg.display.update()

            #Quit the program
            for event in pg.event.get():
              if event.type == pg.QUIT:
                  pg.quit()
                  quit()

          break


# ROLL THE DICE
# Input: None
# Output: Dice roll value, dice image and text display
def get_dice_value():
    global dice_value, playersinfo, turn
    
    # generate a random value for the die 
    dice_value = random.randint(1, 6)

    # Display the die image
    die_image = pg.image.load(f'dice/dice-{str(dice_value)}.png')
    die_image = pg.transform.scale(die_image, (100,100))
    screen.blit(die_image, (600, 150))

    # Display dice number in text
    gameStatusTitle = "You rolled a " + str(dice_value)
    gameStatusTitle_img = fontM.render(gameStatusTitle, True, playersinfo[turn][3])
    pg.draw.rect(screen, (0,0,0), (748, 175, 200, 50))
    screen.blit(gameStatusTitle_img, (750, 175))

    # Black rectangles for screen updates
    pg.draw.rect(screen, (0,0,0), (600, 290, 400, 50))
    pg.draw.rect(screen, (0,0,0), (600, 318, 400, 200))

    return dice_value


# DISPLAY USERNAME
# Input: none
# Output: Display names, position on grid, and gamepiece for each player
def display_usernames():
  for i in range(len(playersinfo)):
    username = str(i+1) + ": " + playersinfo[i][0] + ' - ' + str(playersinfo[i][2])
    username_img = fontM.render(username, True, playersinfo[i][3])
    image = pg.image.load(playersinfo[i][1])
    pg.transform.scale(image, (10, 10))
    screen.blit(image, (600, (315 + 25*i)))
    screen.blit(username_img, (650, (318 + 25*i)))


# OPEN CUSTOMIZE FROM MAIN
# Input: none
# Output: Open customize menu from main screen
def open_customize():
  menu._open(customize_menu)


# OPEN CUSTOMIZE FROM END
# Input: none
# Output: Open customize menu from end screen
def end_open_customize():
  end_menu._open(customize_menu)

#Create a copy of the ladders dictionary
ladderslist = [
    [3, 20],
    [11, 28],
    [17, 74],
    [22, 37],
    [49, 67],
    [73, 86],
    [88, 91]
]

# QUICKEST PATH
#Create a function to find the quickest way up
def quickest_way_up(ladders):
  differences = []
  movements = []
  #First find the largest ladder and its index
  for i in range(len(ladders)):
    difference = ladders[i][1] - ladders[i][0]
    differences.append(difference)
  max_index = differences.index(max(differences))

  #Update the player's position to the end of the largest ladder and get a count of the rolls
  pos = ladders[max_index][1]
  rolls = math.ceil(ladders[max_index][0] / 6)

  #Ensure the movements are being kept track of
  for i in range(math.floor(ladders[max_index][0] / 6)):
     movements.append(6)
  movements.append(((ladders[max_index][0] / 6) - math.floor(ladders[max_index][0] / 6)) * 6)

  #Keep checking for if the quickest way can be found up the ladder
  while pos < 100:
    for j in range(len(ladders)):
        if ladders[j][0] > pos:
            #If another ladder is found, increment rolls and the movements list, and go to that position
            newdifference = ladders[j][0] - pos

            for i in range(math.floor(newdifference / 6)):
                movements.append(6)
            movements.append(((newdifference / 6) - math.floor(newdifference / 6)) * 6)

            rolls += math.ceil(newdifference / 6)
            pos = ladders[j][1]
        #If no ladder can be found past the current position, find the number of rolls to get to the end using 6'ss.
        elif j == len(ladders) - 1:
            rolls += math.ceil((100 - pos) / 6)

            for i in range(math.floor((100 - pos) / 6)):
                movements.append(6)
            movements.append((((100 - pos) / 6) - math.floor((100 - pos) / 6)) * 6)
            pos = 100

  #Clean up the movements list
  for i in range(movements.count(0)):
    movements.remove(0)
  for element in movements:
     movements[movements.index(element)] = str(round(element))
  
  #Return the desired contents from the function
  printingmovements = ", ".join(movements)
  returning = "*FYI, the quickest way to win is in " + str(rolls) + " moves! This is done if you roll " + printingmovements + "!"

  #Blit the message to the screen
  returning_img = font.render(returning, True, (255, 102, 204))
  screen.blit(returning_img, (50, 565))

#print(quickest_way_up(ladderslist))


# MAIN SCREEN
# Input: none
# Output: Displays the game and ties the functions together 
def main_screen():
    global scale_x, scale_y, GRID_WIDTH, GRID_HEIGHT, number_of_players, width, turn, playersinfo
    global p1_colour, p2_colour, p3_colour, p4_colour, p5_colour, p6_colour
    bg = (0, 0, 0),
    screen.fill(bg)
    
    # Getting all the player information sorted (name, sprite, initial position, colour)
    playersinfo = []
    playersinfo.append([p1_name, p1avatar, 0, p1_colour])
    playersinfo.append([p2_name, p2avatar, 0, p2_colour])
    playersinfo.append([p3_name, p3avatar, 0, p3_colour])
    playersinfo.append([p4_name, p4avatar, 0, p4_colour])
    playersinfo.append([p5_name, p5avatar, 0, p5_colour])
    playersinfo.append([p6_name, p6avatar, 0, p6_colour])

    playersinfo = playersinfo[: number_of_players]

    # Main Game Loop
    run = True
    while run:
        # Generate full gameboard
        x_list, y_list, width = create_grid(screen, 10, 10, x= (scale_x, scale_x + GRID_WIDTH), y = (scale_y, scale_y + GRID_HEIGHT))
        place_game_pieces(playersinfo[turn])
        snakes_and_ladders(playersinfo[turn])
        create_numbers()
        pg.draw.rect(screen, (0,0,0), (750, 225, 200, 50))

        # Quit game if necessary
        for event in pg.event.get():
          if event.type == pg.QUIT:
              run = False
              pg.QUIT()
        
        # Display snakes, ladders, and usernames
        generate_S_and_L(playersinfo[turn])
        display_usernames()
        quickest_way_up(ladderslist)
        pg.display.update()

# MENU -- Themes, colour, fonts
main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.widget_font = pygame_menu.font.FONT_MUNRO
main_theme.title_font = pygame_menu.font.FONT_NEVIS
main_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
main_theme.title_offset = (5, 1)
main_theme.title_font_color = (23, 101, 179)

# Menu buttons (Start, Quit, customize players)
menu = pygame_menu.Menu('Snakes and Ladders', 1000, 600, theme=main_theme) 
menu.add.image("snakesandladders.png", scale = (0.3, 0.3))
menu.add.button('GET STARTED', open_customize)
menu.add.button('Quit', pygame_menu.events.EXIT)

end_menu = pygame_menu.Menu('Game Over!', 1000, 600,
                      theme=main_theme)

customize_menu = pygame_menu.Menu('Customize', 1000, 600,
                       theme=main_theme)

# Pick number of players (slider)
player_number_options = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6'}
numberofplayerslider = customize_menu.add.range_slider('# of Players', 0, list(player_number_options.keys()),
                      slider_text_value_enabled=False,
                      value_format=lambda x: player_number_options[x])

# Default player colours
p1_colour = (255, 0, 0)
p2_colour = (255, 0, 0)
p3_colour = (255, 0, 0)
p4_colour = (255, 0, 0)
p5_colour = (255, 0, 0)
p6_colour = (255, 0, 0)

# Default player names
p1_name = 'Player 1'
p2_name = 'Player 2'
p3_name = 'Player 3'
p4_name = 'Player 4'
p5_name = 'Player 5'
p6_name = 'Player 6'

# Default player game pieces (sprites)
p1avatar = spriteslist[0]
p2avatar = spriteslist[0]
p3avatar = spriteslist[0]
p4avatar = spriteslist[0]
p5avatar = spriteslist[0]
p6avatar = spriteslist[0]

# Functions to set colour preferences for respective players
def p1_colour_selection(key, value):
  global p1_colour
  global p1avatar
  p1_colour = value
  p1avatar = spriteslist[key[1]]

def p2_colour_selection(key, value):
  global p2_colour
  global p2avatar
  p2_colour = value
  p2avatar = spriteslist[key[1]]
  
def p3_colour_selection(key, value):
  global p3_colour
  global p3avatar
  p3_colour = value
  p3avatar = spriteslist[key[1]]
  
def p4_colour_selection(key, value):
  global p4_colour
  global p4avatar
  p4_colour = value
  p4avatar = spriteslist[key[1]]

def p5_colour_selection(key, value):
  global p5_colour
  global p5avatar
  p5_colour = value
  p5avatar = spriteslist[key[1]]
  
def p6_colour_selection(key, value):
  global p6_colour
  global p6avatar
  p6_colour = value
  p6avatar = spriteslist[key[1]]

# Functions to set names for respective players
def p1_name_selection(value):
  global p1_name
  p1_name = value
  
def p2_name_selection(value):
  global p2_name
  p2_name = value
  
def p3_name_selection(value):
  global p3_name
  p3_name = value
  
def p4_name_selection(value):
  global p4_name
  p4_name = value
  
def p5_name_selection(value):
  global p5_name
  p5_name = value
  
def p6_name_selection(value):
  global p6_name
  p6_name = value

# Slider widgets for respective players
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

#Hide all extra colour selectors until it is chosen in the slider
p3_colour_selector.hide()
p4_colour_selector.hide()
p5_colour_selector.hide()
p6_colour_selector.hide()
p3_name_selector.hide()
p4_name_selector.hide()
p5_name_selector.hide()
p6_name_selector.hide()

number_of_players = 2

# Slider to change # of players
def numberofplayerslider_change(value):
  global number_of_players
  number_of_players = value + 2
  if number_of_players >= 3:
    p3_name_selector.show()    
    p3_colour_selector.show()
  if number_of_players >= 4:
    p4_name_selector.show()
    p4_colour_selector.show()
  if number_of_players >= 5:
    p5_name_selector.show()
    p5_colour_selector.show()
  if number_of_players >= 6:
    p6_name_selector.show()
    p6_colour_selector.show()
  
  if number_of_players < 3:
     p3_name_selector.hide()
     p3_colour_selector.hide()
  if number_of_players < 4:
     p4_name_selector.hide()
     p4_colour_selector.hide()
  if number_of_players < 5:
     p5_name_selector.hide()
     p5_colour_selector.hide()
  if number_of_players < 6:
     p6_name_selector.hide()
     p6_colour_selector.hide()

numberofplayerslider.set_onchange(numberofplayerslider_change)
p1_colour_selector.set_onchange(p1_colour_selection)
p2_colour_selector.set_onchange(p2_colour_selection)
p3_colour_selector.set_onchange(p3_colour_selection)
p4_colour_selector.set_onchange(p4_colour_selection)
p5_colour_selector.set_onchange(p5_colour_selection)
p6_colour_selector.set_onchange(p6_colour_selection)

#Add button to the customize menu
customize_menu.add.button('PLAY', main_screen, font_size=40)


#Initialize clock
clock = pg.time.Clock()
      
# Add a message to the screen for snake hits
def got_snake_bite(player_entry, end_square):
  #Selection of expressions
  snake_bite = [
    "Boohoo ):",
    "Bummer",
    "Snake bite",
    "Oh no",
    "Dang"]
  
  #Format message with random choice, create image and blit it to the screen
  snakemessage = random.choice(snake_bite) + " " + player_entry[0] + f"! You got sent back to square {end_square}."
  snakemessage_img = font.render(snakemessage, True, player_entry[3])
  pg.draw.rect(screen, (0,0,0), (600, 290, 400, 50))
  screen.blit(snakemessage_img, (600, 290))

# Add a message to the screen for ladder hits
def got_ladder_jump(player_entry, end_square):
  #Selection of expressions
  ladder_jump = [
    "Woohoo",
    "Wow",
    "Awesome",
    "No way ",
    "Yaayy"]
  
  #Create ladder message and format it, blit it to the screen
  laddermessage = random.choice(ladder_jump) + " " + player_entry[0] + f"! You got sent to square {end_square}"
  laddermessage_img = font.render(laddermessage, True, player_entry[3])
  pg.draw.rect(screen, (0,0,0), (600, 290, 400, 50))
  screen.blit(laddermessage_img, (600, 290))

# SNAKES AND LADDERS
# Input: Player entry
# Output: Generate snakes and ladders on board
def generate_S_and_L(player_entry):
  
  # ladder takes you up from 'key' to 'value'
  ladders = {
    3: 20,
    11: 28,
    17: 74,
    22: 37,
    49: 67,
    73: 86,
    88: 91
  }
  
  # snake takes you down from 'key' to 'value'
  snakes = {
    18: 1,
    39: 5,
    51: 6,
    54: 36,
    75: 28,
    90: 48,
    92: 25,
  }
 
  # --- SNAKES ---
  for i in snakes.items():
    # Draw snake lines based on coords
    start_pos = (coords[100 - i[0]][i[0]][0]+25, coords[100 - i[0]][i[0]][1]+25)
    end_pos = (coords[100 - i[1]][i[1]][0]+25, coords[100 - i[1]][i[1]][1]+25)
    
    pg.draw.line(screen, (0, 255, 0), start_pos, end_pos, 4)

    # Display each player's current position square
    if str(playersinfo[turn-1][2]) == "0":
      pg.draw.rect(screen, (0,0,0), (750, 225, 200, 50))

    else:
      area_title = "You are now at square " + str(playersinfo[turn-1][2]) + "."
      area_title_img = font.render(area_title, True, playersinfo[turn-1][3])
      pg.draw.rect(screen, (0,0,0), (750, 225, 200, 50))
      screen.blit(area_title_img, (750, 225))

    # Move player piece down the snake
    if player_entry[2] == i[0]:
      player_entry[2] = i[1]
      transport_piece(player_entry, i[0])
      got_snake_bite(player_entry, i[1])

  # --- LADDERS ---
  for i in ladders.items():
    # Draw ladder lines based on coords
    pg.draw.rect(screen, (0,0,0), (750, 225, 200, 50))
    start_pos = (coords[100 - i[0]][i[0]][0]+25, coords[100 - i[0]][i[0]][1]+18)
    end_pos = (coords[100 - i[1]][i[1]][0]+25, coords[100 - i[1]][i[1]][1]+18)
    
    start_pos2 = (coords[100 - i[0]][i[0]][0]+25, coords[100 - i[0]][i[0]][1]+27)
    end_pos2 = (coords[100 - i[1]][i[1]][0]+25, coords[100 - i[1]][i[1]][1]+27)

    pg.draw.line(screen, (252, 232, 3), start_pos, end_pos, 2)
    pg.draw.line(screen, (252, 232, 3), start_pos2, end_pos2, 2)
    
    # Display each player's current position square
    if str(playersinfo[turn-1][2]) == "0":
      pg.draw.rect(screen, (0,0,0), (750, 225, 200, 50))

    else:
      area_title = "You are now at square " + str(playersinfo[turn-1][2]) + "."
      area_title_img = font.render(area_title, True, playersinfo[turn-1][3])
      pg.draw.rect(screen, (0,0,0), (750, 225, 200, 50))
      screen.blit(area_title_img, (750, 225))

    # Move player piece up ladder
    if player_entry[2] == i[0]:
      player_entry[2] = i[1]
      transport_piece(player_entry, i[0])
      got_ladder_jump(player_entry, i[1])

# Game Loop
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




# ------------------------------ RESOURCES ---------------------------------------
# ------------ https://www.geeksforgeeks.org/snake-ladder-problem-2/ -------------
# ------------ https://pygame-menu.readthedocs.io/en/3.5.2/_source/themes.html ---
# ------------ https://www.pygame.org/docs/ --------------------------------------
# --------------------------------------------------------------------------------