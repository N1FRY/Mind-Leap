import pygame
import tkinter.messagebox as mb
from sys import *
from pygame import *
from random import *
from player import *
from objects import *
from levels import *

# Переменные
WIN_WIDTH = 1280 # Ширина окна
WIN_HEIGHT = 800 # Высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "White" 
FPS = 60
running = True
# puzzle_complete = False

# Главная функция, заключающая в себе весь игровой процесс
def game(lvl, puz_completed = None):
    global running

    platforms = []
    puzzles = []
    buttons = []
    lamps = []
    cubes = []
    doors = []
    exits = []
    blocks = [platforms, buttons, doors, cubes]
    objects = [exits, puzzles, lamps]
    
    entities = pygame.sprite.Group() # Все объекты
    screen = pygame.display.set_mode(DISPLAY) # Создание окна программы
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Поверхность, являющаяся задним фоном для игры
    pygame.display.update() 
    bg.fill(Color(BACKGROUND_COLOR)) # Цвет заднего фона    
    # bg = image.load(f"%s/Sprites/Bgs/Bg{lvl}.png" % ICON_DIR)
    pygame.display.set_caption("Mind Leap")

    timer = pygame.time.Clock()

    left = right = up = False
    
    x=y=0
    for line in range(len(levels[lvl])):
        for symbol in range(len(levels[lvl][line])):

            if levels[lvl][line][symbol] == "-": # Платформы
                platform = Block(x,y, "platform")
                entities.add(platform)
                blocks[0].append(platform)
            if levels[lvl][line][symbol] == "b": # Кнопка
                if levels[lvl][line][symbol - 1] == "b":
                    button = Block(x,y, "button", "r")
                else:
                    button = Block(x,y, "button", "l")
                entities.add(button)
                blocks[1].append(button)
            if levels[lvl][line][symbol] == "d": # Главная дверь
                exit_block = Block(x,y,"door", 1)
                entities.add(exit_block)
                blocks[2].append(exit_block)
            if levels[lvl][line][symbol] == "D": # Дверь 1
                if not puz_completed:
                    door = Block(x,y,"door", 2)
                    entities.add(door)
                    blocks[2].append(door)

            if levels[lvl][line][symbol] == "p": # Головоломки
                puz = Object(x,y, "puzzle", lvl)
                entities.add(puz)
                objects[1].append(puz)
                if puz_completed:
                    puz.completed = True 
                    hero = Player(x,y)
                    entities.add(hero)
            if levels[lvl][line][symbol] == "l": # Лампочка
                lamp = Object(x,y, "lamp")
                entities.add(lamp)
                objects[2].append(lamp)
            if levels[lvl][line][symbol] == "e": # Настоящий выход с уровня
                level_exit = Object(x, y, "exit")
                entities.add(level_exit)
                objects[0].append(level_exit)

            elif levels[lvl][line][symbol] == "H":
                if not puz_completed:
                    hero = Player(x,y)
                    entities.add(hero)
            
            if levels[lvl][line][symbol] == "c": # Кубы
                cube = Cube(x,y)
                entities.add(cube)
                blocks[-1].append(cube)
            x += BLOCK_WIDTH # Платформы ставятся на ширине блоков
        y += BLOCK_HEIGHT    # Платформы ставятся на высоте блоков
        x = 0  
    x=y=0    
    
    while running:        
        timer.tick(FPS)
        for e in pygame.event.get(): 
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN: # Клавиша нажата
                if e.key == K_UP or e.key == K_w or e.key == K_SPACE: 
                    up = True
                if (e.key == K_RIGHT or e.key == K_d):
                    right = True
                if (e.key == K_LEFT or e.key == K_a):
                    left = True
                if (e.key == K_BACKSPACE):
                    game(lvl+1)
                    running = 0
                if e.key == K_r:
                    for p in puzzles:
                      p.completed = False
                    game(lvl)
                    running = 0
                if e.key == K_e:
                    for p in puzzles:
                        if hero.rect.collidelistall(puzzles) and not p.completed:
                            p.completed = True
                            if lvl == 1:
                                buts(lvl)
                            elif lvl == 2:
                                mats(lvl)
                            elif lvl == 3:
                                maze(lvl)
                            # print(p.type2)
                            running = 0
            if e.type == KEYUP: # Клавиша не нажата
                if (e.key == K_UP or e.key == K_w or e.key == K_SPACE):
                    up = False
                if (e.key == K_RIGHT or e.key == K_d):
                    right = False
                if (e.key == K_LEFT or e.key == K_a):
                    left = False

        for b in buttons:
            if hero.rect.collidelistall(buttons) or cube.rect.collidelistall(buttons):
                if  cube.rect.collidelistall(buttons):
                    cube.rect.bottom = b.hitbox.top
                b.pressed = True 
                for d in doors:
                    if d.type2 == 1:
                        d.opened = True
            else:
                
                b.pressed = False
                for d in doors:
                    if d.type2 == 1:
                        d.opened = False
            b.button_pressed()

        for p in puzzles:
            if p.completed:
                for d in doors:
                    if d.type2 == 2:
                        d.opened = True

        for d in doors:
            d.door_opened()

        for l in lamps:
            for p in puzzles:
                if not hero.rect.collidelistall(puzzles) and not p.completed:
                    l.touch = False
                else:
                    l.touch = True
            l.light()
        
        if hero.rect.collidelistall(exits):
            if lvl != 3:
                game(lvl+1)
                running = 0
            else:
                mb.showinfo("Mind Leap",f"Игра пройдена!")
                running = 0
    
        screen.blit(bg, (0,0))
        hero.update(left, right, up, blocks)
        cube.update(blocks, hero)
        entities.draw(screen) 
        pygame.display.update() 
        #print(f'FPS={int(timer.get_fps())}')

def buts(lvl = None, puz_level = 0):
    global running
    
    entities = pygame.sprite.Group() # Все объекты
    screen = pygame.display.set_mode(DISPLAY) # Создание окна программы
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Поверхность, являющаяся задним фоном для игры
    pygame.display.update() 
    bg.fill(Color(BACKGROUND_COLOR)) # Цвет заднего фона
    pygame.display.set_caption("Mind Leap")

    timer = pygame.time.Clock()

    # Список цветов кнопок
    colors = ["red", "yellow", "blue", "purple", "green"]
    shuffle(colors) # Пермешивание спичка
    # Посредством данного перемешивания получается 
    # случайная последовательность при каждом новом запуске

    buttons_puzzle = []
    buttons_pressed = 0

    for col in colors:
        button = Button_puzzle(col)
        buttons_puzzle.append(button)
        entities.add(button)

    while running:        
        timer.tick(FPS)
        for e in pygame.event.get(): 
            if e.type == QUIT:
                exit()
            
            if e.type == KEYDOWN:
                if e.key == K_r:
                    buts(lvl)
                    running = 0
                if e.key == K_BACKSPACE:
                    game(lvl, False)
                    running = 0

            
            if e.type == pygame.MOUSEBUTTONDOWN:       
                for b in buttons_puzzle:
                    if b.rect.collidepoint(mouse.get_pos()):
                        if b.color == colors[buttons_pressed]:
                            b.change_color()
                            buttons_pressed += 1
                        else:
                            for but in buttons_puzzle:
                                but.reset()
                            buttons_pressed = 0

        if buttons_pressed == len(buttons_puzzle):
            game(lvl, True)
            running = 0
        
        # print(mouse.get_pos())
        screen.blit(bg, (0,0))
        entities.draw(screen) 
        pygame.display.update() 
        # print(f'FPS={int(timer.get_fps())}')

def maze(lvl):
    global running

    entities = pygame.sprite.Group() # Все объекты
    screen = pygame.display.set_mode(DISPLAY) # Создание окна программы
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Поверхность, являющаяся задним фоном для игры
    pygame.display.update() 
    bg.fill(Color(BACKGROUND_COLOR)) # Цвет заднего фона
    blocks = []
    objects= []
    pygame.display.set_caption("Mind Leap") 

    timer = pygame.time.Clock()

    mouse.set_pos(32 * 4, 32 * 4)

    x=y=0
    for line in level_maze:
        for symbol in line:
            if symbol == "-": # Платформы
                platform = Block(x,y, "platform")
                entities.add(platform)
                blocks.append(platform)
            if symbol == "e": # Настоящий выход с уровня
                level_exit = Object(x, y, "exit")
                entities.add(level_exit)
                objects.append(level_exit)
            x += BLOCK_WIDTH # Платформы ставятся на ширине блоков
        y += BLOCK_HEIGHT    # Платформы ставятся на высоте блоков
        x = 0
    x=y=0

    while running:
        timer.tick(FPS)
        for e in pygame.event.get(): 
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_r:
                    maze(lvl)
                    running = 0
                if e.key == K_BACKSPACE:
                    game(lvl, True)
                    running = 0
            
        mouse_pos = mouse.get_pos()
        for b in blocks:
            if b.rect.collidepoint(mouse_pos):
                mouse.set_pos(32 * 4, 32 * 4)
        for e in objects:
            if e.rect.collidepoint(mouse_pos):
                game(lvl, True)

        screen.blit(bg, (0,0))
        entities.draw(screen) 
        pygame.display.update()
        # print(f'FPS={int(timer.get_fps())}')

def mats(lvl = None, puz_level = 0):
    global running

    entities = pygame.sprite.Group() # Все объекты
    screen = pygame.display.set_mode(DISPLAY) # Создание окна программы
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Поверхность, являющаяся задним фоном для игры
    pygame.display.update() 
    bg.fill(Color(BACKGROUND_COLOR)) # Цвет заднего фона
    pygame.display.set_caption("Mind Leap")

    timer = pygame.time.Clock()

    matches = []
    placeholders = []
    
    held = False
    held_m = None

    k = 1
    while k <= 46:
        for line in levels_matches[puz_level][:-1]:
            for symb in line:
                placeholder = Placeholder(k)
                placeholders.append(placeholder)
                entities.add(placeholder)
                if symb == "1":
                    placeholder.taken = True
                    placeholder.taken_num = k
                    match = Match(k)
                    matches.append(match)
                    entities.add(match)
                    # print(k)
                k += 1
    k = 1            
    while running:        
        timer.tick(FPS)
        for e in pygame.event.get(): 
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_r:
                    mats(lvl, puz_level)
                    running = 0
                if e.key == K_BACKSPACE:
                    game(lvl, False)
                    running = 0
                if e.key == K_f and held:
                    if held_m.orient == "hor":
                        held_m.rotate("vert")
                    else:
                        held_m.rotate("hor")
            
            if k > 0:
                if not held:
                    for m in matches:
                        if m.hitbox.collidepoint(mouse.get_pos()):
                            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                                for p in placeholders:
                                    if p.taken_num == m.num:
                                        p.taken = False 
                                        p.taken_num = None
                                m.held = True
                                held_m = m
                                held = True
                else:
                    for p in placeholders:
                        if p.hitbox.collidepoint(mouse.get_pos()):
                            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                                if not p.taken and (p.orient == held_m.orient):
                                    p.taken = True
                                    p.taken_num = held_m.num
                                    held_m.held = False
                                    held_m.rect.center = p.rect.center
                                    held_m = None
                                    held = False
                                    k -= 1
            elif k == 0:
                print("Для перезапуска нажмите R")
                
            if not placeholders[levels_matches[puz_level][-1][0] - 1].taken and placeholders[levels_matches[puz_level][-1][1] - 1].taken:
                if puz_level != 1:
                    mats(lvl, puz_level + 1)
                else:
                   game(lvl, True)
                running = 0
            

        print(held)

        for m in matches:
            m.update(mouse.get_pos())
        # for p in placeholders:
        #     p.update()

        # print(mouse.get_pos())
        screen.blit(bg, (0,0))
        entities.draw(screen) 
        pygame.display.update() 
        # print(f'FPS={int(timer.get_fps())}')

game(0)
# buts(1)
# maze(3)
# mats(2)