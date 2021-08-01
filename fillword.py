"""
fillword o V 4.0
controls:
mouse, arrows and holding space
"""

from random import choice, shuffle

import PySimpleGUI as Sg
import pygame

import fillword_maker

pygame.init()
time_codes = [15, 205, 328, 464, 628, 763, 864, 920, 1142, 1246, 1363, 1510, 1610, 1728, 1851, 1968,
              2168, 2308, 2454, 2540, 2691, 2801, 2972, 3104, 3222, 3392, 3486]
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
pygame.mixer.music.rewind()
pygame.mixer.music.set_pos(choice(time_codes))

debug = True  # DEBUG-----------------------


class Fillword:
    def __init__(self, matrix, shape):
        self.matrix = matrix
        self.shape = shape
        self.size = len(matrix)
        self.used_cells = []
        self.cells_color = {}


class Session:
    def __init__(self, core):

        cell_s = 50
        border_w = 4

        display_s = (cell_s + border_w) * core.size + border_w
        display = pygame.display.set_mode((display_s, display_s))
        pygame.display.set_caption('fillword o')

        clock = pygame.time.Clock()

        cursor_x = 0
        cursor_y = 0
        selecting = False
        selection = []

        possible_colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),
                           (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255),
                           (255, 0, 255), (255, 0, 128)]

        shuffle(possible_colors)

        game_status = True

        def run_game():
            nonlocal selecting, selection

            while game_status:
                clock.tick(60)
                if debug:
                    print(selection)
                    print(core.shape)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            move_cursor(0, -1)
                        if event.key == pygame.K_DOWN:
                            move_cursor(0, 1)
                        if event.key == pygame.K_RIGHT:
                            move_cursor(1, 0)
                        if event.key == pygame.K_LEFT:
                            move_cursor(-1, 0)
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:
                    selecting = True
                    move_cursor(0, 0)
                else:
                    if selecting:
                        check_sequence(selection)
                    selection = []
                    selecting = False
                display_update()

        def display_update():
            display.fill((255, 255, 255))

            draw_cursor()
            draw_field()
            draw_selection()
            draw_letters()
            pygame.display.flip()

        def draw_cursor():
            pygame.draw.rect(display, (0, 0, 0),
                             ((cell_s + border_w) * cursor_x,
                              (cell_s + border_w) * cursor_y,
                              cell_s + border_w * 2,
                              cell_s + border_w * 2))

        def draw_selection():
            if selecting:
                for i in range(len(selection)):
                    pygame.draw.rect(display,
                                     transform_colors(*possible_colors[0], len(selection), i),
                                     ((cell_s + border_w) * selection[i][0] + border_w,
                                      (cell_s + border_w) * selection[i][1] + border_w,
                                      cell_s, cell_s))

        def transform_colors(r, g, b, o, i):
            t = 1 - i / o
            return int(255 - (255 - r) * t), int(255 - (255 - g) * t), int(255 - (255 - b) * t)

        def draw_field():
            for i in range(core.size):
                for j in range(core.size):
                    pygame.draw.rect(display,
                                     core.cells_color.get((i, j), (200, 200, 200)),
                                     ((cell_s + border_w) * i + border_w,
                                      (cell_s + border_w) * j + border_w, cell_s, cell_s))

        def draw_letters():
            delta = 10
            for i in range(core.size):
                for j in range(core.size):
                    print_text(core.matrix[j][i],
                               (cell_s + border_w) * i + border_w + delta,
                               (cell_s + border_w) * j + border_w + delta)

        def print_text(message, x, y, font_color=(0, 0, 0), font_type='fontA.ttf', font_size=30):
            font_type = pygame.font.Font(font_type, font_size)
            text = font_type.render(message, True, font_color)
            display.blit(text, (x, y))

        def move_cursor(dx, dy):
            nonlocal cursor_x, cursor_y, selection
            if 0 <= cursor_x + dx < core.size:
                if 0 <= cursor_y + dy < core.size:
                    if (not selecting) or ((cursor_x + dx, cursor_y + dy) not in core.used_cells):
                        cursor_x += dx
                        cursor_y += dy
                        if selecting:
                            if (cursor_x, cursor_y) in selection:
                                selection = selection[:selection.index((cursor_x, cursor_y))]
                            selection.append((cursor_x, cursor_y))

        def check_sequence(s):
            nonlocal game_status
            if tuple(s) in core.shape:
                core.used_cells.extend(s)
                for i in range(len(s)):
                    core.cells_color[s[i]] = transform_colors(*possible_colors[0], len(s), i)
                possible_colors.pop(0)
            if len(core.used_cells) == core.size ** 2:
                Sg.Popup('YOU WIN', no_titlebar=True, auto_close=True, auto_close_duration=3)
                game_status = False

        run_game()


def choose():
    number_levels = 5
    event, values = Sg.Window(
        'Choose level', [
            [Sg.Listbox(list(range(1, 1 + number_levels)) + ['generate'],
                        size=(29, number_levels + 1),
                        key='choice')], [Sg.Button('Ok'), Sg.Button('Cancel')]]
    ).read(close=True)
    if event == 'Cancel' or not event:
        exit()
    if values['choice']:
        return values['choice'][0]
    else:
        return choose()


def load():
    n = str(choose())
    if n == 'generate':
        event, values = Sg.Window(
            'set', [[Sg.Text('size')],
                    [Sg.Listbox(list(range(3, 7)), size=(29, 4), default_values=[4], key='1')],
                    [Sg.Text('range of len of words')],
                    [Sg.Slider(key='2', orientation='horizontal', range=(3, 9), default_value=3)],
                    [Sg.Slider(key='3', orientation='horizontal', range=(3, 9), default_value=9)],
                    [Sg.Button('Ok'), Sg.Button('Cancel')]]).read(close=True)
        if event == 'Cancel' or not event:
            exit()
        if event == 'Ok':
            if values['1']:

                a = fillword_maker.main(values['1'][0], values['2'], values['3'])
                return Fillword(*a)

    with open(f'data/{n}/l.txt', encoding='utf-8') as i:
        i = list(i.read().strip())
        size = int(len(i) ** 0.5)
        mat = [[i[o + p * size] for o in range(size)] for p in range(size)]

    with open(f'data/{n}/s.txt', encoding='utf-8') as i:
        i = i.read().strip().split()
        shp = []
        for u in i:
            shp.append(tuple([(int(u[p]), int(u[p + 1])) for p in range(0, len(u), 2)]))
        shp = tuple(shp)
    return Fillword(mat, shp)


while True:
    Session(load())
