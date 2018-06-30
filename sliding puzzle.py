import pygame
from random import shuffle, randrange

width = 800
height = 600

board_dimension = 400
grid = None
border = 10

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
bg_color = (239, 228, 176)
tab_color = (255, 127, 39)
font_color = (163, 73, 164)


pygame.init()
screen = None
clock = pygame.time.Clock()




class tab:
	def __init__(self, index, value = 0):
		self.index = index
		self.value = value
		self.rect = None

		font = pygame.font.SysFont(None, int(tab_dimension/2))
		self.textSurf = font.render(str(self.value), True, WHITE)
		self.textRect = self.textSurf.get_rect()

	def update(self):
		self.rect = pygame.draw.rect(screen, tab_color,
							(start_x + self.index[1]*step, start_y + self.index[0]*step,
							tab_dimension, tab_dimension))

		self.textRect.center = (start_x + self.index[1]*step + int(tab_dimension/2), start_y + self.index[0]*step + int(tab_dimension/2))
		screen.blit(self.textSurf, self.textRect)
		pygame.display.update([self.rect, self.textRect])

		if (self.index[0]*grid + self.index[1] + 1) == self.value:
			tab_seq[self.index[0]*grid + self.index[1]] = 1
		else:
			tab_seq[self.index[0]*grid + self.index[1]] = 0

class slider:
	def __init__(self, index):
		self.index = index
		self.value = 0
		self.rect = None
	def update(self):
		self.rect = pygame.draw.rect(screen, bg_color,
							(start_x + self.index[1]*step, start_y + self.index[0]*step,
							tab_dimension, tab_dimension))
		pygame.display.update(self.rect)
	def move(self, direction):
		if(self.check(direction)):
			print("end")
			return 0
		else:
			indexA = self.index
			indexB = self.find_index(direction)

			self.index = indexB
			tab_mat[indexB[0]][indexB[1]].index = indexA

			temp = tab_mat[indexA[0]][indexA[1]]
			tab_mat[indexA[0]][indexA[1]] = tab_mat[indexB[0]][indexB[1]]
			tab_mat[indexB[0]][indexB[1]] = temp

			update_board()
			
	def find_index(self, direction):
		if(direction == "right"):
			return (self.index[0], self.index[1] -1)
		if(direction == "left"):
			return (self.index[0], self.index[1] +1)
		if(direction == "down"):
			return (self.index[0] -1, self.index[1])
		if(direction == "up"):
			return (self.index[0] +1, self.index[1])

	def check(self, direction):
		if(direction == "right"):
			return (self.index[1] == 0)
		if(direction == "left"):
			return (self.index[1] == grid-1)
		if(direction == "down"):
			return (self.index[0] == 0)
		if(direction == "up"):
			return (self.index[0] == grid-1)


tab_mat = None
slide = None
def initiate():
	global tab_mat, slide, screen, start_x, start_y, step, tab_dimension, tab_seq
	
	#calculation for drawing squares
	tab_dimension = int(board_dimension/grid) - 2*border
	start = (int((width - board_dimension)/2), int((height - board_dimension)/2))
	start_x = start[0] + border
	end_x = board_dimension + start[0]
	start_y = start[1] + border
	end_y = board_dimension + start[1]
	step = tab_dimension + 2*border

	print("Initiating board...")
	#creating tabs
	tab_seq = list(range(1, grid*grid + 1))
	shuffle(tab_seq)
	tab_seq, slider_i = valid(tab_seq)
	#tab_seq += [0]
	tab_mat = [[tab((int(j/grid), i), val) for i,val in  enumerate(tab_seq[j:j+grid])] for j in range(0, len(tab_seq), grid)]
	slide = slider((slider_i//grid, slider_i%grid))
	tab_mat[slider_i//grid][slider_i%grid] = slide

	#creating screen
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Sliding Puzzle")


def valid(seq):
	valid = False
	#print (seq)
	x = seq.index(grid*grid)
	del(seq[x])
	#print(x, seq)

	inversion = 0
	for i in range(len(seq)):
		for j in range(i+1,len(seq)):
			if seq[i] > seq[j]:
				inversion += 1
				#print(seq[i], seq[j])
	#print(inversion)
	
	if grid%2 ==1:
		if inversion%2 == 0:
			valid = True
	else:
		if inversion%2 == 1 and (x//grid)%2 == 0:
			valid = True
		elif inversion%2 == 0 and (x//grid)%2 == 1:
			valid = True

	#print(inversion, x//grid, valid)
	if not valid:
		print("...")
		y = x 
		while (y == x or y == x-1):
			y = randrange(len(seq)-1)
			print("....")
		seq[y], seq[y+1] = seq[y+1], seq[y]
		#print(y)
	#print (inversion)
	seq.insert(x, 0)
	#print(seq)
	return seq, x

def update_board():
	for i in tab_mat:
		for j in i:
			j.update()



def gameloop():
	initiate()
	screen.fill(WHITE)
	pygame.draw.rect(screen,bg_color,((width - board_dimension)/2,(height - board_dimension)/2, board_dimension, board_dimension))
	update_board()
	pygame.display.update()
	#clock.tick(0)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.display.quit()
				return 0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				pygame.display.quit()
				return 0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				slide.move("up")
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
				slide.move("right")
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				slide.move("down")
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				slide.move("left")
		if (sum(tab_seq[:-1]) == grid*grid -1):
			print("\n\n\nWow! You solved it.\n\n")
			break
	while True:	
		font = pygame.font.SysFont(None, 100)
		textSurf = font.render("Good Job!", True, BLACK)
		textRect = textSurf.get_rect()
		textRect.center = (width//2, height//2)
		screen.blit(textSurf, textRect)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.display.quit()
				return 0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				pygame.display.quit()
				return 0

while True:
	try:
		grid = int(input("enter dimension: ")[0])
	except:
		grid = 4
	gameloop()
	# print([[i.index for i in j] for j in tab_mat])
	# print([[i.value for i in j] for j in tab_mat])
# print(start_x, start_y)
# print(end_x, end_y)
