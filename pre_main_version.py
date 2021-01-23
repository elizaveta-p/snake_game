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


def add_result_to_db(score, mins, secs):
    with sqlite3.connect('data/records.db') as con:
        cur = con.cursor()

        cur.execute(f"""INSERT INTO main VALUES ({score}, {mins}, {secs})""")


def get_results_from_database():
    with sqlite3.connect('data/records.db') as con:
        cur = con.cursor()

        result = list(cur.execute(f"""SELECT Score, Min, Sec 
FROM main
ORDER BY Score DESC, Min ASC, Sec ASC"""))[0:5]
        return result


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
        self.purple = pygame.Color(76, 0, 153)
        self.light_grass_color = pygame.Color(84, 158, 52)
        self.border_color = pygame.Color(43, 82, 27)
        self.ground_color = pygame.Color(222, 198, 120)

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.score = 0
        self.max_score = 253
        self.mins = 0
        self.secs = 0

        self.checking = False

    def load_graphic_elements(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        pygame.font.init()
        self.image = load_image('background.jpg')
        # rect = (160, 30, 400, 400)
        self.grass = load_image('grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (720, 460))
        self.apple = load_image('apple.png')
        self.apple = pygame.transform.scale(self.apple, (25, 25))
        self.play_surface.blit(self.image, (160, 30))
        self.snake = load_image('body_part.png')
        self.snake = pygame.transform.scale(self.snake, (25, 25))
        self.snake_head = load_image('snake_head.png')
        self.snake_head = pygame.transform.scale(self.snake_head, (25, 25))
        self.angled_part = load_image('angled_part.png')
        self.angled_part = pygame.transform.scale(self.angled_part, (25, 25))
        self.snake_tail = load_image('tail.png')
        self.snake_tail = pygame.transform.scale(self.snake_tail, (25, 25))

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        """Задаем surface(поверхность поверх которой будет все рисоваться)
                и устанавливаем загаловок окна"""
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
        self.play_surface.blit(self.image, (160, 30))

    def event_loop(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return change_to

    def refresh_screen(self):
        """обновляем экран и задаем фпс"""
        pygame.display.flip()
        game.fps_controller.tick(6)

    def show_score(self, start_time=None, choice=1):
        """Отображение результата"""
        s_font = pygame.font.SysFont('Sans', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.purple)
        s_rect = s_surf.get_rect()

        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
            s_rect.x -= 15
            s_rect.y -= 10
            s_rect.width += 10
            pygame.draw.ellipse(game.play_surface, game.ground_color, s_rect)
            # print(type(start_time), start_time/1000)
            time_font = pygame.font.SysFont('Sans', 40)
            start_time //= 1000
            mins = ('0' + str(start_time // 60))[-2:]
            self.mins = int(mins)
            secs = ('0' + str(start_time % 60))[-2:]
            self.secs = int(secs)
            curr_time = time_font.render(f"{mins}:{secs}", True, self.purple)
            time_rect = curr_time.get_rect()
            time_rect.x = 35
            time_rect.y = 50
            pygame.draw.rect(self.play_surface, game.ground_color, time_rect)
            self.play_surface.blit(curr_time, (35, 50))
        # при game_overe отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (350, 100)
            pygame.draw.rect(game.play_surface, game.white, s_rect)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        add_result_to_db(self.score, self.mins, self.secs)
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        fon = pygame.transform.scale(load_image('fon.jpg'), (self.screen_width, self.screen_height))
        self.play_surface.blit(fon, (0, 0))
        go_font = pygame.font.SysFont('Sans', 72)
        go_surf = go_font.render('Game over', True, self.brown)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(None, 0)
        self.end_buttons = pygame.sprite.Group()
        to_menu = pygame.sprite.Sprite()
        to_menu.image = load_image('button_to_menu.png')
        to_menu.image = pygame.transform.scale(to_menu.image, (150, 50))
        to_menu.rect = to_menu.image.get_rect()
        to_menu.rect.x = 285
        to_menu.rect.y = 200
        self.end_buttons.add(to_menu)
        self.end_buttons.draw(self.play_surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if (pos[0] in range(to_menu.rect.x, to_menu.rect.x + 150)) and \
                            (pos[1] in range(to_menu.rect.y, to_menu.rect.y + 50)):
                        self.start_screen()
            pygame.display.flip()
            self.fps_controller.tick(50)

    def you_win(self):
        add_result_to_db(self.score, self.mins, self.secs)
        fon = pygame.transform.scale(load_image('win_background.jpg'), (self.screen_width, self.screen_height))
        self.play_surface.blit(fon, (0, 0))
        go_font = pygame.font.SysFont('Sans', 72)
        go_surf = go_font.render('You win!!!', True, self.border_color)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(None, 0)
        self.end_buttons = pygame.sprite.Group()
        to_menu = pygame.sprite.Sprite()
        to_menu.image = load_image('button_to_menu.png')
        to_menu.image = pygame.transform.scale(to_menu.image, (150, 50))
        to_menu.rect = to_menu.image.get_rect()
        to_menu.rect.x = 285
        to_menu.rect.y = 200
        self.end_buttons.add(to_menu)
        self.end_buttons.draw(self.play_surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if (pos[0] in range(to_menu.rect.x, to_menu.rect.x + 150)) and \
                            (pos[1] in range(to_menu.rect.y, to_menu.rect.y + 50)):
                        self.start_screen()
            pygame.display.flip()
            self.fps_controller.tick(50)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        fon = pygame.transform.scale(load_image('start_background.jpg'), (self.screen_width, self.screen_height))
        self.play_surface.blit(fon, (0, 0))
        # print(filled_with_snake)
        self.buttons = pygame.sprite.Group()
        play_button = pygame.sprite.Sprite()
        play_button.image = load_image('button_play.png')
        play_button.image = pygame.transform.scale(play_button.image, (150, 50))
        play_button.rect = play_button.image.get_rect()
        play_button.rect.x = 285
        play_button.rect.y = 240
        self.buttons.add(play_button)
        instructions_button = pygame.sprite.Sprite()
        instructions_button.image = load_image('button_instructions.png')
        instructions_button.image = pygame.transform.scale(instructions_button.image, (150, 50))
        instructions_button.rect = instructions_button.image.get_rect()
        instructions_button.rect.x = 285
        instructions_button.rect.y = 310
        self.buttons.add(instructions_button)
        records_button = pygame.sprite.Sprite()
        records_button.image = load_image('button_records.png')
        records_button.image = pygame.transform.scale(records_button.image, (150, 50))
        records_button.rect = instructions_button.image.get_rect()
        records_button.rect.x = 285
        records_button.rect.y = 380
        self.buttons.add(records_button)
        self.buttons.draw(self.play_surface)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    self.start_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # print(pos)
                    if (pos[0] in range(play_button.rect.x, play_button.rect.x + 150)) and \
                            (pos[1] in range(play_button.rect.y, play_button.rect.y + 50)):
                        self.start_game()
                    elif (pos[0] in range(instructions_button.rect.x, instructions_button.rect.x + 150)) and \
                            (pos[1] in range(instructions_button.rect.y, instructions_button.rect.y + 50)):
                        self.instructions_screen()
                    elif (pos[0] in range(records_button.rect.x, records_button.rect.x + 150)) and \
                            (pos[1] in range(records_button.rect.y, records_button.rect.y + 50)):
                        self.show_record_table()
            for elem in filled_with_snake:
                choice = random.choice([self.brown, self.light_grass_color,
                                        self.black, self.ground_color])
                # choice = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # if choice == 1:
                #     pygame.draw.rect(self.play_surface, self.light_grass_color, (elem[1]*17, elem[0]*17, 17, 17))
                pygame.draw.rect(self.play_surface, choice, (elem[1] * 17, elem[0] * 17, 17, 17))
                pygame.draw.rect(self.play_surface, self.border_color, (elem[1] * 17, elem[0] * 17, 17, 17), 2)
            pygame.display.flip()
            self.fps_controller.tick(17)

    def instructions_screen(self):
        self.play_surface.fill(self.ground_color)
        text = ['Instruction', "1. Find apples and eat them. It adds one point to the score",
                'and lengthen the snake.', '2. Avoid touching dark green borders,', 'it will kill your snake.',
                "3. You can't bump into your body or cut off your tail,", 'it will also kill the snake.',
                '4. You will become a winner, if snake fills the entire field.']
        font = pygame.font.SysFont('Sans', 30)
        text_coord = 20
        for line in text:
            string_rendered = font.render(line, True, self.purple)
            rect = string_rendered.get_rect()
            text_coord += 10
            rect.top = text_coord
            rect.x = 10
            text_coord += rect.height
            self.play_surface.blit(string_rendered, rect)
        self.ins_scrn_buttons = pygame.sprite.Group()
        back_button = pygame.sprite.Sprite()
        back_button.image = load_image('button_to_menu.png')
        back_button.image = pygame.transform.scale(back_button.image, (150, 50))
        back_button.rect = back_button.image.get_rect()
        back_button.rect.x = 550
        back_button.rect.y = 390
        self.ins_scrn_buttons.add(back_button)
        self.ins_scrn_buttons.add(back_button)
        self.ins_scrn_buttons.draw(self.play_surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # print(pos)
                    if (pos[0] in range(back_button.rect.x, back_button.rect.x + 150)) and \
                            (pos[1] in range(back_button.rect.y, back_button.rect.y + 50)):
                        self.start_screen()
                        # return True
            pygame.display.flip()
            self.fps_controller.tick(50)

    def show_record_table(self):
        self.play_surface.fill(self.white)
        font = pygame.font.SysFont('Sans', 30)
        text_coord = 70
        header = 'Score:                   Time:'
        header_rend = font.render(header, True, self.brown)
        rect = header_rend.get_rect()
        rect.top = 30
        rect.x = 130
        self.play_surface.blit(header_rend, rect)
        table = get_results_from_database()
        for line in table:
            score = str(line[0])
            time = f"{('0' + str(line[1]))[-2:]}:{('0' + str(line[2]))[-2:]}"
            new_line = list(' ' * 30)
            new_line[:len(score) + 1] = list(score)
            new_line[-1 * len(time):] = list(time)
            new_line = ''.join(new_line)
            string_rendered = font.render(new_line, True, self.purple)
            rect = string_rendered.get_rect()
            text_coord += 10
            rect.top = text_coord
            rect.x = 160
            text_coord += rect.height
            self.play_surface.blit(string_rendered, rect)
        rec_scrn_buttons = pygame.sprite.Group()
        back_button = pygame.sprite.Sprite()
        back_button.image = load_image('button_to_menu.png')
        back_button.image = pygame.transform.scale(back_button.image, (150, 50))
        back_button.rect = back_button.image.get_rect()
        back_button.rect.x = 550
        back_button.rect.y = 390
        rec_scrn_buttons.add(back_button)
        rec_scrn_buttons.add(back_button)
        rec_scrn_buttons.draw(self.play_surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # print(pos)
                    if (pos[0] in range(back_button.rect.x, back_button.rect.x + 150)) and \
                            (pos[1] in range(back_button.rect.y, back_button.rect.y + 50)):
                        self.start_screen()
            pygame.display.flip()
            self.fps_controller.tick(50)

    def start_game(self):
        clock = pygame.time.Clock()
        global game, snake, food, foods
        game = Game()

        game.load_graphic_elements()

        snake = Snake(game.green)
        snake_body_list = snake.get_body()
        foods = pygame.sprite.GroupSingle()
        food = Food(game.brown, game.board_width, game.board_height, game.cell_size, game.board_top, game.board_left,
                    snake_body_list, game.apple)
        foods.add(food.apple)

        game.init_and_check_for_errors()
        # game.set_surface_and_title()

        game.play_surface.fill(game.light_grass_color)

        game.play_surface.blit(game.grass, (0, 0, 720, 460))
        pygame.draw.rect(game.play_surface, game.border_color, (155, 25, 410, 410))
        start_time = pygame.time.get_ticks()
        while True:
            snake.change_to = game.event_loop(snake.change_to)
            snake.validate_direction_and_change()
            snake.change_head_position(game.cell_size)
            game.score, food.food_pos = snake.snake_body_mechanism(
                game.score, food.food_pos, game.board_width, game.board_height,
                game.cell_size, game.you_win, game.board_top, game.board_left)
            snake.draw_snake(game.play_surface, game.ground_color)
            snake.check_for_boundaries(
                game.game_over, game.board_width, game.board_height, game.you_win, game.board_left, game.board_top,
                game.cell_size, game.score, game.max_score)
            food.draw_food(game.play_surface, foods)
            time_since_enter = pygame.time.get_ticks() - start_time
            game.show_score(time_since_enter)
            game.refresh_screen()


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
        # если вставлять просто snake_head_pos,
        # то на всех трех позициях в snake_body
        # окажется один и тот же список с одинаковыми координатами
        # и мы будем управлять змеей из одного квадрата

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height, cell_size, you_win, board_top, board_left):
        self.snake_body.insert(0, list(self.snake_head_pos))
        # print(self.snake_body)
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличивем score на один
            not_found = True
            while not_found:
                x = random.randrange(0, (screen_width / cell_size)) * cell_size
                y = random.randrange(0, (screen_height / cell_size)) * cell_size
                if [x + board_left, y + board_top] not in snake.snake_body:
                    not_found = False
                if len(self.snake_body) == 256 or game.checking:
                    not_found = False
                    you_win()
            # print(x, y)
            food_pos = [x + game.board_left,
                        y + game.board_top]
            score += 1
        else:
            # если не нашли еду, то убираем последний сегмент,
            # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        # print(f"after: {self.snake_body}")
        return score, food_pos

    def draw_snake(self, play_surface, ground_color):
        """Отображаем все сегменты змеи"""
        # play_surface.fill(surface_color)
        # game.play_surface.blit(game.image, (160, 30))
        pygame.draw.rect(play_surface, ground_color, (160, 30, 400, 400))
        # pygame.draw.rect(play_surface, game.border_color, (160, 30, 400, 400), 1)
        i = 0
        body_in_list = []
        for part in self.body_sprites.sprites():
            # print(i)
            # if i == 0:
            #     # part.image = game.snake_head
            #     if self.direction == "RIGHT":
            #         part.image = pygame.transform.rotate(game.snake_head, -90)
            #     elif self.direction == "LEFT":
            #         part.image = pygame.transform.rotate(game.snake_head, 90)
            #     elif self.direction == "UP":
            #         part.image = pygame.transform.rotate(game.snake_head, 0)
            #     elif self.direction == "DOWN":
            #         part.image = pygame.transform.rotate(game.snake_head, 180)
            if i < len(self.snake_body):
                part.rect.x = self.snake_body[i][0]
                part.rect.y = self.snake_body[i][1]
            i += 1
            body_in_list.append(part)
        if len(self.snake_body) > len(self.body_sprites.sprites()):
            new_snake_part = pygame.sprite.Sprite()
            # new_snake_part.image = game.snake
            new_snake_part.rect = game.snake.get_rect()
            new_snake_part.rect.x = self.snake_body[i][0]
            new_snake_part.rect.y = self.snake_body[i][1]
            self.body_sprites.add(new_snake_part)
            body_in_list.append(new_snake_part)
        self.is_angled(body_in_list)
        # self.body_sprites.draw(play_surface)
        # self.body_sprites.update()

    def check_for_boundaries(self, game_over, width, height, you_win, board_left, board_top, cell_size, score,
                             max_score):
        """Проверка, что столкунлись с концами экрана или сами с собой
        (змея закольцевалась)"""
        if score == max_score:
            you_win()
        if any((
                self.snake_head_pos[0] > board_left + width - cell_size
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > board_top + height - cell_size
                or self.snake_head_pos[0] not in range(board_left, board_left + width + 1)
                or self.snake_head_pos[1] not in range(board_top, board_top + height + 1)
        )):
            game_over()
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в
            # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()

    def is_angled(self, body):
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
                    part.image = game.angled_part
                elif (prev_part.rect.y < part.rect.y and next_part.rect.x < part.rect.x) or \
                        (next_part.rect.y < part.rect.y and prev_part.rect.x < part.rect.x):
                    part.image = pygame.transform.rotate(game.angled_part, 90)
                elif (prev_part.rect.y > part.rect.y and next_part.rect.x > part.rect.x) or \
                        (next_part.rect.y > part.rect.y and prev_part.rect.x > part.rect.x):
                    part.image = pygame.transform.rotate(game.angled_part, -90)
                else:
                    part.image = pygame.transform.rotate(game.angled_part, 180)
            elif (prev_part.rect.x == part.rect.x) and (part.rect.x == next_part.rect.x):
                part.image = game.snake
                next_part.image = game.snake
            else:
                part.image = pygame.transform.rotate(game.snake, 90)
                next_part.image = pygame.transform.rotate(game.snake, 90)
                # part.image = game.snake
                # next_part.image = game.snake
        head = body[0]
        next_part = body[1]
        if head.rect.x == next_part.rect.x:
            if head.rect.y < next_part.rect.y:
                head.image = game.snake_head
            else:
                head.image = pygame.transform.rotate(game.snake_head, 180)
        elif head.rect.y == next_part.rect.y:
            if head.rect.x > next_part.rect.x:
                head.image = pygame.transform.rotate(game.snake_head, -90)
            else:
                head.image = pygame.transform.rotate(game.snake_head, 90)
        tail = body[-1]
        prev_part = body[-2]
        if tail.rect.x == prev_part.rect.x:
            if tail.rect.y < prev_part.rect.y:
                tail.image = game.snake_tail
            else:
                tail.image = pygame.transform.rotate(game.snake_tail, 180)
        elif tail.rect.y == prev_part.rect.y:
            if tail.rect.x > prev_part.rect.x:
                tail.image = pygame.transform.rotate(game.snake_tail, -90)
            else:
                tail.image = pygame.transform.rotate(game.snake_tail, 90)
        self.body_sprites.draw(game.play_surface)
        self.body_sprites.update()

    def get_body(self):
        return snake.snake_body


class Food:
    def __init__(self, food_color, screen_width, screen_height):
        """Инит еды"""
        self.food_color = food_color
        self.food_size_x = self.food_size_y = game.cell_size
        not_found = True
        while not_found:
            x = random.randrange(0, (screen_width / game.cell_size)) * game.cell_size
            y = random.randrange(0, (screen_height / game.cell_size)) * game.cell_size
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
        foods.draw(play_surface)
        foods.update()


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

game = Game()

game.load_graphic_elements()

snake = Snake(game.green)
foods = pygame.sprite.GroupSingle()
food = Food(game.brown, game.board_width, game.board_height)

game.start_screen()
print('here')
game.init_and_check_for_errors()
game.set_surface_and_title()
game.start_screen()
