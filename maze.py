from pygame import *

WIN_WIDTH = 1280 # Ширина окна
WIN_HEIGHT = 800 # Высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "White" 
FPS = 60
running = True

level_maze = [
       "                                        ",
       "  ------------------------------------  ",
       "  ------------------------------------  ",
       "  --ee   -       -   -    -   -     --  ",
       "  --ee   - -----   - - -    - - --- --  ",
       "  ------ - -   ----- - ---- - - - - --  ",
       "  --     - - - -         -- - - -   --  ",
       "  -- --- - - - ---------  --- - ------  ",
       "  --   --- - - -   -   --           --  ",
       "  ----     - - - -   -  ----------- --  ",
       "  -- ------- --- ------      -    - --  ",
       "  --       -     -    ------ ---- - --  ",
       "  -------- ----- -         -      - --  ",
       "  --       -     -    ---- - - ---- --  ",
       "  -- ------- ------------- - ---    --  ",
       "  --       -     -     --- -     -----  ",
       "  -------- ----- - --- --- -------  --  ",
       "  --             -   -     -     - ---  ",
       "  -- --------------- ----- - ----- ---  ",
       "  --      -        -     - -        --  ",
       "  -- --- -- - ---- ----- - -------- --  ",
       "  --   -    -    -       -          --  ",
       "  ------------------------------------  ",
       "  ------------------------------------  ",
       "                                        " ]

def maze(lvl):
    global running

    entities = pygame.sprite.Group() # Все объекты
    screen = pygame.display.set_mode(DISPLAY) # Создание окна программы
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Поверхность, являющаяся задним фоном для игры
    pygame.display.update() 
    bg.fill(Color(BACKGROUND_COLOR)) # Цвет заднего фона
    blocks = []
    objects= []
    pygame.mouse.set_pos(WIN_WIDTH/2,WIN_HEIGHT/2)

    timer = pygame.time.Clock()

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
        mouse_pos = pygame.mouse.get_pos()
        for b in blocks:
            if b.rect.collidepoint(mouse_pos):
                pygame.mouse.set_pos(WIN_WIDTH/2,WIN_HEIGHT/2)
        for e in objects:
            if e.rect.collidepoint(mouse_pos):
                game(lvl, True)

        screen.blit(bg, (0,0))
        entities.draw(screen) 
        pygame.display.update()