import time, os, menu, random, pickle
from pynput import keyboard
from threading import Thread

class Snake:
	def __init__(self,size=10,speed=3):
		self.speed = speed
		self.score = 0
		self.size = size
		self.flag = False
		self.direction = 'd'
		self.prev = []

	def snake_gen(self,size): #Screen instances generator
		snake = [[self.size//2, self.size//2] for _ in (1, 2)] if not self.prev else self.prev
		end = self.size-1
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
    
			#turn
			match self.direction:
				case "w":
					head[0] = head[0]-1 if head[0] != 0 else end #up
				case 's':
					head[0] = head[0]+1 if head[0] != end else 0 #down
				case 'a':
					head[1] = head[1]-1 if head[1] != 0 else end #left
				case 'd':
					head[1] = head[1]+1 if head[1] != end else 0 #right
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
   
	def end(self, outcome): #1 - win, 0 - lose
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
			n = 8 # self.score // 10
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
		try:
			with open("data/data.pickle", "wb") as f:
				pickle.dump(self, f)
		except Exception as ex:
			print("Error during saving:", ex)
		
	@classmethod
	def load(self):
		try:
			with open("data/data.pickle", "rb") as f:
				return pickle.load(f)
		except Exception as ex:
			print("Error during loading or no save file found", ex)

class Controlls:
    def on_press(self, k):
        try:
            if k.char in ['w','a','s','d']:
                snake.direction = k.char
        except AttributeError:
            if k == keyboard.Key.esc:
                return False

    def listen(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
 
	# loading screen
	a = menu.Menu()
	
	# load
	snake = Snake.load()
	if not snake or snake.flag: # if file is empty(failed to load) or snake dead initialize again
		a.show()
		vals = a.get_input()
		a.collapse(vals['speed'])
		snake = Snake(size=vals['size'], speed=vals['speed'])
  
	#controlls
	c = Controlls()
	t1 = Thread(target=lambda: c.listen())
	t1.start()
	
 	#game
	t2 = Thread(target=lambda: snake.start())
	t2.start()
	
	t1.join() # wait for escape key to close
	snake.save() # save before closing so flag == false otherwise if dead flag == true and save will not load
	snake.end(3)