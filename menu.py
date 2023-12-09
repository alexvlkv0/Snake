import os
import time

class Menu:
    def __init__(self):
        self.art = self.copy_art()
        self.numbers = [self.art[i].split("\n") for i in range(10)]
        self.snake_art = [self.art[i].split("\n") for i in range(10, 14)]
        for i in range(len(self.snake_art)-1): self.snake_art[i].pop() # get rid of empty strings
        self.val = [self.numbers[0]]*2
        self.gradient = ['$','X','x','=','+',';',':','.']
        self.dist = 0
    
    def starting_screen(self):
        newText, loadText, gameText = [self.art[i].split("\n") for i in range(14, 17)]
        for i in range(len(newText)):
            print(newText[i] + ' '*5 + loadText[i])

    def copy_art(self):
        with open ('data/menu.txt', 'r') as f:
            a, i = [""], 0
            for line in f.readlines():
                if line != '\n': a[i] += line
                else: 
                    a.append("")
                    i+=1
        return a
    
    def change_num(self, n, value):
        num = self.snake_art[1] if not n else self.snake_art[2]
        number = self.numbers[value]
        for i in range(len(num)):
            num[i] = num[i].replace(self.val[n][i], number[i])
        self.val[n] = self.numbers[value]
        self.snake_art[n+1] = num
        os.system('cls')
        self.show()
    
    def get_input(self):
        val = int(input())
        self.change_num(0, val)
        val1 = int(input())
        self.change_num(1, val1)
        return {'size':val, 'speed':val1}
        
    def collapse(self, speed):
        full_art = []
        for i in self.snake_art:
            full_art += i
        print('\n'.join(full_art))
        
        queue,i = [], 0
        while True:
            if i <= len(full_art)-1: queue.insert(0, full_art[i])
            elif queue: queue.pop()
            else: break
            i+=1
            for pos in range(len(queue)):
                if pos < len(self.gradient):
                    queue[pos] =  ''.join(map(lambda a: self.gradient[pos] if a != ' ' else a, queue[pos]))
                else:
                    queue.pop()
            os.system('cls')
            print('\n'.join(reversed(queue)) + '\n' + '\n'.join(full_art[i:]))
            time.sleep(1/(speed+4))

    def show(self):
        for line in self.snake_art:
            print('\n'.join(line))

if __name__ == '__main__':
    a=Menu()
    a.starting_screen()
    a.show()
    vals=a.get_input()
    a.collapse(vals['speed'])
    