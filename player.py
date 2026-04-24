from pygame import *
from objects import *

MOVE_SPEED = 6 # Скорость передвижения персонажа
SPEED_ACS = 1.5 # Ускорение персонажа
WIDTH = 32 # Ширина персонажа
HEIGHT = 32 # Высота персонажа
COLOR =  "Orange" # Цвет персонажа
JUMP_POWER = 12 # Сила прыжка персонажа
GRAVITY = 0.5 # Ускорение падения персонажа

# Создание нового класса
class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0 # Скорость перемещения по горизонтали
        self.yvel = 0 # Скорость перемещения по вертикали
        self.onGround = False # Находится ли персонаж на поверхности
        self.image = Surface((WIDTH,HEIGHT)) 
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
       
    def update(self, left, right, up, blocks):
        if self.onGround: # Если персонаж на поверхности
            if up: # При совершении прыжка
                self.yvel = -JUMP_POWER # Персонаж поднимается вверх со скоростью, равной силе прыжка
        if not self.onGround: # Если персонаж не на поверхности
            self.yvel +=  GRAVITY # Перрсонаж движется вниз с ускорением
        if left: # При выполнении движения влево
            while self.xvel > -MOVE_SPEED: # Пока скорость движения персонажа не равна заданной     
                self.xvel -= SPEED_ACS # Персонаж ускоряется
        # Перед остановкой персонаж какое-то время движется по инерции
        elif self.xvel < 0:
            self.xvel += SPEED_ACS
        if right: # При выполнении движения вправо
            while self.xvel < MOVE_SPEED: # Пока скорость движения персонажа не равна заданной 
                self.xvel += SPEED_ACS # Персонаж ускоряется
        # Перед остановкой персонаж какое-то время движется по инерции
        elif self.xvel > 0:
            self.xvel -= SPEED_ACS
        if left and right or not (left or right):
            self.xvel = 0
        self.onGround = False

        self.rect.x += self.xvel
        for b in blocks:
            self.collide(self.xvel, 0, b)

        self.rect.y += self.yvel
        for b in blocks:
            self.collide(0, self.yvel, b)

        
   
    def collide(self, xvel, yvel, blocks):
        for b in blocks:
            if self.rect.colliderect(b.hitbox): # Если персонаж сталкивается с платформой
                if xvel > 0:
                    self.rect.right = b.hitbox.left # Правая сторона персонажа не проходит дальше левой стороны платформы
                    if type(b) == Cube:
                        b.xvel = self.xvel
                if xvel < 0:
                    self.rect.left = b.hitbox.right # Левая сторона персонажа не проходит дальше правой стороны платформы
                    if type(b) == Cube:
                        b.xvel = self.xvel
                if yvel > 0:
                    self.rect.bottom = b.hitbox.top # Нижняя сторона персоанжа не проваливатеся сквозь верхнюю сторону платформы
                    self.onGround = True # Персонаж находится на поверхности
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = b.hitbox.bottom # Верхняя сторона персоанжа не проходит дальше нижней стороны платформы
                    self.yvel = 0


class Cube(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("%s/Sprites/portal_cube.png" % ICON_DIR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.hitbox = self.rect
        self.x = x
        self.y = y
        self.xvel = 0 # Скорость перемещения по горизонтали
        self.yvel = 0 # Скорость перемещения по вертикали
        self.onGround = False # Находится ли куб на поверхности
    
    def update(self, blocks, hero = None):
        if not self.onGround: # Если куб не на поверхности
            self.yvel += GRAVITY # Куб движется вниз с ускорением

        blocks = list(blocks)
        blocks.pop()

        self.onGround = False

        self.rect.x += self.xvel
        for b in blocks:
            self.collide(self.xvel, 0, b, hero)

        self.rect.y += self.yvel
        for b in blocks:
            self.collide(0, self.yvel, b, hero)

        if self.xvel > 0:
            self.xvel -= SPEED_ACS
        if self.xvel < 0:
            self.xvel += SPEED_ACS

    def collide(self, xvel, yvel, blocks, hero):
        for b in blocks:
            if self.rect.colliderect(b.hitbox): # Если персонаж сталкивается с платформой
                if xvel > 0:
                    self.rect.right = b.hitbox.left # Правая сторона персоажа не проходит дальше левой стороны платформы
                if xvel < 0:
                    self.rect.left = b.hitbox.right # Левая сторона персоажа не проходит дальше правой стороны платформы
                if yvel > 0:
                    self.rect.bottom = b.hitbox.top # Нижняя сторона персоажа не проваливатеся сквозь верхню сторону платформы
                    self.onGround = True # Персонаж находися на поверхности
                    self.yvel = 0
    
        # if self.rect.colliderect(hero.rect):
        #     if hero.xvel > 0:
        #         self.rect.left = hero.rect.right # Правая сторона персоажа не проходит дальше левой стороны куба 
        #         self.xvel = hero.xvel #Куб двигается вправо
        #     if hero.xvel < 0:
        #         self.rect.right = hero.rect.left # Левая сторона персоажа не проходит дальше правой стороны куба
        #         self.xvel = hero.xvel #Куб двигается влево 

        # for d in blocks[2]:
        #     if d.opened == False and d.type_door == 2:
        #         if self.rect.colliderect(d.hitbox): # Если персонаж сталкивается с платформой
        #             if xvel > 0:
        #                 self.rect.right = d.hitbox.left # Правая сторона персонажа не проходит дальше левой стороны платформы
        #             if xvel < 0:
        #                 self.rect.left = d.hitbox.right # Левая сторона персонажа не проходит дальше правой стороны платформы
        #             if yvel > 0:
        #                 self.rect.bottom = d.hitbox.top # Нижняя сторона персоанжа не проваливатеся сквозь верхнюю сторону платформы
        #                 self.onGround = True # Персонаж находится на поверхности
        #                 self.yvel = 0
        #             if yvel < 0:
        #                 self.rect.top = d.hitbox.bottom # Верхняя сторона персоанжа не проходит дальше нижней стороны платформы
        #                 self.yvel = 0