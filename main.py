import os
import sqlite3

import pygame
import sys
import random
import time

from snake_class import Snake
from game_class import Game
from food_class import Food


with open('data/snake_doc.txt', 'r') as file:
    data = [line.rstrip('\n') for line in file.readlines()]
    # print(data)
    snake_text = []
    filled_with_snake = []
    for row in range(11):
        line = data[row]
        if line != '':
            for col in range(31):
                symb = data[row][col]
                # print(symb)
                # print('here')
                snake_text.append(symb)
                if symb == '#':
                    filled_with_snake.append([row, col])

game = Game(filled_with_snake)

game.load_graphic_elements()

snake = Snake(game.board_left, game.board_top)
foods = pygame.sprite.GroupSingle()
food = Food(game.board_width, game.board_height, game.cell_size, game.board_top, game.board_left,
            snake.snake_body)
foods.add(food.apple)
game.start_screen()

print('here')
game.init_and_check_for_errors()
game.set_surface_and_title()
game.start_screen()
