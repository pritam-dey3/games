import pygame

width = 800
height = 600

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
bg_color = (239, 228, 176)


m,n = (4,4)
board_h, board_w = 400, 400
circle_radius = 5

#player details
players = {0:["P", 0, (0, 162, 232), (152, 192, 252)],
			1:["S", 0, (250, 79, 5), (252,156,116)]}
p1_color = (0, 162, 232)
p2_color = (250, 79, 5)

pygame.init()
clock = pygame.time.Clock()

def initiate():
	global screen, clock, stick_length
	screen = pygame.display.set_mode((width,height))
	pygame.display.set_caption("dot-box")

	screen.fill(WHITE)
	pygame.draw.rect(screen, bg_color,((width - board_w)/2, (height - board_h)/2, board_w, board_h))

	#necessary calculations
	start_x = (width - board_w)/2 + circle_radius
	start_y = (height - board_h)/2 + circle_radius
	stick_length = (board_w - 2*n*circle_radius) / (n - 1)
	# step_right = (board_w - 2*circle_radius) / (n - 1)
	# step_down = (board_h - 2*circle_radius) / (m - 1)

	for j in range(m):
		for i in range(n):
			pos_x = int(start_x + (stick_length + 2*circle_radius)*i)
			pos_y = int(start_y + (stick_length + 2*circle_radius)*j)
			pygame.draw.circle(screen, BLACK, (pos_x, pos_y), circle_radius)

	pygame.display.update()

def create_boxes():
	global box_mat
	box_mat = [[box((j,i)) for i in range(n-1)] for j in range(m-1)]
	# print(box_mat)
	# for j in range(m-1):
	# 	for i in range(n-1):
	# 		box_mat[j][i].win(str(j)+str(i))

def draw_sticks():
	global sticks
	sticks = {}
	for j in range(m-1):
		for i in range(n-1):
			try:
				sticks["0"+str(j)+str(i)].r = box_mat[j][i]
			except KeyError:
				sticks["0"+str(j)+str(i)] = stick((box_mat[j][i].x, box_mat[j][i].y - circle_radius*2), True)
				sticks["0"+str(j)+str(i)].r = box_mat[j][i]

			try:
				sticks["0"+str(j+1)+str(i)].l = box_mat[j][i]
			except KeyError:
				sticks["0"+str(j+1)+str(i)] = stick((box_mat[j][i].x, box_mat[j][i].y + stick_length), True)
				sticks["0"+str(j+1)+str(i)].l = box_mat[j][i]

			try:
				sticks["1"+str(j)+str(i)].l = box_mat[j][i]
			except KeyError:
				sticks["1"+str(j)+str(i)] = stick((box_mat[j][i].x - circle_radius*2, box_mat[j][i].y), False)
				sticks["1"+str(j)+str(i)].l = box_mat[j][i]

			try:
				sticks["1"+str(j)+str(i+1)].r = box_mat[j][i]
			except KeyError:
				sticks["1"+str(j)+str(i+1)] = stick((box_mat[j][i].x + stick_length, box_mat[j][i].y), False)
				sticks["1"+str(j)+str(i+1)].r = box_mat[j][i]

	pygame.display.update()

def switch_player(player, forward = True):
	if forward:
		return ((player+1) % 2)
	else:
		return ((player-1) % 2)

def result():
	if players[0][1] > players[1][1]:
		winner = 0
	elif players[0][1] < players[1][1]:
		winner =1
	else:
		winner = 0

	text = text = players[winner][0] + " won.  "
	score = str(players[winner][1]) + "  ---  " + str(players[switch_player(winner)][1])

	font = pygame.font.SysFont(None, 40)
	textSurf = font.render(text+score, True, BLACK)
	textRect = textSurf.get_rect()
	textRect.left, textRect.bottom = (int(width/2), textRect.height)
	screen.blit(textSurf, textRect)
	pygame.display.update()



class box:
	def __init__(self, index):
		self.index = index
		self.score = 0
		self.x = (width - board_w)/2 + 2*circle_radius + (stick_length + 2*circle_radius)*self.index[1]
		self.y = (height - board_h)/2 + 2*circle_radius + (stick_length + 2*circle_radius)*self.index[0]
	def update_score(self, player):
		self.score += 1
		if(self.score == 4):
			players[player][1] += 1

			font = pygame.font.SysFont(None, int(stick_length/1.5))
			textSurf = font.render(players[player][0], True, players[player][2])
			textRect = textSurf.get_rect()
			textRect.center = (int(self.x + stick_length/2), int(self.y + stick_length/2))
			screen.blit(textSurf, textRect)
			pygame.display.update()
			return True
		return False
	def reduce_score(self,player):
		self.score -= 1
		if(self.score == 3):
			players[player][1] -= 1
			r = pygame.draw.rect(screen, bg_color, (self.x, self.y, stick_length, stick_length))
			pygame.display.update(r)
			return True
		return False

class stick:
	def __init__(self, pos, row):
		self.r = None
		self.l = None
		self.surf = None
		self.rect = None
		if(row):
			self.surf = pygame.Surface((stick_length, circle_radius*2))
			#self.surf.fill(p1_color)
		else:
			self.surf = pygame.Surface((circle_radius*2, stick_length))
			#self.surf.fill(p2_color)
		# self.surf = pygame.Surface.convert_alpha(self.surf)
		self.rect = self.surf.get_rect()
		self.rect.left, self.rect.top = pos[0], pos[1]
		screen.blit(self.surf, self.rect)
	def draw(self, player):
		self.surf.fill(players[player][2])
		bonus_l = False
		bonus_r = False
		if (self.r != None):
			bonus_r = self.r.update_score(player)
		if (self.l != None):
			bonus_l = self.l.update_score(player)
		if(bonus_l or bonus_r):
			return (player - 1)
		else:
			return player
	def undo(self, player):
		self.surf.fill(bg_color)
		screen.blit(self.surf, self.rect)
		pygame.display.update(self.rect)
		bonus_l = False
		bonus_r = False
		if (self.r != None):
			bonus_r = self.r.reduce_score(player)
		if (self.l != None):
			bonus_l = self.l.reduce_score(player)
		if(bonus_l or bonus_r):
			return (player + 1)
		else:
			return player


def gameloop():
	initiate()
	create_boxes()
	draw_sticks()
	player = 0
	undo_list = []
	global sticks

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
				try:
					undo = undo_list.pop()
				except IndexError:
					print("empty board")
					break
				player = undo[1].undo(player)
				sticks[undo[0]] = undo[1]
				player = switch_player(player, False)
		for key,stick in sticks.copy().items():
			if stick.rect.collidepoint(pygame.mouse.get_pos()):
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					player = stick.draw(player)
					player = switch_player(player)
					undo_list.append((key, sticks.pop(key)))
				else:
					stick.surf.fill(players[player][3])
			else:
				stick.surf.fill(bg_color)
			screen.blit(stick.surf, stick.rect)
			pygame.display.update(stick.rect)
		if len(sticks) == 0:
			break
	result()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				pygame.display.quit()
				return 0


while True:
	# try:
	# 	text = input("enter dimension: ")
	# 	m, n = int(text[0]), int(text[2])
	# except:
	# 	m,n = (4,4)

	# players[0][0] = input("Player-1 signature: ")[0]
	# players[1][0] = input("Player-2 signature: ")[0]
	gameloop()