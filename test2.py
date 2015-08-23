#----------Imports-------------------------------

import pygame
import sys
#---------Board setup---------------------------

BLACK = (0,0,0)
WHITE = (255,255,255)
board_color = (161, 148, 36)

game_size = 10 
screen_width = 800
screen_height = 800
board_size = screen_height - 100  
unit_size = int(board_size /game_size)
unit_sizeh = int(unit_size/2)
offsetx = (screen_width-board_size)/2
offsety = (screen_height-board_size)/2
board_surface = pygame.Surface((board_size, board_size))


#--------------pygame config---------------------------

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("GO by Taxi and Dor")

def draw_init():
	#init board surface
	board_surface.fill(board_color)

	for x in range(1,game_size):
		for y in range(1,game_size):
			pygame.draw.line(board_surface,BLACK,(x*unit_size,unit_size),(x*unit_size,unit_size*9),3)
			pygame.draw.line(board_surface,BLACK,(unit_size,y*unit_size),(unit_size*9,y*unit_size),3)

def mouse_clicked(event):
	#print(event.pos)
	#print(grid2pos(pos2grid(event.pos)))
	print(grid2pos((0,0)))
def pos2grid(pos):
	x = pos[0]-offsetx-unit_sizeh
	y = pos[1]-offsety-unit_sizeh
	x = (x-x%unit_size)/unit_size
	y = (y-y%unit_size)/unit_size
	return (x,y)
def grid2pos(grid):
	x = (grid[0]*unit_size)+offsetx+unit_size
	y = grid[1]*unit_size+offsety+unit_size

	return (x,y)
def draw():
	screen.fill(WHITE)
	screen.blit(board_surface,(offsetx,offsety))
	for val in black_dict.values():
	    for tupl in val:
	        draw_stone(screen, tupl[0], tupl[1],BLACK)

	for val in white_dict.values():
	    for tupl in val:
	        draw_stone(screen, tupl[0], tupl[1],WHITE)

def make_board_tuple(num):
    '''Makes a list of tuples to range num exclusive. of form (x,y)
    eg) [
          (0, 0), (1, 0), (2, 0),
          (1, 0), (1, 1), (2, 1),
          (2, 0), (2, 1), (2, 2)
        ]
    '''
    return [(j, i) for i in range(num) for j in range(num)]

def draw_stone(surface, x, y,color):
    '''draws a black stone'''
    x,y=grid2pos((x,y))
    pygame.draw.circle(surface, color, (x, y), unit_sizeh)



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

def add_stone(dictionary, key, coor):
    '''Adds tuple stone to dictionary'''
    if str(key) != "empty":  # If we're not adding an empty stone like after atari 
        empty_dict['empty'].remove(coor)
    dictionary[str(key)].append(coor)


def remove_stone(dictionary, key, coor):
    '''Removes stone argument from dictionary'''
    global white_kills
    global black_kills
    if key == 'black':
        white_kills += 1
    elif key == 'white':
        black_kills += 1
    else: 
        pass
    dictionary[str(key)].remove(coor)

# Fill with some tests to make sure everything is working

#black pieces, should only be at (3, 5) and (0, 1)
add_stone(black_dict, 'black', (3, 5))
add_stone(black_dict, 'black', (8, 8))
add_stone(black_dict, 'black', (0, 0))
remove_stone(black_dict, 'black', (8, 8))
print("Total white kills: {}".format(white_kills))  # should be one, only one removed


#white pieces, should only be at (3, 6), (3, 4), (2, 5), and (4, 5)
add_stone(white_dict, 'white', (3, 6))
add_stone(white_dict, 'white', (3, 4))
add_stone(white_dict, 'white', (2, 5))
add_stone(white_dict, 'white', (4, 5))
add_stone(white_dict, 'white', (7, 7))
add_stone(white_dict, 'white', (7, 6))
remove_stone(white_dict, 'white', (7, 7))
remove_stone(white_dict, 'white', (7, 6))
print("Total black kills: {}".format(black_kills))  # Should be 2 since white got removed twice


def game_loop():
	draw_init()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_clicked(event)
			draw()
		pygame.display.flip()
if __name__ == '__main__':
	game_loop()