from __future__ import print_function
from board import Board
from font import font_dictionary
from pipe import Pipe
from mock import MagicMock, patch
from random import randint
from bird import Bird
from tinydb import TinyDB, Query
import math
import pygame
import sys
import time


try:
    from unicornhat import UnicornHat
except ImportError:
    print("[Game][error] An error occurred importing 'unicornhat'")
    mock = MagicMock()

    with patch.dict('sys.modules', {'unicornhat': mock}):
        from unicornhat import UnicornHat

try:
    import RPi.GPIO as Gpio
except ImportError:
    print("[Game][error] An error occurred importing 'RPi.GPIO'")
    mock = MagicMock()
    mock.setmode.return_value = True
    mock.setup.return_value = True
    mock.add_event_detect.return_value = True
    mock.add_event_callback.return_value = True
    mock.output.return_value = True
    mock.input.return_value = True
    mock.cleanup.return_value = True
    with patch.dict('sys.modules', {'RPi': mock, 'RPi.GPIO': mock.GPIO}):
        import RPi.GPIO as Gpio


class Game:
    SWITCHES = None

    BLOCK_SIZE = 32

    COLUMNS = 8
    ROWS = 8

    FPS = None

    COLORS = [
        # 0 - Black
        (0, 0, 0),
        # 1 - Green
        (0, 255, 0),
        # 2 - Red
        (255, 0, 0),
        # 3 - Purple
        (128, 0, 128),
        # 4 - Blue
        (0, 0, 255),
        # 5 - Orange
        (255, 165, 0),
        # 6 - Cyan
        (0, 255, 255),
        # 7 - Yellow
        (255, 255, 0),
        # 8 - Dark Grey
        (35, 35, 35),
        # 9 - White
        (255, 255, 255)
    ]

    SHAPES = [
        # Bird
        [
            [7],
        ],

        # Pipe
        [
            [1],
        ],
    ]

    WIDTH = None
    HEIGHT = None

    COUNTDOWN = None

    SCORE_INCREMENT = None

    SCORE = 0
    PIPES = 0

    INTERVAL = None
    INTERVAL_INCREMENT = None

    LEVEL = 1
    LEVEL_INCREMENT = None

    PAUSED = False

    GAMEOVER = False

    BACKGROUND_GRID = None

    BIRD_MOVED = True

    pygame = None
    pygame_font = None
    pygame_screen = None
    unicornhat = None
    db = None

    board = None
    bird = None
    pipe = None

    def __init__(self, switches, columns, rows, fps, countdown, interval, score_increment, level_increment, interval_increment, pygame_instance=None):
        self.SWITCHES = switches
        self.COLUMNS = columns
        self.ROWS = rows
        self.FPS = fps
        self.COUNTDOWN = countdown
        self.INTERVAL = interval
        self.SCORE_INCREMENT = score_increment
        self.LEVEL_INCREMENT = level_increment
        self.INTERVAL_INCREMENT = interval_increment

        if pygame_instance is None:
            self.pygame = pygame
        else:
            self.pygame = pygame_instance

        self.gpio = Gpio

        self.unicornhat = UnicornHat
        self.db = TinyDB('data/database.json')

        try:
            self.WIDTH = self.BLOCK_SIZE * self.COLUMNS + 150
            self.HEIGHT = self.BLOCK_SIZE * self.ROWS

            self.BACKGROUND_GRID = [
                [8 if x % 2 == y % 2 else 0 for x in xrange(self.COLUMNS)]
                for y in xrange(self.ROWS)
            ]

            self.pygame.init()
            self.pygame.key.set_repeat(0, 0)
            self.pygame_font = self.pygame.font.Font(self.pygame.font.get_default_font(), 12)
            self.pygame_screen = self.pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 24)
            self.pygame.event.set_blocked(self.pygame.MOUSEMOTION)

            self.unicornhat.rotation(180)
            self.unicornhat.brightness(0.4)

            self.board = Board(self.COLUMNS, self.ROWS)
            self.__generate_bird()
            self.__generate_pipe()
        except AttributeError:
            print("[Game][error] An error occurred initialising game")

    def start(self, run_once=False):
        print("[Game][info] Starting game")

        try:
            pygame_wait = True

            while pygame_wait:
                for event in self.pygame.event.get():
                    if event.type == self.pygame.KEYDOWN:
                        if event.key == self.pygame.K_RETURN:
                            pygame_wait = False
                        elif event.key == self.pygame.K_ESCAPE:
                            self.quit()

                self.pygame_screen.fill(self.COLORS[0])
                self.__display_message("Press to start")
                self.pygame.display.update()

            self.unicornhat.clear()
        except AttributeError:
            print("[Game][error] An error occurred starting game")

        self.__countdown()
        self.__loop()
        self.finish()

        if run_once is not True:
            self.start()

    def __countdown(self):
        print("[Game][info] Starting game countdown")

        try:
            seconds = 0

            while True:
                self.pygame_screen.fill(self.COLORS[0])
                remaining = (self.COUNTDOWN - seconds)

                if seconds > self.COUNTDOWN:
                    break

                if seconds == self.COUNTDOWN:
                    self.__display_message("Go!")
                else:
                    self.__display_message("%d!" % remaining)

                seconds += 1
                self.unicornhat.clear()
                self.pygame.display.update()
                self.pygame.time.wait(1000)

            self.pygame_screen.fill(self.COLORS[0])
            self.unicornhat.clear()
        except AttributeError:
            print("[Game][error] An error occurred starting game countdown")

    def __loop(self):
        print("[Game][info] Starting game loop")

        try:
            self.pygame.time.set_timer(pygame.USEREVENT + 1, self.INTERVAL)

            key_actions = {
                'ESCAPE': lambda: self.quit(),
                'UP': lambda: self.__direction_up(),
                'p': lambda: self.toggle_pause(),
            }

            pygame_clock = self.pygame.time.Clock()

            while not self.GAMEOVER:
                self.unicornhat.clear()
                self.pygame_screen.fill(self.COLORS[0])

                if self.PAUSED:
                    self.__display_message("Paused")
                else:
                    self.__draw_line(
                        ((self.BLOCK_SIZE * self.COLUMNS) + 1, 0),
                        ((self.BLOCK_SIZE * self.COLUMNS) + 1, (self.HEIGHT - 1)),
                        self.COLORS[9]
                    )

                    self.__display_message(
                        "Score: %d\n\nLevel: %d\n\nPipes: %d" % (self.SCORE, self.LEVEL, self.PIPES),
                        ((self.BLOCK_SIZE * self.COLUMNS) + self.BLOCK_SIZE, 2),
                        self.COLORS[9],
                        self.COLORS[0],
                        False
                    )

                    self.__draw_matrix(self.BACKGROUND_GRID, (0, 0), None, False)
                    self.__draw_matrix(self.board.coordinates(), (0, 0), None, False)
                    self.__draw_matrix(self.pipe.coordinates(), (self.pipe.x(), self.pipe.y()))
                    self.__draw_matrix(self.bird.coordinates(self.COLUMNS, self.ROWS), (0, 0))

                self.pygame.display.update()

                for event in self.pygame.event.get():
                    if event.type == self.pygame.USEREVENT + 1:
                        self.__move()
                    elif event.type == self.pygame.QUIT:
                        self.quit()
                    elif event.type == self.pygame.KEYDOWN:
                        for key in key_actions:
                            if event.key == eval("self.pygame.K_" + key):
                                key_actions[key]()

                pygame_clock.tick(self.FPS)
        except AttributeError as e:
            print("[Game][error] An error occurred during game loop")
            print(e)

    def __generate_bird(self):
        print("[Game][info] Generating bird")

        self.bird = Bird(self.SHAPES[0], 1, int(math.floor(self.ROWS / 3)))

    def __generate_pipe(self):
        print("[Game][info] Generating pipe")

        offset_x, offset_y = (self.COLUMNS - 1,  0)
        gap = randint(0, 4)
        coordinates = []

        for x in range(1):
            for y in range(self.ROWS):
                rows = []

                if (y < gap) or (y > gap + 2):
                    rows.append(self.SHAPES[1][0][0])
                else:
                    rows.append(0)

                coordinates.append(rows)

        self.pipe = Pipe(coordinates, offset_x, offset_y)

    def __display_message(self, message, coordinates=None, color=COLORS[9], background_color=COLORS[0], unicornhat=True):
        print("[Game][info] Displaying message")

        if unicornhat:
            self.__scroll_message(message, text_colour=color, scroll_speed=0.05)

        for i, line in enumerate(message.splitlines()):
            message_image = self.pygame_font.render(line, False, color, background_color)

            if coordinates is not None:
                position_x, position_y = coordinates
            else:
                message_image_center_x, message_image_center_y = message_image.get_size()
                message_image_center_x //= 2
                message_image_center_y //= 2
                position_x = self.WIDTH // 2 - message_image_center_x
                position_y = self.HEIGHT // 2 - message_image_center_y

            self.pygame_screen.blit(
                message_image,
                (position_x, position_y + i * 22)
            )

    def __scroll_message(self, message, text_colour=COLORS[9], scroll_speed=0.05):
        r, g, b = text_colour
        scroll_rows = [[0] * 8] * 8

        for character in message:
            if character in font_dictionary:
                character_rows = font_dictionary[character]
            else:
                character_rows = font_dictionary['-']
            for i in range(8):
                scroll_rows[i] = scroll_rows[i] + character_rows[i]
                scroll_rows[i] += [0]

        for i in range(8):
            scroll_rows[i] += [0] * 8

        for scroll_position in range(len(scroll_rows[0]) - 8):
            for y in range(8):
                for x in range(8):
                    self.unicornhat.set_pixel(x, y, r, g, b)

            self.unicornhat.show()
            # time.sleep(scroll_speed)

    def __draw_line(self, start_position, end_position, color=COLORS[9], unicornhat=True):
        print("[Game][info] Drawing line")

        if unicornhat:
            start_x, start_y = start_position
            end_x, end_y = start_position

            for i in xrange(start_y, end_y):
                for j in xrange(start_x, end_x):
                    if start_x == end_x or start_y == end_y:
                        self.unicornhat.set_pixel(j, i, color)

        self.pygame.draw.line(self.pygame_screen, color, start_position, end_position)

    def __draw_matrix(self, matrix, offset, color=None, unicornhat=True):
        print("[Game][info] Drawing matrix")

        offset_x, offset_y = offset

        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    if color is None:
                        shape_color = self.COLORS[val]
                    else:
                        shape_color = color

                    if unicornhat:
                        self.unicornhat.set_pixel((offset_x + x), (offset_y + y), shape_color)

                    self.pygame.draw.rect(
                        self.pygame_screen,
                        shape_color,
                        self.pygame.Rect((offset_x + x) * self.BLOCK_SIZE, (offset_y + y) * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE),
                        0
                    )

    def __count_clear_pipes(self, pipes):
        print("[Game][info] Counting cleared pipes")

        if pipes > 0:
            self.PIPES += pipes
            self.SCORE += self.SCORE_INCREMENT * self.LEVEL

        if self.PIPES >= self.LEVEL * self.LEVEL_INCREMENT:
            self.LEVEL += 1
            delay = self.INTERVAL - self.INTERVAL_INCREMENT * (self.LEVEL - 1)
            delay = 100 if delay < 100 else delay
            self.pygame.time.set_timer(self.pygame.USEREVENT + 1, delay)

    def __move(self):
        print("[Game][info] Moving bird %s" % (self.bird.direction()))

        if not self.GAMEOVER and not self.PAUSED:
            new_x, new_y = self.bird.position()
            pipe_x, pipe_y = self.pipe.position()

            if self.bird.direction() == self.bird.DIRECTION_UP:
                new_y = self.bird.y() - 1
                self.bird.set_direction(self.bird.DIRECTION_DOWN)
            elif self.bird.direction() == self.bird.DIRECTION_DOWN:
                new_y = self.bird.y() + 1

            cleared_pipes = 0

            if pipe_x - 1 >= 0:
                self.pipe.set_position((pipe_x - 1, pipe_y))
            else:
                cleared_pipes += 1
                self.__generate_pipe()

            if self.board.check_collision(self.pipe, (new_x, new_y)):
                self.GAMEOVER = True

                return False

            self.bird.set_position((new_x, new_y))
            self.__count_clear_pipes(cleared_pipes)
            self.BIRD_MOVED = True

            return True

    def __direction_up(self):
        print("[Game][info] Event direction up")

        if self.BIRD_MOVED is True:
            self.bird.set_direction(self.bird.DIRECTION_UP)
            self.BIRD_MOVED = False

    def __direction_down(self):
        print("[Game][info] Event direction down")

        if self.BIRD_MOVED is True:
            self.bird.set_direction(self.bird.DIRECTION_DOWN)
            self.BIRD_MOVED = False

    def toggle_pause(self):
        print("[Game][info] Toggling paused state")

        self.PAUSED = not self.PAUSED

    def get_score(self):
        print("[Game][info] Calculating score")

        return self.SCORE

    def print_score(self, high_score=False):
        print("[Game][info] Printing score")

        score = self.get_score()

        try:
            self.unicornhat.clear()
            self.pygame_screen.fill(self.COLORS[0])

            if high_score:
                self.__display_message("Game Over!\n\nHigh score: %d" % score)
                self.pygame.display.update()
            else:
                self.__display_message("Game Over!\n\nYour score: %d!" % self.get_score())
                self.pygame.display.update()

            self.pygame.time.wait(3000)
        except AttributeError:
            print("[Game][error] An error occurred printing score")

    def finish(self):
        print("[Game][info] Finishing game")

        score = self.get_score()

        self.pygame.display.update()

        if self.db.contains(Query().score >= score):
            self.print_score()
        else:
            self.print_score(True)

        self.db.insert({'score': score})
        self.reset()

    def quit(self):
        print("[Game][info] Quitting game")

        self.pygame_screen.fill(self.COLORS[0])
        self.unicornhat.clear()
        self.__display_message("Exiting...")
        self.pygame.display.update()
        sys.exit()

    def reset(self):
        print("[Game][info] Resetting game")

        self.PAUSED = False
        self.GAMEOVER = False
        self.SCORE = 0
        self.PIPES = 0
        self.LEVEL = 1
        self.BIRD_MOVED = True

        self.board = Board(self.COLUMNS, self.ROWS)
        self.bird = None
        self.pipe = None
        self.__generate_bird()
        self.__generate_pipe()

        self.unicornhat.clear()
        self.pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        self.pygame.display.update()

    def cleanup(self):
        print("[Game][info] Game clean up")

        try:
            self.unicornhat.clear()
            self.pygame_screen.fill(self.COLORS[0])
            self.pygame.display.update()
            self.pygame.quit()
        except AttributeError:
            print("[Game][error] An error occurred cleaning up")

    def __exit__(self):
        print("[Game][info] Game exit")

        self.cleanup()
