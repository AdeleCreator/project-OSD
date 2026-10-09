#pgzero
import pgzrun
import random

WIDTH = 800
HEIGHT = 400

TITLE = "ОСД"
FPS = 60




# =========================
# ОБЪЕКТЫ
# =========================

char1 = Actor('will', (50, 240), size=(80, 90))

# Большой фон (позиция будет выставлена ниже, после расчёта границ)
fon1 = Actor("кке")

chest_x = random.randint(20,fon1.width-20)
chest_y = random.randint(20,fon1.height-20)

chest = Actor("chest1",(chest_x,chest_y))

chests = ["chest2","chest3","chest4"]
chest_open = 0
chest_time = 0

# Враг
enemy1 = Actor('demo', (250, 270), size=(100, 110))

# Game Over
go = Actor('go', size=(800, 400))

game_over = 0
score = 0


type_game = "menu"


# =========================
# МОНЕТКИ
# =========================

monetki = []

for i in range(10):

    x = random.randint(
        150,
        max(150, fon1.width - 150)
    )

    y = random.randint(
        150,
        max(150, fon1.height - 150)
    )

    monetka = Actor(
        'monetka',
        (x, y),
        size=(50, 50)
    )

    monetki.append(monetka)


# =========================
# СКОРОСТЬ
# =========================

speed = 10
enemy_speed = 1


# =========================
# ГРАНИЦЫ ФОНА
# =========================

def get_limits():

    # Максимально фон может сдвинуться вправо
    # (левый край фона совпадает с левым краем экрана)
    right_limit = fon1.width // 2

    # Максимально фон может сдвинуться влево
    # (правый край фона совпадает с правым краем экрана)
    left_limit = WIDTH - fon1.width // 2

    # Максимально фон может сдвинуться вниз
    # (верхний край фона совпадает с верхом экрана)
    bottom_limit = fon1.height // 2

    # Максимально фон может сдвинуться вверх
    # (нижний край фона совпадает с низом экрана)
    top_limit = HEIGHT - fon1.height // 2

    return left_limit, right_limit, top_limit, bottom_limit


# =========================
# СТАРТОВАЯ ПОЗИЦИЯ ФОНА
# =========================

# Ставим фон так, чтобы был виден левый верхний угол мира —
# это гарантированно валидная позиция внутри границ движения
_left_limit, _right_limit, _top_limit, _bottom_limit = get_limits()
fon1.x = _right_limit
fon1.y = _bottom_limit


# =========================
# ДВИЖЕНИЕ МИРА
# =========================

def move_world(dx, dy):

    left_limit, right_limit, top_limit, bottom_limit = get_limits()


    # =========================
    # ДВИЖЕНИЕ ПО X
    # =========================

    if dx != 0:

        new_x = fon1.x + dx

        # Проверяем границы
        if left_limit <= new_x <= right_limit:

            # Двигаем фон
            fon1.x = new_x

            # Двигаем врага вместе с фоном
            enemy1.x += dx

            # Двигаем монетки вместе с фоном
            for monetka in monetki:
                monetka.x += dx
                
            chest.x += dx

    # =========================
    # ДВИЖЕНИЕ ПО Y
    # =========================

    if dy != 0:

        new_y = fon1.y + dy

        # Проверяем границы
        if top_limit <= new_y <= bottom_limit:

            # Двигаем фон
            fon1.y = new_y

            # Двигаем врага вместе с фоном
            enemy1.y += dy

            # Двигаем монетки вместе с фоном
            for monetka in monetki:
                monetka.y += dy

            chest.y += dy

# =========================
# DRAW
# =========================

def draw():
    # Фон
    fon1.draw()
    
    if type_game == "menu": # если мы находимся в меню
        screen.draw.text(
            "НАЧАТЬ",
            center=(400, 200),
            color='green',
            fontsize=50
        )
        screen.draw.text(
            "нажми пробел, что бы начать",
            center=(400, 250),
            color='green',
            fontsize=20
        )
        screen.draw.text(
            "z/x/c смена персонажа",
            center=(400,300),
            color='green',
            fontsize=20
        )

        screen.draw.text(
            "Управление: W, A, S и D",
            center=(400,350),
            color='green',
            fontsize=20
        )
        
        # Игрок
        char1.draw()
    elif type_game == "game": # если мы начали играть
        chest.draw()
        # Монетки
        for monetka in monetki:
            monetka.draw()
        # Враг
        enemy1.draw()
        # Игрок
        char1.draw()
        # Счёт
        screen.draw.text(
            "Монетки: " + str(score),
            center=(100, 30),
            color='white',
            fontsize=30
        )
    elif type_game == "win": # если мы начали играть
        screen.draw.text(
            "You Win!!!",
            center=(400, 200),
            color='yellow',
            fontsize=60
        )

        screen.draw.text(
            "Нажмите Крестик Для Закрытия",
            center=(400,250),
            color='yellow',
            fontsize=50
        )   
    # Game Over
    if game_over == 1:
        go.draw()




# =========================
# UPDATE
# =========================

def update(dt):
    global game_over
    global score
    global type_game
    global chest_open
    global chest_time
    # если мы в меню по нажатию пробела запускаем игру
    if type_game =="menu":
        if keyboard.space:
            type_game = "game"

    if score >=5:
        type_game = "win"
        score = 0
    
    # смена персонажа
    if keyboard.x:
        char1.image = "одди"
    if keyboard.z:
        char1.image = "will"
    if keyboard.c:
        char1.image = "lukas"
         
    # перезапуск уровня
    if keyboard.o:
        type_game = "game"
        char1.pos = (50,240)
        enemy1.x = 250
        enemy1.y = 270
        game_over = 0
        score = 0
    
    # Если Game Over
    if game_over == 1 or type_game == "menu" :
        return

    
    if chest_open == 1:
        if chest.image != 'chest4':
            num = int(chest.image[-1])
            chest.image = 'chest' + str(num+1)
        if chest.image == 'chest4':
            type_game = "win"
    # ==================================================
    # УПРАВЛЕНИЕ ИГРОКОМ
    # ==================================================

    # =========================
    # A — ВЛЕВО
    # =========================

    if keyboard.a:

        if char1.x > char1.width // 2:

            # Пока игрок находится внутри экрана
            char1.x -= speed

        else:

            # Игрок упёрся в левую сторону
            # Начинаем двигать мир
            move_world(speed, 0)


    # =========================
    # D — ВПРАВО
    # =========================

    if keyboard.d:

        if char1.x < WIDTH - char1.width // 2:

            # Пока игрок находится внутри экрана
            char1.x += speed

        else:

            # Игрок упёрся в правую сторону
            move_world(-speed, 0)


    # =========================
    # W — ВВЕРХ
    # =========================

    if keyboard.w:

        if char1.y > char1.height // 2:

            # Игрок идёт вверх
            char1.y -= speed

        else:

            # Игрок упёрся в верхнюю часть экрана
            # Двигаем мир вниз
            move_world(0, speed)


    # =========================
    # S — ВНИЗ
    # =========================

    if keyboard.s:

        if char1.y < HEIGHT - char1.height // 2:

            # Игрок идёт вниз
            char1.y += speed

        else:
            # Игрок упёрся в нижнюю часть экрана
            # Двигаем мир вверх
            move_world(0, -speed)

    # ==================================================
    # ВРАГ ИДЁТ К ИГРОКУ
    # ==================================================

    if enemy1.x < char1.x:
        enemy1.x += enemy_speed
    elif enemy1.x > char1.x:
        enemy1.x -= enemy_speed

    if enemy1.y < char1.y:
        enemy1.y += enemy_speed
    elif enemy1.y > char1.y:
        enemy1.y -= enemy_speed

    # ==================================================
    # СБОР МОНЕТОК
    # ==================================================
    collected = []
    for monetka in monetki:
        if char1.colliderect(monetka):
            collected.append(monetka)
            score += 1

    # Удаляем собранные монетки
    for monetka in collected:
        if monetka in monetki:
            monetki.remove(monetka)

    # ==================================================
    # СТОЛКНОВЕНИЕ С ВРАГОМ
    # ==================================================
    #if char1.colliderect(enemy1) and type_game == "game":
       # game_over = 1
      #  return
    if char1.colliderect(chest):
        chest_open = 1
pgzrun.go()