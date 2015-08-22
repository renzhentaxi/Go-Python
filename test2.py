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
board_surface = pygame.Surface((screen_width,screen_height))
board_surface = pygame.Surface((board_size,board_size))
white_surface = pygame.Surface((unit_size,unit_size))
black_surface = pygame.Surface((unit_size,unit_size))
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
	#init stone surface
	rect =white_surface.get_rect()
	pygame.draw.circle(white_surface,WHITE,rect.center,unit_sizeh)
	pygame.draw.circle(black_surface,BLACK,rect.center,unit_sizeh)

def mouse_clicked(event):
	x = event.pos[0]-offsetx-unit_sizeh
	y = event.pos[1]-offsety-unit_sizeh
	x = (x-x%unit_size)/unit_size
	y = (y-y%unit_size)/unit_size
	print(x,y)

def draw():
	screen.fill(WHITE)
	screen.blit(board_surface,(offsetx,offsety))

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