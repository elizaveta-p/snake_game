import os

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


class Game:
    def __init__(self):
        # задаем размеры экрана
        self.screen_width = 720
        self.screen_height = 460

        # set board size
        self.board_width = 400
        self.board_height = 400
        self.board_top = 30
        self.board_left = 160

        # set cell size to be able to change it later easily
        self.cell_size = 25

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.score = 0

    def load_graphic_elements(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        self.image = load_image('background.jpg')
        rect = (160, 30, 400, 400)
        self.apple = load_image('apple.png')
        self.apple = pygame.transform.scale(self.apple, (25, 25))
        self.play_surface.blit(self.image, (160, 30))
        self.snake = load_image('snake.png')
        self.snake = pygame.transform.scale(self.snake, (25, 25))
        self.snake_head = load_image('snake_head.png')
        self.snake_head = pygame.transform.scale(self.snake_head, (25, 25))

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        """Задаем surface(поверхность поверх которой будет все рисоваться)
                и устанавливаем загаловок окна"""
        # self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        # pygame.display.set_caption('Snake Game')
        # self.image = load_image('background.jpg')
        # rect = (160, 30, 400, 400)
        # self.apple = load_image('apple.png')
        # self.apple = pygame.transform.scale(self.apple, (25, 25))
        # self.play_surface.blit(self.image, (160, 30))
        # self.snake = load_image('snake.png')
        # self.snake = pygame.transform.scale(self.snake, (25, 25))
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        """Задаем surface(поверхность поверх которой будет все рисоваться)
        и устанавливаем загаловок окна"""
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        self.image = load_image('background.jpg')
        rect = (160, 30, 400, 400)
        self.apple = load_image('apple.png')
        self.apple = pygame.transform.scale(self.apple, (25, 25))
        self.play_surface.blit(self.image, (160, 30))

    def event_loop(self, change_to):
        """Функция для отслеживания нажатий клавиш игроком"""

        # запускаем цикл по ивентам
        for event in pygame.event.get():
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return change_to

    def refresh_screen(self):
        """обновляем экран и задаем фпс"""
        pygame.display.flip()
        game.fps_controller.tick(6)

    def show_score(self, choice=1):
        """Отображение результата"""
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_overe отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (360, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        fon = pygame.transform.scale(load_image('fon.jpg'), (self.screen_width, self.screen_height))
        self.play_surface.blit(fon, (0, 0))
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            pygame.display.flip()
            self.fps_controller.tick(50)
        # time.sleep(3)
        # pygame.quit()
        # sys.exit()

    def terminate(self):
        pygame.quit()
        sys.exit()
    #
    # def start_screen(self):
    #     intro_text = ["ЗАСТАВКА", "",
    #                   "Правила игры",
    #                   "Если в правилах несколько строк,",
    #                   "приходится выводить их построчно"]
    #
    #     fon = pygame.transform.scale(load_image('fon.jpg'), (self.screen_width, self.screen_height))
    #     self.play_surface.blit(fon, (0, 0))
    #     font = pygame.font.Font(None, 30)
    #     text_coord = 50
    #     for line in intro_text:
    #         string_rendered = font.render(line, 1, pygame.Color('green'))
    #         intro_rect = string_rendered.get_rect()
    #         text_coord += 10
    #         intro_rect.top = text_coord
    #         intro_rect.x = 10
    #         text_coord += intro_rect.height
    #         self.play_surface.blit(string_rendered, intro_rect)
    #
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.terminate()
    #             elif event.type == pygame.KEYDOWN or \
    #                     event.type == pygame.MOUSEBUTTONDOWN:
    #                 return True
    #         pygame.display.flip()
    #         self.fps_controller.tick(50)
    #
    # def instructions_screen(self):
    #     pass


class Snake:
    def __init__(self, snake_color):
        # важные переменные - позиция головы змеи и его тела
        self.snake_head_pos = [game.board_left + 100, game.board_top + 50]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[game.board_left + 100, game.board_top + 50],
                           [game.board_left + 75, game.board_top + 50], [game.board_left + 50, game.board_top + 50]]
        self.snake_color = snake_color
        # направление движение змеи, изначально
        # зададимся вправо
        self.direction = "RIGHT"
        # куда будет меняться напрвление движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction
        self.body_sprites = pygame.sprite.Group()
        for i in self.snake_body:
            snake_part = pygame.sprite.Sprite()
            snake_part.image = game.snake
            snake_part.rect = snake_part.image.get_rect()
            snake_part.rect.x = i[0]
            snake_part.rect.y = i[1]
            self.body_sprites.add(snake_part)

    def validate_direction_and_change(self):
        """Изменияем направление движения змеи только в том случае,
        если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Изменияем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += game.cell_size
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= game.cell_size
        elif self.direction == "UP":
            self.snake_head_pos[1] -= game.cell_size
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += game.cell_size

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        # если вставлять просто snake_head_pos,
        # то на всех трех позициях в snake_body
        # окажется один и тот же список с одинаковыми координатами
        # и мы будем управлять змеей из одного квадрата
        self.snake_body.insert(0, list(self.snake_head_pos))

        # если съели еду
        # if pygame.sprite.spritecollide(food.apple, snake.body_sprites,
        #                                False,
        #                                collided=lambda col: (self.snake_head_pos[0] == food_pos[0]
        #                                            and self.snake_head_pos[1] == food_pos[1])):
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):

            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            # food_pos = [random.randrange(1, screen_width/10)*10,
            #             random.randrange(1, screen_height/10)*10]
            # new_snake_part = pygame.sprite.Sprite()
            # new_snake_part.image = game.snake
            # new_snake_part.rect = new_snake_part.image.get_rect()

            not_found = True
            while not_found:
                x = random.randrange(1, (screen_width / game.cell_size)) * game.cell_size
                y = random.randrange(1, (screen_height / game.cell_size)) * game.cell_size
                if [x + game.board_left, y + game.board_top] not in snake.snake_body:
                    not_found = False
            # x = random.randrange(1, screen_width / game.cell_size) * game.cell_size
            # y = random.randrange(1, screen_height / game.cell_size) * game.cell_size
            print(x, y)
            food_pos = [x + game.board_left,
                        y + game.board_top]
            # food.apple.x = food_pos[0]
            # food.apple.y = food_pos[1]
            # foods.draw(game.play_surface)
            # foods.update()
            score += 1
        else:
            # если не нашли еду, то убираем последний сегмент,
            # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        """Отображаем все сегменты змеи"""
        play_surface.fill(surface_color)
        # for i in range(game.screen_height):
        #     for j in range(game.screen_width):
        #         pygame.draw.rect(game.play_surface, (200, 150, 200), (j * 10 + 0,
        #                                                         i * 10 + 0,
        #                                                         10, 10), 1)
        game.play_surface.blit(game.image, (160, 30))
        pygame.draw.rect(game.play_surface, (200, 150, 200), (160, 30, 400, 400), 1)
        # for pos in self.snake_body:
        # pygame.Rect(x,y, sizex, sizey)
        # pygame.draw.rect(
        #     play_surface, self.snake_color, pygame.Rect(
        #         pos[0], pos[1], game.cell_size, game.cell_size))
        # i = self.snake_body.index(pos)
        i = 0
        for part in self.body_sprites.sprites():
            print(i)
            if i == 0:
                part.image = game.snake_head
            if i < len(self.snake_body):
                part.rect.x = self.snake_body[i][0]
                part.rect.y = self.snake_body[i][1]
            i += 1
        if len(self.snake_body) > len(self.body_sprites.sprites()):
            new_snake_part = pygame.sprite.Sprite()
            new_snake_part.image = game.snake
            new_snake_part.rect = new_snake_part.image.get_rect()
            new_snake_part.rect.x = self.snake_body[i][0]
            new_snake_part.rect.y = self.snake_body[i][1]
            self.body_sprites.add(new_snake_part)
        self.body_sprites.draw(play_surface)
        self.body_sprites.update()

    def check_for_boundaries(self, game_over, width, height):
        """Проверка, что столкунлись с концами экрана или сами с собой
        (змея закольцевалась)"""
        if any((
                self.snake_head_pos[0] > game.board_left + width - game.cell_size
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > game.board_top + height - game.cell_size
                or self.snake_head_pos[0] not in range(game.board_left, game.board_left + game.board_width + 1)
                or self.snake_head_pos[1] not in range(game.board_top, game.board_top + game.board_height + 1)
        )):
            game_over()
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food:
    def __init__(self, food_color, screen_width, screen_height):
        """Инит еды"""
        print('------food init-------')
        self.food_color = food_color
        self.food_size_x = self.food_size_y = game.cell_size
        # self.food_size_y = 10
        not_found = True
        while not_found:
            x = random.randrange(1, (screen_width / game.cell_size)) * game.cell_size
            y = random.randrange(1, (screen_height / game.cell_size)) * game.cell_size
            if [x + game.board_left, y + game.board_top] not in snake.snake_body:
                not_found = False
        print(x, y)
        self.food_pos = [x + game.board_left,
                         y + game.board_top]
        self.apple = pygame.sprite.Sprite()
        # определим его вид
        self.apple.image = game.apple
        # и размеры
        # self.apple.rect = self.food_pos[0], self.food_pos[1], 25, 25
        # добавим спрайт в группу
        foods.add(self.apple)

    def draw_food(self, play_surface):
        """Отображение еды"""
        x = self.food_pos[0]
        y = self.food_pos[1]
        self.apple.rect = self.food_pos[0], self.food_pos[1], 25, 25
        # print(x, y)
        # print(f"left: {game.board_left} top: {game.board_top}")
        # pygame.draw.rect(
        #     play_surface, self.food_color, pygame.Rect(x, y,
        #         self.food_size_x, self.food_size_y))
        self.apple.x = x
        self.apple.y = y
        foods.draw(game.play_surface)
        foods.update()
        # game.play_surface.blit(game.apple, (x, y))


game = Game()

game.load_graphic_elements()

snake = Snake(game.green)
foods = pygame.sprite.GroupSingle()
food = Food(game.brown, game.board_width, game.board_height)

game.init_and_check_for_errors()
# game.set_surface_and_title()
# if game.start_screen():
#     pass

while True:
    snake.change_to = game.event_loop(snake.change_to)

    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, game.board_width, game.board_height)
    snake.draw_snake(game.play_surface, game.white)

    food.draw_food(game.play_surface)

    snake.check_for_boundaries(
        game.game_over, game.board_width, game.board_height)

    game.show_score()
    game.refresh_screen()
