#----------- Imports ------------------------------

import pygame
import sys


#---------- Board Setup ---------------------------


game_size = 9 
screen_width = 800
screen_height = 800
BLACK = (0,0,0)
WHITE = (255,255,255)
board_size = screen_height - 200  # to ensure stones on corners are visible
unit_size = int(board_size / game_size)


#---------- PyGame Config -------------------------


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GO by Taxi")



#--------- Board & Pieces Functions ---------------


def make_board_tuple(num):
    '''Makes a list of tuples to range num exclusive. of form (x,y)
    eg) [
          (0, 0), (1, 0), (2, 0),
          (1, 0), (1, 1), (2, 1),
          (2, 0), (2, 1), (2, 2)
        ]
    '''
    return [(j, i) for i in range(num) for j in range(num)]

def draw_board(surface):
    '''Draws intersections for game board'''
    surface.fill((161, 148, 36))  # So white stones are visible, can replace with board img later
    for x in range(1, game_size+1):  # So lines aren't drawn at pos 0 on either x or y coordinates 
      for y in range(1, game_size+1):  # So lines aren't drawn at pos 0 on either x or y coordinates 
        pygame.draw.line(surface, BLACK,(x*unit_size, 65), (x*unit_size, board_size-8), 3) # for border vertical line fixed length issue, added width for visibility
        pygame.draw.line(surface, BLACK,(65, y*unit_size), (board_size-5, y*unit_size), 3) # for border horizontal line fixed length issue added width for visibility

def draw_black(surface, x, y):
    '''draws a black stone'''
    pygame.draw.circle(surface, BLACK,((x+1)*unit_size,(y+1)*unit_size), int(unit_size/2))

def draw_white(surface, x, y):
    '''draws a white circle'''
    pygame.draw.circle(surface, WHITE,((x+1)*unit_size,(y+1)*unit_size), int(unit_size/2))


#---------------- Game Functions -------------------

board_tuples = make_board_tuple(9)

empty_dict = {
                "empty": board_tuples
             }

white_dict = {
                "white": []
             }

black_dict = {
                "black": []
             }

white_kills = 0
black_kills = 0

def add_coordinate(dictionary, key, coor):
    '''Adds tuple coordinate to dictionary'''
    if str(key) != "empty":  # If we're not adding an empty coordinate like after atari 
        empty_dict['empty'].remove(coor)
    dictionary[str(key)].append(coor)


def remove_coordinate(dictionary, key, coor):
    '''Removes coordinate argument from dictionary'''
    global white_kills
    global black_kills
    if key == 'black':
        white_kills += 1
    elif key == 'white':
        black_kills += 1
    else: 
        pass
    dictionary[str(key)].remove(coor)



#check if move valid
#like def count_score (+= kill_count)
#def komi_count
#def atari_check
#def ko_check


#---------- Event Handling Functions ---------------


def mouse_clicked(pos):
    '''Add something to doctstring'''
    a = 4



#Should go under Game Functions section
def game_loop():
    '''Infinite game loop until broken'''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked(event.pos)
            pygame.display.flip()


#------------------ Tests -------------------------  # Delete before release  

# Fill with some tests to make sure everything is working

#black pieces, should only be at (3, 5) and (0, 1)
add_coordinate(black_dict, 'black', (3, 5))
add_coordinate(black_dict, 'black', (8, 8))
add_coordinate(black_dict, 'black', (0, 1))
remove_coordinate(black_dict, 'black', (8, 8))
print("Total white kills: {}".format(white_kills))  # should be one, only one removed


#white pieces, should only be at (3, 6), (3, 4), (2, 5), and (4, 5)
add_coordinate(white_dict, 'white', (3, 6))
add_coordinate(white_dict, 'white', (3, 4))
add_coordinate(white_dict, 'white', (2, 5))
add_coordinate(white_dict, 'white', (4, 5))
add_coordinate(white_dict, 'white', (7, 7))
add_coordinate(white_dict, 'white', (7, 6))
remove_coordinate(white_dict, 'white', (7, 7))
remove_coordinate(white_dict, 'white', (7, 6))
print("Total black kills: {}".format(black_kills))  # Should be 2 since white got removed twice


#Atari and random black piece scenario
draw_board(screen)

for val in black_dict.values():
    for tupl in val:
        draw_black(screen, tupl[0], tupl[1])

for val in white_dict.values():
    for tupl in val:
        draw_white(screen, tupl[0], tupl[1])


#---------------- Running Game --------------------


if __name__ == '__main__':
    game_loop()