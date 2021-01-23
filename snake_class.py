import os
import sqlite3

import pygame
import sys
import random
import time


ANGLED_PARTS = {'top_right': None,
                'top_left': None,
                'bottom_right': None,
                'bottom_left': None}
BODY = {'vertical': None, 'horizontal': None}
HEAD = {'top': None, 'right': None, 'bottom': None, 'left': None}
TAIL = {'top': None, 'right': None, 'bottom': None, 'left': None}


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


class Snake:
    def __init__(self, board_left, board_top):
        self.snake_head_pos = [board_left + 100, board_top + 50]  # [x, y]
        self.snake_body = [[board_left + 100, board_top + 50],
                           [board_left + 75, board_top + 50], [board_left + 50, board_top + 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.load_graphic_elems()
        self.body_sprites = pygame.sprite.Group()
        for i in self.snake_body:
            snake_part = pygame.sprite.Sprite()
            # snake_part.image = BODY['vertical']
            snake_part.rect = BODY['vertical'].get_rect()
            snake_part.rect.x = i[0]
            snake_part.rect.y = i[1]
            self.body_sprites.add(snake_part)

    def load_graphic_elems(self):
        angled_part = pygame.transform.scale(load_image('angled_part.png'), (25, 25))
        t_l = pygame.transform.rotate(angled_part, -90)
        b_r = pygame.transform.rotate(angled_part, 180)
        b_l = pygame.transform.rotate(angled_part, 90)
        parts = [angled_part, t_l, b_r, b_l]
        global ANGLED_PARTS, BODY, HEAD
        for i in range(len(ANGLED_PARTS)):
            ANGLED_PARTS[list(ANGLED_PARTS.keys())[i]] = parts[i]
        part = pygame.transform.scale(load_image('body_part.png'), (25, 25))
        parts = [part, pygame.transform.rotate(part, 90)]
        for i in range(len(BODY)):
            BODY[list(BODY.keys())[i]] = parts[i]
        head = pygame.transform.scale(load_image('snake_head.png'), (25, 25))
        parts = [head, pygame.transform.rotate(head, 90),
                 pygame.transform.rotate(head, 180), pygame.transform.rotate(head, -90)]
        for i in range(len(HEAD)):
            HEAD[list(HEAD.keys())[i]] = parts[i]
        tail = pygame.transform.scale(load_image('tail.png'), (25, 25))
        parts = [pygame.transform.rotate(tail, 180), pygame.transform.rotate(tail, -90),
                 tail, pygame.transform.rotate(tail, 90)]
        for i in range(len(TAIL)):
            TAIL[list(TAIL.keys())[i]] = parts[i]

    def validate_direction_and_change(self):
        """Изменияем направление движения змеи только в том случае,
        если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self, cell_size):
        """Изменияем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += cell_size
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= cell_size
        elif self.direction == "UP":
            self.snake_head_pos[1] -= cell_size
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += cell_size

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height, cell_size, you_win, board_top, board_left, checking, sound):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            not_found = True
            while not_found:
                x = random.randrange(0, (screen_width / cell_size)) * cell_size
                y = random.randrange(0, (screen_height / cell_size)) * cell_size
                if [x + board_left, y + board_top] not in self.snake_body:
                    not_found = False
                if len(self.snake_body) == 256 or checking:
                    not_found = False
                    you_win()
            food_pos = [x + board_left,
                        y + board_top]
            score += 1
            ch = sound.play()
            ch.play(sound)
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, ground):
        # pygame.draw.rect(play_surface, ground_color, (160, 30, 400, 400))
        play_surface.blit(ground, (160, 30, 400, 400))
        i = 0
        body_in_list = []
        for part in self.body_sprites.sprites():
            # print(i)
            if i < len(self.snake_body):
                part.rect.x = self.snake_body[i][0]
                part.rect.y = self.snake_body[i][1]
            i += 1
            body_in_list.append(part)
        if len(self.snake_body) > len(self.body_sprites.sprites()):
            new_snake_part = pygame.sprite.Sprite()
            # new_snake_part.image = game.snake
            new_snake_part.rect = BODY['vertical'].get_rect()
            new_snake_part.rect.x = self.snake_body[i][0]
            new_snake_part.rect.y = self.snake_body[i][1]
            self.body_sprites.add(new_snake_part)
            body_in_list.append(new_snake_part)
        self.is_angled(play_surface, body_in_list)
        # self.body_sprites.draw(play_surface)
        # self.body_sprites.update()

    def check_for_boundaries(self, game_over, width, height, you_win, board_left, board_top, cell_size, score,
                             max_score):
        """Проверка, что столкунлись с концами экрана или сами с собой
        (змея закольцевалась)"""
        # print(self.snake_body)
        if score == max_score:
            you_win()
        if any((
                self.snake_head_pos[0] > board_left + width - cell_size
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > board_top + height - cell_size
                or self.snake_head_pos[0] not in range(board_left, board_left + width + 1)
                or self.snake_head_pos[1] not in range(board_top, board_top + height + 1)
        )):
            print('first game over')
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                print('second game over')
                game_over()

    def is_angled(self, play_surface, body):
        for i in range(1, len(body[:-1])):
            prev_part = body[i - 1]
            part = body[i]
            next_part = body[i + 1]
            # print(prev_part.rect.x, part.rect.x, next_part.rect.x)
            # print(prev_part.rect.y, part.rect.y, next_part.rect.y)
            if ((prev_part.rect.x != part.rect.x) or (part.rect.x != next_part.rect.x)) and \
                    ((prev_part.rect.y != part.rect.y) or (part.rect.y != next_part.rect.y)):
                # print('is angled')
                # part.image = game.angled_part
                if (prev_part.rect.y < part.rect.y and next_part.rect.x > part.rect.x) or \
                        (next_part.rect.y < part.rect.y and prev_part.rect.x > part.rect.x):
                    part.image = ANGLED_PARTS['top_right']
                elif (prev_part.rect.y < part.rect.y and next_part.rect.x < part.rect.x) or \
                        (next_part.rect.y < part.rect.y and prev_part.rect.x < part.rect.x):
                    part.image = ANGLED_PARTS['bottom_left']
                elif (prev_part.rect.y > part.rect.y and next_part.rect.x > part.rect.x) or \
                        (next_part.rect.y > part.rect.y and prev_part.rect.x > part.rect.x):
                    part.image = ANGLED_PARTS['top_left']
                else:
                    part.image = ANGLED_PARTS['bottom_right']
            elif (prev_part.rect.x == part.rect.x) and (part.rect.x == next_part.rect.x):
                part.image = BODY['vertical']
                next_part.image = BODY['vertical']
            else:
                part.image = BODY['horizontal']
                next_part.image = BODY['horizontal']
                # part.image = game.snake
                # next_part.image = game.snake
        head = body[0]
        next_part = body[1]
        if head.rect.x == next_part.rect.x:
            if head.rect.y < next_part.rect.y:
                head.image = HEAD['top']
            else:
                head.image = HEAD['bottom']
        elif head.rect.y == next_part.rect.y:
            if head.rect.x > next_part.rect.x:
                head.image = HEAD['left']
            else:
                head.image = HEAD['right']
        tail = body[-1]
        prev_part = body[-2]
        if tail.rect.x == prev_part.rect.x:
            if tail.rect.y < prev_part.rect.y:
                tail.image = TAIL['bottom']
            else:
                tail.image = TAIL['top']
        elif tail.rect.y == prev_part.rect.y:
            if tail.rect.x > prev_part.rect.x:
                tail.image = TAIL['right']
            else:
                tail.image = TAIL['left']
        self.body_sprites.draw(play_surface)
        self.body_sprites.update()

    def get_body(self):
        return self.snake_body
    