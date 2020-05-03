import sys, time, copy
import pygame as pg

class Snake:

    def __init__(self, color, location = [ [210, 210], [210, 180], [210, 150] ], direct = 'up'):
        #self.length = length
        self.color = color
        #self.x = x
        #self.y = y
        self.location = location
        self.direct = direct

        #self.rect = x, y, 30, length * 30

    def status(self):
        return [self.color, self.location]

pg.init()

size = width, height = 510, 510
scale = 30
black = 0, 0, 0
white = 255, 255, 255
screen = pg.display.set_mode(size)

snake = Snake(color = white)

def display(screen, color, coords):
    #print('start')
    for pair in coords:
        rect = *pair, scale, scale
        #print(pair)
        pg.draw.rect(screen, color, rect)
    #print('finish')


while True:
    time.sleep(0.5)
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == 273: snake.direct = 'up'
            elif event.key == 274: snake.direct = 'down'
            elif event.key == 275: snake.direct = 'right'
            elif event.key == 276: snake.direct = 'left' 

    snake.location.pop(0)
    head = copy.deepcopy(snake.location[-1])

    if snake.direct == 'up': 
        head[1] -= scale
        if head[1] < 0:
            head[1] = height - scale
    elif snake.direct == 'down': 
        head[1] += scale
        if head[1] > height - scale:
            head[1] = 0
    elif snake.direct == 'right': 
        head[0] += scale
        if head[0] > width - scale:
            head[0] = 0
    elif snake.direct == 'left': 
        head[0] -= scale
        if head[0] < 0:
            head[0] = width - scale


    if head[1] < 0:
        head[1] = height - scale
    snake.location.append(head)
    #elif snake.direct == 'left':
        #snake.x += 30

   # if snake.x > width - snake.length * 30:
        #snake.x = 0

    #if snake.y < 0:
       # snake.y = height

    screen.fill(black)
    display(screen, *snake.status())
    #display(screen, white, [[210, 210], [240, 180]])
    pg.display.flip()

#cd documents/GitHub/pygame