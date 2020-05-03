# -*- coding: utf8 -*-
import sys, time, random
import pygame as pg

class Snake:

    def __init__(self, color):
        self.color = color

    def next_step(self, scale, size, direct, snake_head_coords):

        step = {
            'up':       lambda head: [head[0], head[1] - scale],
            'down':     lambda head: [head[0], head[1] + scale],
            'right':    lambda head: [head[0] + scale, head[1]],
            'left':     lambda head: [head[0] - scale, head[1]],
        }

        if_step_over = {
            'up':       lambda head: [head[0], size[1] - scale] if head[1] < 0 else False,
            'down':     lambda head: [head[0], 0] if head[1] > size[1] - scale else False,
            'right':    lambda head: [0, head[1]] if head[0] > size[0] - scale else False,
            'left':     lambda head: [size[0] - scale, head[1]] if head[0] < 0 else False,
        }



        new_snake_coords = step[direct](snake_head_coords)
        step_over = if_step_over[direct](new_snake_coords)
        if step_over:
            new_snake_coords = []
            new_snake_coords.extend(step_over) 

        return new_snake_coords

class Game:

    def __init__(self, width, height, scale, snake_coords = [[210,210],[210,180],[210, 150]], 
                    food_coords = [], direct = 'up', speed = 0.3):
        self.size = width, height
        self.screen = pg.display.set_mode( (width, height) )
        self.scale = scale
        self.snake_coords = snake_coords
        self.food_coords = food_coords
        self.direct = direct
        self.speed = speed
        self.counter = 0

        self.eat = {
                'up':       lambda head: [head[0], head[1] - scale],
                'down':     lambda head: [head[0], head[1] + scale],
                'right':    lambda head: [head[0] + scale, head[1]],
                'left':     lambda head: [head[0] - scale, head[1]],
            }

    def game_process(self, snake, food):
        time.sleep(self.speed)




        if self.counter == 15:
            self.counter = 0;

            busy_coords = []
            busy_coords.extend(self.food_coords)
            busy_coords.extend(list(map(lambda coords: [coords[0] + self.scale // 2, coords[1] + self.scale // 2], self.snake_coords)))
            new_food_coords = food.birth(self.size, self.scale, busy_coords)
            self.food_coords.append(new_food_coords)

        new_snake_coords = snake.next_step(self.scale, self.size, self.direct, self.snake_coords[-1])

        if self.snake_coords.count(new_snake_coords) != 0: sys.exit()

        self.snake_coords.pop(0)
        self.snake_coords.append(new_snake_coords)

        scraps_coords = [new_snake_coords[0] + self.scale // 2, new_snake_coords[1] + self.scale // 2]
        if self.food_coords.count(scraps_coords) != 0:
            addit_snake_chain = []
            addit_snake_chain.extend(self.eat[self.direct](new_snake_coords))
            self.snake_coords.append(addit_snake_chain)
            self.food_coords.pop(self.food_coords.index(scraps_coords))

        self.counter += 1

    def display(self, snake_color, food_color):
        for coords in self.snake_coords:
            snake_rect = *coords, self.scale, self.scale
            pg.draw.rect(self.screen, snake_color, snake_rect)

        for coords in self.food_coords:
            pg.draw.circle(self.screen, food_color, coords, self.scale // 2)

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

            new_food_coords = [x, y]
            if busy_coords.count(new_food_coords) == 0: break
            else: print('111')

        return new_food_coords

pg.init()

black = 0, 0, 0
orange = 255, 221, 0
white = 255, 255, 255

snake = Snake(color = white)
food = Food(color = orange)
game = Game(width = 510, height = 510, scale = 30, speed = 0.2)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit() 
        if event.type == pg.KEYDOWN:
            if event.key    == 273 and game.direct != 'down': 
                game.direct = 'up'
                break

            elif event.key  == 274 and game.direct != 'up': 
                game.direct = 'down'
                break

            elif event.key  == 275 and game.direct != 'left': 
                game.direct = 'right'
                break

            elif event.key  == 276 and game.direct != 'right': 
                game.direct = 'left' 
                break

    game.game_process(snake, food)
    game.screen.fill(black)
    game.display(snake_color = white, food_color = orange)
    pg.display.flip()

#cd documents/GitHub/pygame