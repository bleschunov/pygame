import sys, time, copy, random
import pygame as pg

class Snake:

    def __init__(self, color, location = [ [210, 210], [210, 180], [210, 150] ], direct = 'up'):
        self.color = color
        self.location = location
        self.direct = direct

    def next_step(self, screen, scale, food_coords):
        eaten_up = False
        game_flag = True
        addit = [] # addit[0] - head, [ addit[1] - next chain if has food ]
        self.location.pop(0)
        addit.append(self.location[-1])

        step = {
            'up':       lambda head: [head[0], head[1] - scale],
            'down':     lambda head: [head[0], head[1] + scale],
            'right':    lambda head: [head[0] + scale, head[1]],
            'left':     lambda head: [head[0] - scale, head[1]],
        }

        if_step_over = {
            'up':       lambda head: [head[0], height - scale] if head[1] < 0 else False,
            'down':     lambda head: [head[0], 0] if head[1] > height - scale else False,
            'right':    lambda head: [0, head[1]] if head[0] > width - scale else False,
            'left':     lambda head: [width - scale, head[1]] if head[0] < 0 else False,
        }

        if_on_food = {
            'up':       lambda head: [head[0], head[1] - scale],
            'down':     lambda head: [head[0], head[1] + scale],
            'right':    lambda head: [head[0] + scale, head[1]],
            'left':     lambda head: [head[0] - scale, head[1]],
        }

        addit[0] = step[self.direct](addit[0])
        if self.location.count(addit[0]) != 0: game_flag = False
        if if_step_over[self.direct](addit[0]):
            addit.append( if_step_over[self.direct](addit[0]) )


        snake_on_food_at = food_coords.count([addit[0][0] + scale // 2, addit[0][1] + scale // 2])
        if snake_on_food_at != 0:
            eaten_up = [addit[0][0] + scale // 2, addit[0][1] + scale // 2]
            addit.append( if_on_food[self.direct](addit[0]) )

        self.location.extend(addit)

        return eaten_up, game_flag

    def display(self, screen, scale):
        for coords in self.location:
            snake_rect = *coords, scale, scale
            pg.draw.rect(screen, self.color, snake_rect)

class GameMode:

    def __init__(self):
        pass

    def game_process(self, flag):
        if not flag: sys.exit()

class Food:

    def __init__(self, color, location = []):
        self.location = location
        self.color = color 

    def birth(self, size, scale, busy_coords):
        busy_coords.extend(list(map(lambda coords: [coords[0] + scale, coords[1]], busy_coords)))
        busy_coords.extend(list(map(lambda coords: [coords[0] - scale, coords[1]], busy_coords)))
        busy_coords.extend(list(map(lambda coords: [coords[0], coords[1] + scale], busy_coords)))
        busy_coords.extend(list(map(lambda coords: [coords[0], coords[1] - scale], busy_coords)))
        while True:
            x = random.randint(0, size[0] // scale) * scale + scale // 2
            y = random.randint(0, size[1] // scale) * scale + scale // 2

            xy = [x, y]
            if busy_coords.count(xy) == 0: break
               
        self.location.extend( [xy] )

    def display(self, screen, scale):
        for coords in self.location:
            pg.draw.circle(screen, self.color, coords, scale // 2)

    def clean_scraps(self, screen, coords):
        if coords:
            self.location.pop(self.location.index(coords))

pg.init()

size = width, height = 510, 510
scale = 30
black = 0, 0, 0
orange = 255, 221, 0
white = 255, 255, 255
screen = pg.display.set_mode(size)

snake = Snake(color = white, location = [ [210, 210], [210, 180], [210, 150], [210, 120], [210, 90] ])
food = Food(color = orange)
game = GameMode()

while True:
    time.sleep(0.3)
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit() 
        if event.type == pg.KEYDOWN:
            if event.key    == 273 and snake.direct != 'down': 
                snake.direct = 'up'
                break

            elif event.key  == 274 and snake.direct != 'up': 
                snake.direct = 'down'
                break

            elif event.key  == 275 and snake.direct != 'left': 
                snake.direct = 'right'
                break

            elif event.key  == 276 and snake.direct != 'right': 
                snake.direct = 'left' 
                break
    
    busy_coords = []
    busy_coords.extend(food.location + snake.location)
    food.birth(size, scale, busy_coords)
    screen.fill(black)
    eaten_up, game_flag = snake.next_step(screen, scale, food.location)
    game.game_process(game_flag)
    snake.display(screen, scale)
    food.clean_scraps(screen, eaten_up)
    food.display(screen, scale)
    pg.display.flip()

#cd documents/GitHub/pygame