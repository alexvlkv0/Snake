import time, os, menu, random
from pynput import keyboard
from threading import Thread

class Game:
	def __init__(self,size=10,speed=3):
		self.speed = speed # скорость змейки
		self.score = 0 # счет
		self.size = size # размер поля
		self.flag = False # проигрыш
		self.direction = [-1, 0] # направление движения [по строкам, по столбцам]
		self.input = self.direction # вводимое с клавиатуры направление
		self.prev = []

	def snake_gen(self,size): #Screen instances generator
		snake = [[self.size//2, self.size//2] for _ in (1, 2)] if not self.prev else self.prev
		head = snake[0]
		apple = self.spawn_apple() #spawn apple
  
		while not self.flag:
			#check if apple eaten
			if head == apple:
				snake.append(apple)
				self.score += 5 + len(snake) // 4
				while True:	#spawn new one
					apple = self.spawn_apple()
					if apple not in snake: break 
     
			#draw screen and apple
			screen = [['.' for i in range(size)] for i in range(size)]
			screen[apple[0]][apple[1]] = '@'
   
			#draw snake
			for piece_ind in range(1, len(snake)): 
				screen[snake[piece_ind][0]][snake[piece_ind][1]] = '#'
			screen[head[0]][head[1]] = '$'
			yield screen
			self.prev = snake # saving snakes position
   
			#move
			for i in range(len(snake)-1,0,-1): 
				snake[i] = snake[i-1][:]
			#change direction
			if self.input[0] != -self.direction[0] or self.input[1] != -self.direction[1]: # checking if we are not moving opposite way
				self.direction = self.input
			#turn	
			head[0] += self.direction[0]
			head[1] += self.direction[1]
			# if you cross a border you appear on the other side
			if head[0] == -1: head[0] = self.size-1
			elif head[0] == self.size: head[0] = 0
			elif head[1] == -1: head[1] = self.size-1
			elif head[1] == self.size: head[1] = 0
   
			if head in snake[1:]: self.end(1) #check if head crashes into tail
			if self.size**2 == len(snake): self.end(0) #win

	def spawn_apple(self):
		a_x = random.randint(0,self.size-1)
		a_y = random.randint(0,self.size-1)
		return [a_x, a_y]

	def start(self): #Выводит экран
		for screen in self.snake_gen(self.size):
			s = ''
			for row in screen:
				s += '| ' + ' '.join(row) + ' |\n'
			os.system('cls')
			print(' ' + '__' * self.size + '_')
			print(s, end = '')
			print(' ' + '‾‾' * self.size + '‾')
			time.sleep(1 / self.speed)
   
	def end(self, outcome): 
		#read arts
		art = ['']*6
		with open ('data/art.txt', 'r') as f:
			i = 0
			for line in f.readlines():
				if line != '\n':
					art[i] += line
				else: i+=1
		if outcome == 1:
      		#make snake
			s = ''
			n = self.score // 10
			if n < 1: s = art[1]
			elif n >= 1 and n < 3: s = art[2]
			else: #makes tail longer acording to score
				head = art[3].split('\n')
				tail =  art[0].split('\n')
				for i in range(0, len(head)-1):
					s += '\n' + tail[i]*(n-3) + head[i]
			print(f'{s}\n{art[4]}')
		elif outcome == 0:
			print(f'{art[5]}')
		else:
			self.flag = True
			return 0
		print(f'\nYou got \033[32m {self.score} \033[0m points, congrats')
		print("\nPress escape to exit...")
		self.flag = True
  
	def save(self):
		with open("data/data.txt", "w") as f:
			f.write('\n'.join(str(k) for k in [self.size,self.speed,self.score, ' '.join(str(i) for i in self.direction)]) + '\n')
			for piece in self.prev:
				f.write(f'{str(piece[0])} {str(piece[1])}\n')
		
	@classmethod
	def load(self):
		try:
			with open("data/data.txt", "r") as f:
				data = [line.replace('\n', '') for line in f.readlines()]
				loaded = Game(int(data[0]), int(data[1]))
				data.pop(0)
				data.pop(0)
				loaded.score, loaded.direction, *loaded.prev = data
				loaded.score = int(loaded.score)
				loaded.direction = [int(i) for i in loaded.direction.split()]
				loaded.input = loaded.direction
				loaded.prev = [[int(i) for i in piece.split()] for piece in loaded.prev]
			return loaded
		except Exception as ex:pass

def on_press(k):
	df, sp = keyboard.KeyCode, keyboard.Key # default KeyCode class for all letters and special for arrows
	# wasd or arrows controls. A bit messed up because arrow keys are different class
	if (type(k) == df and k.char == 'w') or (type(k) == sp and k == keyboard.Key.up):
		snake.input = [-1, 0] 
	elif (type(k) == df and k.char == 's') or (type(k) == sp and k == keyboard.Key.down):
		snake.input = [1, 0]
	elif (type(k) == df and k.char == 'a') or (type(k) == sp and k == keyboard.Key.left):
		snake.input = [0, -1]
	elif (type(k) == df and k.char == 'd') or (type(k) == sp and k == keyboard.Key.right):
		snake.input = [0, 1]
	if type(k) == sp and k == keyboard.Key.esc:
		return False

def listen():
	with keyboard.Listener(on_press=on_press) as listener:
		listener.join()

if __name__ == "__main__":
 
	# loading screen
	a = menu.Menu()
	load = a.load_screen()
	
	# load
	if load: snake = Game.load()
	if not load or not snake: # if file is empty or failed to load
		a.show()
		vals = a.get_input()
		snake = Game(size=vals['size'], speed=vals['speed'])
  
	#controlls
	t1 = Thread(target=lambda: listen())
	t1.start()
	
 	#game
	t2 = Thread(target=lambda: snake.start())
	t2.start()
	
	t1.join() # wait for escape key to close
	if not snake.flag: snake.save() # if snake is alive - save
	snake.end(3)
