from random import randint
from threading import Thread
from pynput import keyboard
import time
import os

class Snake:
	def __init__(self,size=10,speed=2):
		self.speed = speed
		self.score = 0
		self.size = size
		self.flag = False
		#self.snakegen = self.snake_gen(size)
		self.direction = 'r'

	def snake_gen(self,size): #Screen instances generator
		snake = [[self.size//2, self.size//2] for _ in (1, 2)]
		end = self.size-1
		head = snake[0]
		apple = self.spawn_apple() #spawn apple
		while not self.flag:
			#check if apple eaten
			if head == apple:
				snake.append(apple)
				self.score += 1 + len(snake) // 4
				while True:	#spawn new one
					apple = self.spawn_apple()
					if apple not in snake: break 
			#draw screen and apple
			screen = [['.' for i in range(size)] for i in range(size)]
			screen[apple[0]][apple[1]] = '@'
			#draw snake
			for piece in snake: 
				screen[piece[0]][piece[1]] = '#'
			screen[head[0]][head[1]] = '$'
			yield screen
			#move
			for i in range(len(snake)-1,0,-1): 
				snake[i] = snake[i-1][:]
			#turn
			match self.direction:
				case "u":
					head[0] = head[0]-1 if head[0] != 0 else end #up
				case 'd':
					head[0] = head[0]+1 if head[0] != end else 0 #down
				case 'l':
					head[1] = head[1]-1 if head[1] != 0 else end #left
				case 'r':
					head[1] = head[1]+1 if head[1] != end else 0 #right
			if head in snake[1:]: self.end(1) #check if head crashes into tail
			if self.size**2 == len(snake): self.end(0) #win

	def spawn_apple(self):
		a_x = randint(0,self.size-1)
		a_y = randint(0,self.size-1)
		return [a_x, a_y]

	def start(self): #Выводит экран
		for screen in self.snake_gen(self.size):
			s = ''
			for row in screen:
				s += ' '.join(row) + '\n'
			os.system('cls')
			print(s)
			time.sleep(1 / self.speed)
   
	def end(self, l): #1 - win, 0 - lose
		#read arts
		art = ['']*6
		with open ('art.txt', 'r') as f:
			i = 0
			for line in f.readlines():
				if line != '\n':
					art[i] += line
				else: 
					i+=1
		if l:
      		#make snake
			s = ''
			n = self.score // 10
			if n < 2: s = art[1]
			elif n >= 2 and n < 4: s = art[2]
			else: #makes tail longer acording to score
				head = art[3].split('\n')
				tail = art[0].split('\n')
				for i in range(len(head)-1):
					s += '\n' + tail[i]*(n-4) + head[i]
			print(f'{s}{art[-2]}')
		else:
			print(f'{art[-1]}')
			#self.score = 777
		print(f'\nYou got \033[32m {self.score} \033[0m points, congrats')
		self.flag = True
  

def on_press(key):
    if key == keyboard.Key.up:
        snake.direction = 'u'
    elif key == keyboard.Key.down:
        snake.direction = 'd'
    elif key == keyboard.Key.left:
        snake.direction = 'l'
    elif key == keyboard.Key.right:
        snake.direction = 'r'
    elif key == keyboard.Key.esc:
        return False

def take_input():
    with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

if __name__ == "__main__":
	snake = Snake(size=4, speed=2)
	t1 = Thread(target=lambda: snake.start())
	t2 = Thread(target=take_input)
	t1.start()
	t2.start()
	t2.join()
	snake.end(1)
