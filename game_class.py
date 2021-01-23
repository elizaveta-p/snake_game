import os

import pygame
import sys
import random

from snake_class import Snake
from food_class import Food

BACKGROUND_MUSIC = ['data/background_music.mp3', 'data/background_music_old.mp3']


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
    with open('data/records.txt', 'r') as file:
        data = [line.rstrip('\n') for line in file.readlines()]
    with open('data/records.txt', 'w') as file:
        data.append(f"{score};{mins};{secs}")
        data = '\n'.join(data)
        file.write(data)


def get_results_from_database():
    with open('data/records.txt', 'r') as file:
        data = [line.rstrip('\n').split(';') for line in file.readlines()]
        data = sorted(data, key=lambda x: (-int(x[0]), int(x[1]), int(x[2])))
        return data[0:5]


class Game:
    def __init__(self, filled_with_snake):

        self.filled_with_snake = filled_with_snake
        self.screen_width = 720
        self.screen_height = 460

        # set board size
        self.board_width = 400
        self.board_height = 400
        self.board_top = 30
        self.board_left = 160

        # set cell size to be able to change it later easily
        self.cell_size = 25

        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        self.purple = pygame.Color(76, 0, 153)
        self.light_grass_color = pygame.Color(84, 158, 52)
        self.border_color = pygame.Color(43, 82, 27)
        self.ground_color = pygame.Color(222, 198, 120)

        self.fps_controller = pygame.time.Clock()

        self.score = 0
        self.max_score = 253
        self.mins = 0
        self.secs = 0

        self.checking = False

    def load_graphic_elements(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        pygame.font.init()
        self.image = load_image('background.png')
        # rect = (160, 30, 400, 400)
        self.grass = load_image('grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (720, 460))
        self.apple = load_image('apple.png')
        self.apple = pygame.transform.scale(self.apple, (25, 25))
        self.play_surface.blit(self.image, (160, 30))
        self.snake_vert = load_image('body_part.png')
        self.snake_vert = pygame.transform.scale(self.snake_vert, (25, 25))
        self.snake_hor = pygame.transform.rotate(self.snake_vert, 90)
        self.snake_head = load_image('snake_head.png')
        self.snake_head = pygame.transform.scale(self.snake_head, (25, 25))
        self.angled_part_tr = load_image('angled_part.png')
        self.angled_part_tr = pygame.transform.scale(self.angled_part_tr, (25, 25))
        self.angled_part_tl = pygame.transform.rotate(self.angled_part_tr, -90)
        self.angled_part_br = pygame.transform.rotate(self.angled_part_tr, 180)
        self.angled_part_bl = pygame.transform.rotate(self.angled_part_tr, 90)
        self.snake_tail = load_image('tail.png')
        self.snake_tail = pygame.transform.scale(self.snake_tail, (25, 25))
        self.frame = load_image('frame4.png')
        self.frame = pygame.transform.scale(self.frame, (429, 429))

    def init_and_check_for_errors(self):
        check_errors = pygame.init()

        if check_errors[1] > 0:
            sys.exit()

    def init_sound_settings(self):
        pygame.mixer.init()
        self.button_sound = pygame.mixer.Sound('data/button_click.wav')
        self.eat_sound = pygame.mixer.Sound('data/food_eaten.wav')
        pygame.mixer.music.load(random.choice(BACKGROUND_MUSIC))
        self.game_over_sound = pygame.mixer.Sound('data/game_over_sound.wav')
        self.you_win_sound = pygame.mixer.Sound('data/you_win_sound.wav')

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
        game.play_surface.blit(self.frame, (144, 14, 429, 429))
        pygame.display.flip()
        game.fps_controller.tick(7)

    def show_score(self, start_time=None, choice=1):
        s_font = pygame.font.SysFont('Sans', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.purple)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
            s_rect.x -= 15
            s_rect.y -= 10
            s_rect.width += 10
            pygame.draw.ellipse(game.play_surface, game.ground_color, s_rect)
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

        else:
            s_rect.midtop = (350, 100)
            pygame.draw.rect(game.play_surface, game.white, s_rect)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        pygame.mixer.music.stop()
        ch = self.game_over_sound.play()
        ch.play(self.game_over_sound)
        add_result_to_db(self.score, self.mins, self.secs)
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
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
                        self.start_screen()
            pygame.display.flip()
            self.fps_controller.tick(50)

    def you_win(self):
        pygame.mixer.music.stop()
        ch = self.you_win_sound.play()
        ch.play(self.you_win_sound)
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
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
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
        self.init_sound_settings()

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
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
                        self.start_game()
                    elif (pos[0] in range(instructions_button.rect.x, instructions_button.rect.x + 150)) and \
                            (pos[1] in range(instructions_button.rect.y, instructions_button.rect.y + 50)):
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
                        self.instructions_screen()
                    elif (pos[0] in range(records_button.rect.x, records_button.rect.x + 150)) and \
                            (pos[1] in range(records_button.rect.y, records_button.rect.y + 50)):
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
                        self.show_record_table()
            for elem in self.filled_with_snake:
                choice = random.choice([self.brown, self.light_grass_color,
                                        self.black, self.ground_color])
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
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
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
                    if (pos[0] in range(back_button.rect.x, back_button.rect.x + 150)) and \
                            (pos[1] in range(back_button.rect.y, back_button.rect.y + 50)):
                        ch = self.button_sound.play()
                        ch.play(self.button_sound)
                        self.start_screen()
            pygame.display.flip()
            self.fps_controller.tick(50)

    def start_game(self):
        clock = pygame.time.Clock()
        global game, snake, food, foods
        game = Game(self.filled_with_snake)

        game.load_graphic_elements()
        game.init_sound_settings()

        snake = Snake(game.board_left, game.board_top)
        snake_body_list = snake.get_body()
        foods = pygame.sprite.GroupSingle()
        food = Food(game.board_width, game.board_height, game.cell_size, game.board_top, game.board_left,
                    snake_body_list)
        foods.add(food.apple)

        game.init_and_check_for_errors()

        game.play_surface.fill(game.light_grass_color)

        game.play_surface.blit(game.grass, (0, 0, 720, 460))
        pygame.mixer.music.play(-1)
        start_time = pygame.time.get_ticks()
        counter = 0
        while True:
            snake.change_to = game.event_loop(snake.change_to)
            snake.validate_direction_and_change()
            snake.change_head_position(game.cell_size)
            game.score, food.food_pos = snake.snake_body_mechanism(
                game.score, food.food_pos, game.board_width, game.board_height,
                game.cell_size, game.you_win, game.board_top, game.board_left, game.checking, self.eat_sound)

            snake.draw_snake(game.play_surface, self.image)
            snake.check_for_boundaries(
                game.game_over, game.board_width, game.board_height, game.you_win, game.board_left, game.board_top,
                game.cell_size, game.score, game.max_score)
            if counter % 5 == 0:
                food.apple.update()
            food.draw_food(game.play_surface, foods)
            counter += 1
            time_since_enter = pygame.time.get_ticks() - start_time
            game.show_score(time_since_enter)
            game.refresh_screen()