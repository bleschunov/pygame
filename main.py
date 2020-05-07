# -*- coding: utf8 -*-
import sys, time, random
import pygame as pg

class Snake:

    def __init__(self, color, shape = 'rect', arr_coords = [ (210, 210), (210, 180), (210, 150) ], direct = 'up'):
        self.color = color
        self.shape = shape
        self.arr_coords = arr_coords # snake`s head -> arr_coords[-1]
        self.direct = direct

    def do_step(self):
        self.arr_coords.pop(0)
        scale = game.scale

        snake_steps = {
            'up':       lambda head: (head[0], head[1] - scale),
            'down':     lambda head: (head[0], head[1] + scale),
            'right':    lambda head: (head[0] + scale, head[1]),
            'left':     lambda head: (head[0] - scale, head[1]),
        }

        snake_head_coords = self.arr_coords[-1]
        result = snake_steps[self.direct](snake_head_coords)

        return result

    def grow(self):
        scale = game.scale

        grow = {
                'up':       lambda head: (head[0], head[1] - scale),
                'down':     lambda head: (head[0], head[1] + scale),
                'right':    lambda head: (head[0] + scale, head[1]),
                'left':     lambda head: (head[0] - scale, head[1]),
            }

        snake_head_coords = self.arr_coords[-1]
        result = grow[self.direct](snake_head_coords)

        return result

    def save_new_head_coords(self, new_snake_head_coords):
        self.arr_coords.extend([new_snake_head_coords])

    def delete_snake_head_coords(self):
        self.arr_coords.pop(-1)


class Food:

    def __init__(self, color, arr_coords = [], shape = 'circle'):
        self.color = color
        self.shape = shape
        self.arr_coords = arr_coords

    def birth(self):
        width = game.size[0]
        height = game.size[1]
        scale = game.scale

        busy_coords = []
        busy_coords.extend(food.arr_coords)
        busy_coords.extend(list(map(lambda coords: (coords[0] + scale // 2, coords[1] + scale // 2), snake.arr_coords)))

        busy_coords.extend(list(map(lambda coords: (coords[0] + scale, coords[1]), busy_coords)))
        busy_coords.extend(list(map(lambda coords: (coords[0] - scale, coords[1]), busy_coords)))
        busy_coords.extend(list(map(lambda coords: (coords[0], coords[1] + scale), busy_coords)))
        busy_coords.extend(list(map(lambda coords: (coords[0], coords[1] - scale), busy_coords)))

        while True:
            x = random.randint(0, width // scale - 1) * scale + scale // 2
            y = random.randint(0, height // scale - 1) * scale + scale // 2

            new_food_coords = (x, y)
            if busy_coords.count(new_food_coords) == 0: break

        return new_food_coords

    def save_new_food_coords(self, new_food_coords):
        self.arr_coords.append(new_food_coords)

    def clear_scraps(self, scraps_coords):
        scraps_index = self.arr_coords.index(scraps_coords)
        self.arr_coords.pop(scraps_index)


class Game:

    def __init__(self, game_speed, width = 510, height = 510, scale = 30):
        self.size = width, height
        self.screen = pg.display.set_mode(self.size)
        self.scale = scale
        self.game_speed = game_speed
        self.counter = 0

    def get_snake_on_food_coords(self):
        snake_head_coords = snake.arr_coords[-1]
        snake_coords_relative_food = snake_head_coords[0] + game.scale // 2, snake_head_coords[1] + game.scale // 2
        food_coords = food.arr_coords

        if food_coords.count(snake_coords_relative_food) != 0:
            return snake_coords_relative_food
        else:
            return False

    def is_snake_on_snake(self):
        snake_head_coords = snake.arr_coords[-1]

        snake_coords = []
        snake_coords.extend( snake.arr_coords )
        snake_coords.pop(-1)

        if snake_coords.count(snake_head_coords) != 0:
            return True
        else:
            return False

    def snake_outside_steps(self):
        width = game.size[0]
        height = game.size[1]
        scale = game.scale

        snake_outside_steps = {
            'up':       lambda head: (head[0], height - scale) if head[1] < 0 else False,
            'down':     lambda head: (head[0], 0) if head[1] > height - scale else False,
            'right':    lambda head: (0, head[1]) if head[0] > width - scale else False,
            'left':     lambda head: (width - scale, head[1]) if head[0] < 0 else False,
        }

        snake_head_coords = snake.arr_coords[-1]
        result = snake_outside_steps[snake.direct](snake_head_coords)
        
        return result

    def display(self):
        for tuple_coords in snake.arr_coords:
            draw_options = *tuple_coords, self.scale, self.scale
            pg.draw.rect(self.screen, snake.color, draw_options)

        for tuple_coords in food.arr_coords:
            pg.draw.circle(self.screen, food.color, tuple_coords, self.scale // 2)

    def finish(self):
        sys.exit()

colors = {
    'black':  (0, 0, 0),
    'white':  (255, 255, 255),
    'orange': (255, 221, 0),
}

game    = Game(game_speed = 0.2)
snake   = Snake(colors['white'])
food    = Food(colors['orange'])

pg.init()

while True:
    time.sleep(game.game_speed)
    game.counter += 1

    game.screen.fill(colors['black'])
    game.display()
    pg.display.flip()

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

    new_snake_head_coords = snake.do_step()
    snake.save_new_head_coords(new_snake_head_coords)

    if game.snake_outside_steps() != False:
        new_snake_head_coords = game.snake_outside_steps()

        snake.delete_snake_head_coords()
        snake.save_new_head_coords(new_snake_head_coords)

    if game.counter == 15:
        new_food_coords = food.birth()
        food.save_new_food_coords(new_food_coords)
        game.counter = 0

    if game.is_snake_on_snake():
        game.finish()

    #print(game.get_snake_on_food_coords())
    #print(food.arr_coords)
    if game.get_snake_on_food_coords() != False:
        scraps_coords = game.get_snake_on_food_coords()

        food.clear_scraps(scraps_coords)
        new_snake_head_coords = snake.grow()
        snake.save_new_head_coords(new_snake_head_coords)
