import pygame
from pygame import *
import os

BLOCK_WIDTH = 32 # Ширина платформы
BLOCK_HEIGHT = 32 # Высота платформы
BUTTON_SIZE = 200, 200  #Размер кнопки пазла
MATCH_WIDTH = 64
MATCH_HEIGHT = 128
MATCH_SIZE = MATCH_WIDTH, MATCH_HEIGHT
# BLOCK_COLOR = "#121212" # Цвет платформы
BG_COLOR="white" # Цвет заднего фона

ICON_DIR = os.path.dirname(__file__) # Функция модуля os, полный путь к каталогу с файлами

class Block(sprite.Sprite):
    def __init__(self, x, y, type1, type2 = None):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.hitbox = self.rect # хитбокс по умолчанию
        self.type1 = type1 # тип объекта
        self.type2 = type2 # подтип объектка (необязательно)
        if self.type1 == "button": # кнопка
            # хитбокс, при контакте игрока или куба с которым кнопка считается нажатой
            self.hitbox = Rect(x, y + 20, BLOCK_WIDTH, 12)
            self.pressed = False # нажата ли кнопка
            if self.type2 == 1 or self.type2 == 2: # левая и правая часть кнопки
                if self.type2 == 1:
                    self.image = image.load("%s/Sprites/button.png" % ICON_DIR)
                if self.type2 == 2: # спрайт отзеркален по вертикали
                    self.image = pygame.transform.flip(image.load("%s/Sprites/button.png" % ICON_DIR), True, False)
        if self.type1 == "platform": # платформы, по которым передвигается персонаж
            self.image.fill(Color("#121212"))
        if self.type1 == "door": 
            self.opened = False
            if self.type2 == 1:
                self.image = image.load("%s/Sprites/door_button.png" % ICON_DIR)
            if self.type2 == 2:
                self.image = image.load("%s/Sprites/door_bulb.png" % ICON_DIR)

    def door_opened(self):
        if self.type1 == "door":
            if self.opened == True:
                self.image = image.load("%s/Sprites/nothing.png" % ICON_DIR)
                self.hitbox = Rect(0, 0, 0, 0)
            else:
                self.hitbox = self.rect
                if self.type2 == 1:
                    self.image = image.load("%s/Sprites/door_button.png" % ICON_DIR)
                if self.type2 == 2:
                    self.image = image.load("%s/Sprites/door_bulb.png" % ICON_DIR)
        
    def button_pressed(self):
        if self.type1 == "button":
            if self.pressed: # если кнопка нажата
                if self.type2 == "l": # спрайт меняется на соответствующий нажатый вариант для левой и правой части
                    self.image = image.load("%s/Sprites/button_pressed.png" % ICON_DIR)
                elif self.type2 == "r":
                    self.image = pygame.transform.flip(image.load("%s/Sprites/button_pressed.png" % ICON_DIR), True, False)
            else: # иначе спрайт меняется на обычный
                if self.type2 == "l":
                    self.image = image.load("%s/Sprites/button.png" % ICON_DIR)
                elif self.type2 == "r":
                    self.image = pygame.transform.flip(image.load("%s/Sprites/button.png" % ICON_DIR), True, False)
                
class Object(sprite.Sprite):
    def __init__(self, x, y, type1, type2 = None):
        sprite.Sprite.__init__(self)
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.type1 = type1
        self.type2 = type2
        if self.type1 == "puzzle":
            self.image = image.load("%s/Sprites/nothing.png" % ICON_DIR)
            self.completed = False
        if self.type1 == "lamp":
            self.touch = False
            self.image = image.load("%s/Sprites/unlight_bulb.png" % ICON_DIR)
        if self.type1 == "exit":
            self.image.fill(Color("#CA221D"))
    
    def light(self):
        if self.touch:
            self.image = image.load("%s/Sprites/light_bulb.png" % ICON_DIR)
        else:
            self.image = image.load("%s/Sprites/unlight_bulb.png" % ICON_DIR)


class Button_puzzle(sprite.Sprite):
    def __init__(self, color):
        sprite.Sprite.__init__(self)
        self.size = BUTTON_SIZE
        self.color = color
        self.hover = False
        self.change = False
        
        if self.color == "red":
            self.image = image.load("%s/Sprites/Buttons_puzzle/red_on.png" % ICON_DIR)
            self.image_change = image.load("%s/Sprites/Buttons_puzzle/red_off.png" % ICON_DIR)
            self.x = 300
            self.y = 250
        if self.color == "blue":
            self.image = image.load("%s/Sprites/Buttons_puzzle/blue_on.png" % ICON_DIR)
            self.image_change = image.load("%s/Sprites/Buttons_puzzle/blue_off.png" % ICON_DIR)
            self.x = 600
            self.y = 250
        if self.color == "purple":
            self.image = image.load("%s/Sprites/Buttons_puzzle/purple_on.png" % ICON_DIR)
            self.image_change = image.load("%s/Sprites/Buttons_puzzle/purple_off.png" % ICON_DIR)
            self.x = 900
            self.y = 250
        if self.color == "green":
            self.image = image.load("%s/Sprites/Buttons_puzzle/green_on.png" % ICON_DIR)
            self.image_change = image.load("%s/Sprites/Buttons_puzzle/green_off.png" % ICON_DIR)
            self.x = 450
            self.y = 550
        if self.color == "yellow":
            self.image = image.load("%s/Sprites/Buttons_puzzle/yellow_on.png" % ICON_DIR)
            self.image_change = image.load("%s/Sprites/Buttons_puzzle/yellow_off.png" % ICON_DIR)
            self.x = 750
            self.y = 550

        self.original_image = self.image

        self.rect = self.image.get_rect(center=(self.x, self.y))
        # size — (width, height)
        self.image = pygame.transform.scale(self.image, self.size)
        # Обновляем rect, сохраняя центр (или верхний левый)
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        
    def reset(self):
        self.image = self.original_image
        self.image = pygame.transform.scale(self.image, self.size)
        self.change = False
        # return self.change

    def change_color(self):
        self.image = self.image_change
        self.image = pygame.transform.scale(self.image, self.size)

class Match(sprite.Sprite):
    def __init__(self, num):
        sprite.Sprite.__init__(self)
        self.num = num
        self.held = False
        # if self.num >= 1 and self.num <= 39:
        if self.num == 1:
            self.x = -16
            self.y = 160 + 2 * 64
        elif self.num == 2:
            self.x = -16 + 1 * 128
            self.y = 160 + 2 * 64
        elif self.num == 3:
            self.x = -16 + 1 * 128 + 1 * 32
            self.y = 160 + 2 * 64
        elif self.num == 4:
            self.x = -16 + 2 * 128 + 1 * 32
            self.y = 160 + 2 * 64
        elif self.num == 5:
            self.x = -16 + 3 * 128 + 3 * 32
            self.y = 160 + 2 * 64
        elif self.num == 6:
            self.x = -16 + 4 * 128 + 3 * 32
            self.y = 160 + 2 * 64
        elif self.num == 7:
            self.x = -16 + 4 * 128 + 4 * 32
            self.y = 160 + 2 * 64
        elif self.num == 8:
            self.x = -16 + 5 * 128 + 4 * 32
            self.y = 160 + 2 * 64
        elif self.num == 9:
            self.x = -16 + 6 * 128 + 6 * 32
            self.y = 160 + 2 * 64
        elif self.num == 10:
            self.x = -16 + 7 * 128 + 6 * 32
            self.y = 160 + 2 * 64
        elif self.num == 11:
            self.x = -16 + 7 * 128 + 7 * 32
            self.y = 160 + 2 * 64
        elif self.num == 12:
            self.x = -16 + 8 * 128 + 7 * 32
            self.y = 160 + 2 * 64
        elif self.num == 13:
            self.x = -16
            self.y = 160 + 4 * 64
        elif self.num == 14:
            self.x = -16 + 1 * 128
            self.y = 160 + 4 * 64
        elif self.num == 15:
            self.x = -16 + 1 * 128 + 1 * 32
            self.y = 160 + 4 * 64
        elif self.num == 16:
            self.x = -16 + 2 * 128 + 1 * 32
            self.y = 160 + 4 * 64
        elif self.num == 17:
            self.x = -16 + 3 * 128 + 3 * 32
            self.y = 160 + 4 * 64
        elif self.num == 18:
            self.x = -16 + 4 * 128 + 3 * 32
            self.y = 160 + 4 * 64
        elif self.num == 19:
            self.x = -16 + 4 * 128 + 4 * 32
            self.y = 160 + 4 * 64
        elif self.num == 20:
            self.x = -16 + 5 * 128 + 4 * 32
            self.y = 160 + 4 * 64
        elif self.num == 21:
            self.x = -16 + 6 * 128 + 6 * 32
            self.y = 160 + 4 * 64
        elif self.num == 22:
            self.x = -16 + 7 * 128 + 6 * 32
            self.y = 160 + 4 * 64
        elif self.num == 23:
            self.x = -16 + 7 * 128 + 7 * 32
            self.y = 160 + 4 * 64
        elif self.num == 24:
            self.x = -16 + 8 * 128 + 7 * 32
            self.y = 160 + 4 * 64
        elif self.num == 25:
            self.x = -16 + 2 * 128 + 4 * 32
            self.y = 160 + 3 * 64
        elif self.num == 26:
            self.x = 16
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 27:
            self.x = 16 + 1 * 128 + 1 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 28:
            self.x = 16 + 3 * 128 + 3 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 29:
            self.x = 16 + 4 * 128 + 4 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 30:
            self.x = 16 + 6 * 128 + 6 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 31:
            self.x = 16 + 7 * 128 + 7 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 32:
            self.x = 16
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 33:
            self.x = 16 + 1 * 128 + 1 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 34:
            self.x = 16 + 3 * 128 + 3 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 35:
            self.x = 16 + 4 * 128 + 4 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 36:
            self.x = 16 + 6 * 128 + 6 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 37:
            self.x = 16 + 7 * 128 + 7 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 38:
            self.x = 16
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 39:
            self.x = 16 + 1 * 128 + 1 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 40:
            self.x = 16 + 3 * 128 + 3 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 41:
            self.x = 16 + 4 * 128 + 4 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 42:
            self.x = 16 + 6 * 128 + 6 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 43:
            self.x = 16 + 7 * 128 + 7 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 44:
            self.x = 16 + 2 * 128 + 2 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 45:
            self.x = 16 + 5 * 128 + 5 * 32
            self.y = 160 + 3 * 32 + 1 * 128 + 16
        elif self.num == 46:
            self.x = 16 + 5 * 128 + 5 * 32
            self.y = 160 + 3 * 32 + 1 * 128 - 16
        if 1 <= self.num <= 25:
            self.orient = "vert"
            self.image = image.load("%s/Sprites/match.png" % ICON_DIR)
            self.size = (MATCH_WIDTH, MATCH_HEIGHT)
            self.hitbox = Rect(self.x + 24, self.y + 8, 16, 112)
        else:
            self.orient = "hor"
            self.image = pygame.transform.rotate(image.load("%s/Sprites/match.png" % ICON_DIR), 90)
            self.size = (MATCH_HEIGHT, MATCH_WIDTH)
            self.hitbox = Rect(self.x + 8, self.y + 24, 112, 16)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # self.image.fill(Color("blue"))
    # def update(self, mouse_pos):
    #     if self.held == True:
    #         self.rect.center = mouse_pos
    
    def update(self, mouse_pos):
        if self.held:
            # if 1 <= self.num <= 25:
            #     self.image = pygame.transform.scale(image.load("%s/Sprites/match_held.png" % ICON_DIR), self.size)
            # else:
            #     self.image = pygame.transform.scale(pygame.transform.rotate(image.load("%s/Sprites/match_held.png" % ICON_DIR), 90), self.size)
            self.rect.center = mouse_pos
        # else:
        #     if 1 <= self.num <= 25:
        #         self.image = pygame.transform.scale(image.load("%s/Sprites/match.png" % ICON_DIR), self.size)
        #     else:
        #         self.image = pygame.transform.scale(pygame.transform.rotate(image.load("%s/Sprites/match.png" % ICON_DIR), 90), self.size)
        self.hitbox.center = self.rect.center 
    
    def rotate(self, orient):
        if orient == "vert":
            self.orient = "vert"
            self.image = image.load("%s/Sprites/match.png" % ICON_DIR)
            self.size = (MATCH_WIDTH, MATCH_HEIGHT)
            self.hitbox = Rect(self.x + 24, self.y + 8, 16, 112)
        elif orient == "hor":
            self.orient = "hor"
            self.image = pygame.transform.rotate(image.load("%s/Sprites/match.png" % ICON_DIR), 90)
            self.size = (MATCH_HEIGHT, MATCH_WIDTH)
            self.hitbox = Rect(self.x + 8, self.y + 24, 112, 16)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Placeholder(sprite.Sprite):
    def __init__(self, num, taken = None):
        sprite.Sprite.__init__(self)
        self.num = num
        self.taken = taken
        self.taken_num = None
        # if self.num >= 1 and self.num <= 39:
        if self.num == 1:
            self.x = -16
            self.y = 160 + 2 * 64
        elif self.num == 2:
            self.x = -16 + 1 * 128
            self.y = 160 + 2 * 64
        elif self.num == 3:
            self.x = -16 + 1 * 128 + 1 * 32
            self.y = 160 + 2 * 64
        elif self.num == 4:
            self.x = -16 + 2 * 128 + 1 * 32
            self.y = 160 + 2 * 64
        elif self.num == 5:
            self.x = -16 + 3 * 128 + 3 * 32
            self.y = 160 + 2 * 64
        elif self.num == 6:
            self.x = -16 + 4 * 128 + 3 * 32
            self.y = 160 + 2 * 64
        elif self.num == 7:
            self.x = -16 + 4 * 128 + 4 * 32
            self.y = 160 + 2 * 64
        elif self.num == 8:
            self.x = -16 + 5 * 128 + 4 * 32
            self.y = 160 + 2 * 64
        elif self.num == 9:
            self.x = -16 + 6 * 128 + 6 * 32
            self.y = 160 + 2 * 64
        elif self.num == 10:
            self.x = -16 + 7 * 128 + 6 * 32
            self.y = 160 + 2 * 64
        elif self.num == 11:
            self.x = -16 + 7 * 128 + 7 * 32
            self.y = 160 + 2 * 64
        elif self.num == 12:
            self.x = -16 + 8 * 128 + 7 * 32
            self.y = 160 + 2 * 64
        elif self.num == 13:
            self.x = -16
            self.y = 160 + 4 * 64
        elif self.num == 14:
            self.x = -16 + 1 * 128
            self.y = 160 + 4 * 64
        elif self.num == 15:
            self.x = -16 + 1 * 128 + 1 * 32
            self.y = 160 + 4 * 64
        elif self.num == 16:
            self.x = -16 + 2 * 128 + 1 * 32
            self.y = 160 + 4 * 64
        elif self.num == 17:
            self.x = -16 + 3 * 128 + 3 * 32
            self.y = 160 + 4 * 64
        elif self.num == 18:
            self.x = -16 + 4 * 128 + 3 * 32
            self.y = 160 + 4 * 64
        elif self.num == 19:
            self.x = -16 + 4 * 128 + 4 * 32
            self.y = 160 + 4 * 64
        elif self.num == 20:
            self.x = -16 + 5 * 128 + 4 * 32
            self.y = 160 + 4 * 64
        elif self.num == 21:
            self.x = -16 + 6 * 128 + 6 * 32
            self.y = 160 + 4 * 64
        elif self.num == 22:
            self.x = -16 + 7 * 128 + 6 * 32
            self.y = 160 + 4 * 64
        elif self.num == 23:
            self.x = -16 + 7 * 128 + 7 * 32
            self.y = 160 + 4 * 64
        elif self.num == 24:
            self.x = -16 + 8 * 128 + 7 * 32
            self.y = 160 + 4 * 64
        elif self.num == 25:
            self.x = -16 + 2 * 128 + 4 * 32
            self.y = 160 + 3 * 64
        elif self.num == 26:
            self.x = 16
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 27:
            self.x = 16 + 1 * 128 + 1 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 28:
            self.x = 16 + 3 * 128 + 3 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 29:
            self.x = 16 + 4 * 128 + 4 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 30:
            self.x = 16 + 6 * 128 + 6 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 31:
            self.x = 16 + 7 * 128 + 7 * 32
            self.y = 160 + 3 * 32 + 0 * 128
        elif self.num == 32:
            self.x = 16
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 33:
            self.x = 16 + 1 * 128 + 1 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 34:
            self.x = 16 + 3 * 128 + 3 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 35:
            self.x = 16 + 4 * 128 + 4 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 36:
            self.x = 16 + 6 * 128 + 6 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 37:
            self.x = 16 + 7 * 128 + 7 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 38:
            self.x = 16
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 39:
            self.x = 16 + 1 * 128 + 1 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 40:
            self.x = 16 + 3 * 128 + 3 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 41:
            self.x = 16 + 4 * 128 + 4 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 42:
            self.x = 16 + 6 * 128 + 6 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 43:
            self.x = 16 + 7 * 128 + 7 * 32
            self.y = 160 + 3 * 32 + 2 * 128
        elif self.num == 44:
            self.x = 16 + 2 * 128 + 2 * 32
            self.y = 160 + 3 * 32 + 1 * 128
        elif self.num == 45:
            self.x = 16 + 5 * 128 + 5 * 32
            self.y = 160 + 3 * 32 + 1 * 128 + 16
        elif self.num == 46:
            self.x = 16 + 5 * 128 + 5 * 32
            self.y = 160 + 3 * 32 + 1 * 128 - 16
        if 1 <= self.num <= 25:
            self.orient = "vert"
            self.image = image.load("%s/Sprites/match.png" % ICON_DIR)
            self.size = (MATCH_WIDTH, MATCH_HEIGHT)
            self.hitbox = Rect(self.x + 24, self.y + 8, 16, 112)
        else:
            self.orient = "hor"
            self.image = pygame.transform.rotate(image.load("%s/Sprites/match.png" % ICON_DIR), 90)
            self.size = (MATCH_HEIGHT, MATCH_WIDTH)
            self.hitbox = Rect(self.x + 8, self.y + 24, 112, 16)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.image.set_alpha(30)
    # def update(self):
    #     if self.taken:
    #         if 1 <= self.num <= 25:
    #             self.image = pygame.transform.scale(image.load("%s/Sprites/match.png" % ICON_DIR), self.size)
    #         else:
    #             self.image = pygame.transform.scale(pygame.transform.rotate(image.load("%s/Sprites/match.png" % ICON_DIR), 90), self.size)
    #     else:
    #         if 1 <= self.num <= 25:
    #             self.image = pygame.transform.scale(image.load("%s/Sprites/match_g.png" % ICON_DIR), self.size)
    #         else:
    #             self.image = pygame.transform.scale(pygame.transform.rotate(image.load("%s/Sprites/match_g.png" % ICON_DIR), 90), self.size)
    #     self.image.set_alpha(50)
