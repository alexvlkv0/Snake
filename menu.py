import os
import time

class Menu:
    def __init__(self):
        self.art = self.copy_art()
        self.numbers = [self.art[i].split("\n") for i in range(10)]
        self.snake_art = [self.art[i].split("\n") for i in range(10, 14)]
        for i in range(len(self.snake_art)-1): self.snake_art[i].pop() # get rid of empty strings
        #print("\n".join(self.snake_art[3]))
        self.val = [self.numbers[0]]*2
        self.gradient = ['$','X','x','=','+',';',':','.']
        self.dist = 0
    
    def copy_art(self):
        with open ('menu.txt', 'r') as f:
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
        return [val, val1]
        
    def collapse(self, b, g):
        queue,i = [], 0
        while True:
            if i <= len(b)-1: queue.insert(0, b[i])
            elif queue: queue.pop()
            else: break
            i+=1
            for pos in range(len(queue)):
                if pos < len(g):
                    queue[pos] =  ''.join(map(lambda a: g[pos] if a != ' ' else a, queue[pos]))
                else:
                    queue.pop()
            yield ('\n'.join(reversed(queue))) + '\n' + '\n'.join(b[i:])

    def close(self):
        full_art = []
        for i in self.snake_art:
            full_art += i
        print('\n'.join(full_art))
        for line in self.collapse(full_art, self.gradient):
            os.system('cls')
            print(line + '\n')
            time.sleep(0.2)
    
    def show(self):
        for line in self.snake_art:
            print('\n'.join(line))

if __name__ == '__main__':
    a=Menu()
    a.show()
    a.get_input()
    a.close()
    