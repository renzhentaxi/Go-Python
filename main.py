#----------- Imports ---------------
import pygame
import sys


#---------- Board Setup ------------
game_size = 9 
screen_width = 800
screen_height = 800
BLACK = (0,0,0)
WHITE = (255,255,255)
board_size = screen_height - 200  # to ensure stones on corners are visible
unit_size = int(board_size / game_size)

#---------- PyGame Config -----------
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GO by Taxi")



#coordinates are (x, y)
NINE_BY_NINE = [
                  (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
                  (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
                  (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
                  (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
                  (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
                  (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7),
                  (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)
               ]



class Intersection:
    '''Class that handles creation of the visible board'''
    intersections = []
    def __init__(self, x, y):
        self.intersections.append(self)
        self.x = x
        self.y = y

    def draw_black(self, surface):
        '''draws a black stone'''
        pygame.draw.circle(surface, BLACK,((self.x+1)*unit_size,(self.y+1)*unit_size), int(unit_size/2))

    def draw_white(self, surface):
        '''draws a white circle'''
        pygame.draw.circle(surface, WHITE,((self.x+1)*unit_size,(self.y+1)*unit_size), int(unit_size/2))


#functions
def start():
    '''Commences board creation'''
    Intersection.intersections = []
    
    for x in range(game_size):
        for y in range(game_size):
            Intersection(x, y)  # I don't like this, it returns a list of Instersection type objects. I'd prefer .append() a tuple and work off that. But up to you

    

def draw_board(surface):
  '''Draws intersections for game board'''
  surface.fill((161, 148, 36))  # So white stones are visible, can replace with board img later
  for x in range(1, game_size+1):  # So lines aren't drawn at pos 0 on either x or y coordinates 
    for y in range(1, game_size+1):  # So lines aren't drawn at pos 0 on either x or y coordinates 
      pygame.draw.line(surface, BLACK,(x*unit_size, 65), (x*unit_size, board_size-8), 3) # for border vertical line fixed length issue, added width for visibility
      pygame.draw.line(surface, BLACK,(65, y*unit_size), (board_size-5, y*unit_size), 3) # for border horizontal line fixed length issue added width for visibility
  

  for intxn in Intersection.intersections[:50:3]:  # indices just for demonstration
      intxn.draw_white(surface)

  for intxn in Intersection.intersections[::4]:   # indices just for demonstration
      intxn.draw_black(surface)
  

def mouse_clicked(pos):
    '''Add something to doctstring'''
    a = 4

start()
#loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked(event.pos)
        draw_board(screen)
        pygame.display.flip()
