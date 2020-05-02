import sys, time
import pygame as pg

class Snake:

    def __init__(self, color, length = 2, x = 210, y = 210, direct = 'up'):
        self.length = length
        self.color = color
        self.x = x
        self.y = y
        self.direct = direct

        self.rect = x, y, 30, length * 30

    def status(self):
        return [self.color, (self.x, self.y, 30, self.length * 30)]

pg.init()

size = width, height = 510, 510
black = 0, 0, 0
white = 255, 255, 255
screen = pg.display.set_mode(size)

snake = Snake(color = white)


while True:
    time.sleep(0.5)
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()

    if snake.direct == 'up':
        snake.y -= 30
    elif snake.direct == 'left':
        snake.x += 30

    if snake.x > width - snake.length * 30:
        snake.x = 0

    if snake.y < 0:
        snake.y = height

    screen.fill(black)
    pg.draw.rect(screen, *snake.status())
    pg.display.flip()
