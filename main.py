# -*- coding:utf-8 -*-

#import pygame_sdl2
#pygame_sdl2.import_as_pygame()

from pygame import init
from pygame.display import Info, set_mode, flip
from pygame.sprite import Group
from pygame import Surface, mixer
from pygame.time import Clock, delay
from pygame.event import get
from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN, mouse, K_RIGHT, K_LEFT
from random import choice
from hexagon import Hexagon
from labels import Text
from buttons import Hexagon_Button

init()
info_display = Info()
DISPLAY_WIDTH = info_display.current_w
DISPLAY_HEIGHT = info_display.current_h
DISPLAY_WIDTH = 854
DISPLAY_HEIGHT = 480

window = set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen = Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))

def generate_court(size=50, col_rows=10, col_cols=17, start_posx=0, start_posy=0):
    hexes = Group()
    id, x = 0, 0
    posy = start_posy
    posx = start_posx
    for j in range(col_cols):
        posx += size//1.45
        y = 0
        for i in range(col_rows):
            posy += size//1.24
            hexes.add(Hexagon(posx=posx, posy=posy, id_and_pos=(id, x, y), width=size, height=size))
            x += 2
            y += 1
        id += 1
        if posy == size//1.24 * col_rows + start_posy:
            posy = size//2.4 + start_posy
            x = 1
        elif posy == size//1.24 * col_rows + size//2.4 + start_posy:
            posy = start_posy
            x = 0
    return hexes

def Game_loop():
    size = DISPLAY_WIDTH / 16.0
    posx = (DISPLAY_WIDTH - (size//2) * 17) * 27 // 100
    posy = 0
    court = generate_court(size=size, start_posx=posx, start_posy=posy)
    snake = [(8, 18, 9),
             (8, 16, 8),
             (8, 14, 7)]
    prey = 0

    button_group = Group()
    left_button = Text(text=u'<', x=5, y=50, size=22,
                       font_file='a_Albionic.ttf', color=(250, 250, 250),
                       surface=screen)
    right_button = Text(text=u'>', x=85, y=50, size=22,
                       font_file='a_Albionic.ttf', color=(250, 250, 250),
                       surface=screen)
    button_group.add(left_button, right_button)
    menu_button = Hexagon_Button(lable=u'меню', posx=87, posy=2, font_size=3, font_file='a_Albionic.ttf',
                                  color=(35, 125, 30), text_color=(210, 205, 10), border_color=(210, 205, 10))

    wasted = Text(text=u'Потрачено!', x=6, y=35, size=7,
                  font_file='a_Albionic.ttf', color=(250, 150, 120), surface=screen)
    win = Text(text=u'Победа!', x=20, y=35, size=14,
                  font_file='a_Albionic.ttf', color=(250, 150, 120), surface=screen)
    points_label = Text(text=u'Очки: 0', x=2, y=2, size=3,
                  font_file='a_Albionic.ttf', color=(85, 170, 10), surface=screen)

    fps = Text(text=u'', x=5, y=2, size=2, font_file='a_Albionic.ttf',
                color=(85, 170, 10), surface=screen)

    apple_eat_sound = mixer.Sound('sounds/Apple_eat.ogg')
    apple_eat_sound.set_volume(1.0)

    finally_background = Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    vector = 1
    alpha = 0
    id = 8
    x = 14
    y = 7
    dt = 0
    clock = Clock()
    done = False
    while not done:
        mp = mouse.get_pos()
        for event in get():
            if event.type == QUIT:
                done = True
                continue
            if event.type == KEYDOWN:
                if vector > 0:
                    if event.key == K_LEFT:
                        vector -= 1
                    if event.key == K_RIGHT:
                        vector += 1
            if event.type == MOUSEBUTTONDOWN:
                if vector > 0:
                    if left_button.rect.collidepoint(mp):
                        vector -= 1
                    elif right_button.rect.collidepoint(mp):
                        vector += 1
                if menu_button.rect.collidepoint(mp):
                    done = True
                    continue
            if vector < 1 and vector > -1:
                vector = 6
            elif vector > 6:
                vector = 1

        if not prey:
            prey = choice(tuple(court))
            while prey.id_and_pos in snake:
                prey = choice(tuple(court))

        if dt > 400:
            dt = 0
            if vector == 1:
                x -= 2
                y -= 1
            elif vector == 2:
                x -= 1
                if x % 2 != 0:
                    y -= 1
                id += 1
            elif vector == 3:
                x += 1
                if x % 2 == 0:
                    y += 1
                id += 1
            elif vector == 4:
                x += 2
                y += 1
            elif vector == 5:
                x += 1
                if x % 2 == 0:
                    y += 1
                id -= 1
            elif vector == 6:
                x -= 1
                if x % 2 != 0:
                    y -= 1
                id -= 1

            next_step = (id, x, y)
            if next_step not in snake:
                if prey.id_and_pos != next_step:
                    snake.append(next_step)
                    snake.pop(0)
                else:
                    snake.append(next_step)
                    apple_eat_sound.play(0)
                    points_label.set_text(text=u'Очки: %s' % str(len(snake)-3))
                    prey = 0
                    #if len(snake) > 13:
                    #    vector = -1
                    #delay(10)
            else:
                vector = -1
            if id < 0 or id > 16 or y < 0 or y > 9:
                vector = -1

        screen.fill((20, 20, 40))
        court.update(screen, snake, prey)

        if vector == -1:
            if alpha < 200:
                alpha += 3
                finally_background.set_alpha(alpha)
            screen.blit(finally_background, (0, 0))
            #if len(snake) < 12:
            #    wasted.draw()
            #else:
            #    win.draw()
            wasted.set_text(text=u'Уничтожено %s жертв!' % str(len(snake)-3))
            wasted.draw()

        fps.set_text(u'FPS: %s' % clock.get_fps())
        fps.draw()

        button_group.draw(screen)
        menu_button.draw(screen, mp)
        points_label.draw()

        window.blit(screen, (0, 0))
        flip()
        clock.tick(40)
        dt += clock.get_tick()

def Main_loop():
    mixer.init()
    background_sound = mixer.Sound('sounds/Dr_Mario.ogg')
    background_sound.set_volume(0.2)
    background_sound.play(-1)
    Main_done = False

    size = DISPLAY_WIDTH / 6
    background = generate_court(size=size, start_posy=-size, start_posx=-size, col_rows=5, col_cols=10)
    start_button = Hexagon_Button(lable=u'Играть', posx=5, posy=2, font_size=8, font_file='a_Albionic.ttf',
                                  text_color=(95, 210, 10), border_color=(95, 210, 10))
    exit_button = Hexagon_Button(lable=u'Выйти', posx=60, posy=30, font_size=8, font_file='a_Albionic.ttf',
                                  text_color=(95, 210, 10), border_color=(95, 210, 10))
    while not Main_done:
        mp = mouse.get_pos()
        for event in get():
            if event.type == QUIT:
                Main_done = True
                continue
            if event.type == KEYDOWN:
                pass
            if event.type == MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(mp):
                    Game_loop()
                if exit_button.rect.collidepoint(mp):
                    Main_done = True
                    continue

        background.update(screen, (0, 0, 0), (0, 0, 0))

        start_button.draw(screen, mp)
        exit_button.draw(screen, mp)

        window.blit(screen, (0, 0))
        flip()

if __name__ == "__main__":
    Main_loop()