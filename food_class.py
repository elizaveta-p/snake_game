import os
import sqlite3

import pygame
import sys
import random
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print('not found')
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    else:
        image = image.convert_alpha()
    return image


class Food:
    def __init__(self, screen_width, screen_height, cell_size, board_top, board_left, snake_body):
        self.food_size_x = self.food_size_y = cell_size
        not_found = True
        while not_found:
            x = random.randrange(0, (screen_width / cell_size)) * cell_size
            y = random.randrange(0, (screen_height / cell_size)) * cell_size
            if [x + board_left, y + board_top] not in snake_body:
                not_found = False
        print(x, y)
        self.food_pos = [x + board_left,
                         y + board_top]
        sheet = pygame.transform.scale(load_image('apple_list.png'), (75, 75))
        self.apple = AnimatedSprite(pygame.transform.scale(load_image('apple2.png'), (25, 25)),
                                    pygame.transform.scale(load_image('apple3.png'), (25, 25)),
                                    pygame.transform.scale(load_image('apple4.png'), (25, 25)),
                                    self.food_pos[0], self.food_pos[1])

    def draw_food(self, play_surface, foods):
        x = self.food_pos[0]
        y = self.food_pos[1]
        self.apple.rect = self.food_pos[0], self.food_pos[1], 25, 25
        self.apple.x = x
        self.apple.y = y
        foods.draw(play_surface)
        foods.update()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, im1, im2, im3, x, y):
        super().__init__()
        self.frames = [im1, im2, im3, im2]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(x, y, 25, 25)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
