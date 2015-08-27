import pygame
import sys
# standard colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
# theme colors
c_board = (161,148,36)
# size related settings
game_size      = 9
screen_width   = 800
screen_height  = 600

board_side_raw = screen_height-100
board_size     = game_size -1
unit_size      = int(board_side_raw/board_size)
unit_sizeh    = int(unit_size/2)
board_side     = unit_size * board_size 
board_offset   = (int(screen_width-board_side)/2,int(screen_height-board_side)/2)
#surface declaration
board_surface = pygame.Surface((board_side,board_side))
board_rect    = board_surface.get_rect()
board_rect.topleft = board_offset
white_surface = pygame.Surface((unit_size,unit_size))
black_surface = pygame.Surface((unit_size,unit_size))
#pygame init
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("GO by Taxi and Dor")
#game init
stone_List = {}
turn = -1 
used_pass = False
group_list = []
ko_prev = None
last_stone = None
game_over = False
white_score = 0
black_score = 0
################################draw function########################
def draw_init():
	board_surface.fill(c_board)
	for i in range(1,board_size):
		pygame.draw.line(board_surface,BLACK,(0,i*unit_size),(board_side,i*unit_size),3)
		pygame.draw.line(board_surface,BLACK,(i*unit_size,0),(i*unit_size,board_side),3)
	white_surface.fill(BLUE)
	white_surface.set_colorkey(BLUE)
	pygame.draw.circle(white_surface,WHITE,(unit_sizeh,unit_sizeh),unit_sizeh)
	black_surface.fill(BLUE)
	black_surface.set_colorkey(BLUE)
	pygame.draw.circle(black_surface,BLACK,(unit_sizeh,unit_sizeh),unit_sizeh)
def draw():
	screen.fill(c_board)
	#draw board
	screen.blit(board_surface,board_rect)
	pygame.draw.rect(screen,BLACK,board_rect,3)
	for stone in stone_List.items():
		if stone[1] == 1:
			screen.blit(white_surface,index2pos(stone[0]))
		elif stone[1] == -1:
			screen.blit(black_surface,index2pos(stone[0]))
####################### unitility #########################
def pos2index(pos):
	result = [0,0]
	for i in range(2):
		result[i] = pos[i] - board_offset[i]+unit_sizeh
		result[i] = int((result[i] - result[i] % unit_size)/unit_size)
	return tuple(result)
def index2pos(index):
	result = [0,0]
	for i in range(2):
		result[i] = index[i]*unit_size+board_offset[i]-unit_sizeh
	return tuple(result)
def index_legal(index):
	for i in index:
		if i> board_size or i<0:
			return False
	return index not in stone_List
############### go logic functions ###########################
def try_capture(index):
	for g in group_list:
		lib = liberties_group(g)
		if len(lib) == 1 and lib[0] == index and stone_List[g[0]] != turn:
			if not ko_rule(g,index):
				remove_group(g)
	return not sucide(index)
def sucide(index):
	if len(liberties(index)+friendly_raw(index,turn)) >0:
		return False
	print("suicidal move detected!!!")
	return True
def ko_rule(group,index):
	global ko_prev, last_stone
	if len(group) == 1:
		if group[0] == last_stone and index == ko_prev:
			print("Ko move detected!!!")
			return True
		last_stone = index
		ko_prev = group[0]
	else:
		ko_prev = None
		last_stone = None
	return False
def score():
	global white_score,black_score,game_over
	if len(stone_List)> 0:
		white_territory,black_territory = count_territory()
		white_score+= white_territory
		black_score+=black_territory
	print("Game has ended")
	print("White score: ",white_score)
	print("Black score: ",black_score)
	game_over = True

########################logic - help function#######################################
def group():
	global group_list
	group_list = []
	stone_queue = list(stone_List)
	while len(stone_queue) > 0:
		stone = stone_queue.pop()
		group = []
		friendly_queue = []
		group.append(stone)
		friendly_queue += friendly(stone)
		while len(friendly_queue) > 0:
			friend = friendly_queue.pop()
			group.append(friend)
			stone_queue.remove(friend)
			friend_of_friends = friendly(friend)
			for f in friend_of_friends:
				if f not in group and f not in friendly_queue:
					friendly_queue.append(f)
		group_list.append(group)
def friendly(index):	
	return friendly_raw(index,stone_List[index])
def friendly_raw2(index,color,stone_List):
	neigh = neighbors(index)
	result = []
	for n in neigh:
		if n in stone_List:
			if stone_List[n] == color:
				result.append(n)
	return result
def friendly_raw(index,color):
	return friendly_raw2(index,color,stone_List)
def liberties(index):
	neigh = neighbors(index)
	result = []
	for n in neigh:
		if n not in stone_List:
			result.append(n)
	return result
def liberties_group(group):
	result = []
	for stone in group:
		temp = liberties(stone)
		for l in temp:
			if l not in result:
				result.append(l)
	return result
def neighbors(index):
	up 	  = index[0],index[1]-1
	down  = index[0],index[1]+1
	left  = index[0]-1,index[1]
	right = index[0]+1,index[1]
	temp  = (up,down,left,right)
	result = []
	for t in temp:
		if (t[0] <= board_size and t[0] >= 0) and (t[1] <= board_size and t[1] >= 0):
			result.append(t)
	return result
			
def count_territory():
	empty = list((x,y) for x in range(game_size) for y in range(game_size))
	terr = {}
	for t in empty:
		if t not in stone_List.keys():
			terr[t] = None
	for stone in stone_List:
		stone_liberties = liberties(stone)
		if stone_List[stone] == 1:
			for sl in stone_liberties:
				terr[sl] = 1 if terr[sl] != -1 else 0
		else:
			for sl in stone_liberties:
				terr[sl] =-1 if terr[sl] != 1 else 0
	runAtLeastOnce = True
	runoneMoreTime = True
	while runoneMoreTime:
		while get_count(terr,None) > 0 or runAtLeastOnce:
			terr_step(terr)
			runAtLeastOnce = False
		terr_step(terr)
		runoneMoreTime = False

	
	return get_count(terr,1),get_count(terr,-1)
def terr_step(terr):
	for t in terr:
			t_color = terr[t]
			t_liber = liberties(t)
			t_colors = get_colors(terr,t_liber)
			t_colors_count = len(t_colors)
			if   t_colors_count >  1:
				terr[t] = 0
			elif t_colors_count == 1:
				if t_color == None:
					terr[t] = t_colors[0]
				elif t_color == 0:
					change_color(terr,t_liber,0)
				elif t_color != t_colors[0]:
					change_color(terr,t_liber+[t],0)
			elif t_colors_count == 0:
				change_color(terr,t_liber,t_color)
def get_count(terr,color):
	result = 0
	for t in terr.values():
		if t == color:
			result+=1
	return result
def get_colors(terr,liber):
	result = []
	for l in liber:
		if terr[l] != None and terr[l] not in result:
			result.append(terr[l])
	return result
def change_color(terr,liber,color):
	for l in liber:
		terr[l] = color
################# stone placement/removal ####################
def add_stone(index,color):
	stone_List[index] = color
def add_group(group,color):
	for stone in group:
		add_group(stone,color)
def del_stone(index):
	del stone_List[index]
def remove_group(group):
	global black_score,white_score
	if stone_List[group[0]] == 1:
		black_score += len(group)
	else:
		white_score +=len(group)
	for stone in group:
		del_stone(stone)
	
#########################event handling ###############################
def on_mouse_click(event):
	global turn,used_pass
	if not game_over:
		if event.button == 1:
			index = pos2index(event.pos)
			if index_legal(index):
				if try_capture(index):
					add_stone(index,turn)
					group()
					used_pass = False
					turn *= -1
		elif event.button == 3:
			if used_pass:
				score()
			used_pass = True
			turn *= -1
def newGame():
	global game_over,used_pass,turn
	turn = -1
	game_over = False
	stone_List.clear()
	used_pass = False

##################debug#########################################

################################game loop
def game_loop():
	draw_init()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				on_mouse_click(event)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					newGame()
			draw()
		pygame.display.flip()
if __name__ == '__main__':
	game_loop()
