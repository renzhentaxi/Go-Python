import pygame,sys


gameSize = 9
screenWidth = 800
screenHeight = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
boardSize = screenHeight
unitSize = int(boardSize/gameSize)
#display
pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("GO by Taxi")
#classes
class Intersection:
    intersections = []
    def __init__(self,x,y):
        self.intersections.append(self)
        self.x = x
        self.y = y
    def draw(self,surface):
        pygame.draw.circle(surface,BLACK,((self.x+1)*unitSize,(self.y+1)*unitSize),int(unitSize/2))
#functions
def start():
    #createIntersections
    Intersection.intersections = []
    
    for x in range(gameSize-1):
        for y in range(gameSize-1):
            Intersection(x,y)

def drawBoard(surface):
  surface.fill(WHITE)
  for x in range(gameSize):
    for y in range(gameSize):
      pygame.draw.line(surface,BLACK,(x*unitSize,0),(x*unitSize,boardSize))
      pygame.draw.line(surface,BLACK,(0,y*unitSize),(boardSize,y*unitSize))
  for i in Intersection.intersections:
      i.draw(surface)

def mouseClicked(pos):
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
        drawBoard(screen)
        pygame.display.flip()
