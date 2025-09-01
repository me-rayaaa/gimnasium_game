import random

import pygame
from PIL import Image

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пиксельная игра с препятствиями")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (34, 45, 90)

# Максимальное количество препятствий
MAX_OBSTACLES = 4


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пиксельная игра с препятствиями")


# Загрузка изображений
background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

game_over_img = pygame.image.load('game_over.gif')
game_over_img = pygame.transform.scale(game_over_img, (250, 250))


player_imgs = [
    pygame.image.load('player1.gif'),
    pygame.image.load('player2.gif'),
    pygame.image.load('player3.gif'),
    pygame.image.load('player4.png')

]
obstacle_imgs = [
    pygame.image.load('obstacle1.png')
]
bonus_imgs = [
    pygame.image.load('bonus1.png'),
    pygame.image.load('bonus2.png')
]

# Масштабирование изображений
player_size = 150
for i in range(len(player_imgs)):
    player_imgs[i] = pygame.transform.scale(player_imgs[i], (player_size, player_size))

obstacle_size = player_size
for i in range(len(obstacle_imgs)):
    obstacle_imgs[i] = pygame.transform.scale(obstacle_imgs[i], (obstacle_size//2, obstacle_size//2))

bonus_size = int(player_size)
for i in range(len(bonus_imgs)):
    bonus_imgs[i] = pygame.transform.scale(bonus_imgs[i], (bonus_size//2, bonus_size//2))

# Шрифты
font = pygame.font.Font('pixy.ttf', 36)
big_font = pygame.font.Font('pixy.ttf', 72)


# Функция для отображения текста
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Функция для выбора персонажа
def choose_character():
    choosing = True
    selected = 0
    while choosing:
        screen.blit(background_img, (0, 0))
        draw_text("Выберите персонажа", big_font, BLUE, WIDTH // 2, 100)

        for i, img in enumerate(player_imgs):
            screen.blit(img, (WIDTH // 2 - player_size * 1.5 + i * player_size, HEIGHT // 2 - player_size // 2))
            if i == selected:
                pygame.draw.rect(screen, RED, (WIDTH // 2 - player_size * 1.5 + i * player_size - 5,
                                               HEIGHT // 2 - player_size // 2 - 5,
                                               player_size + 10, player_size + 10), 5)

        draw_text("Нажмите ПРОБЕЛ для выбора", font, BLUE, WIDTH // 2, HEIGHT - 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(player_imgs)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(player_imgs)
                elif event.key == pygame.K_SPACE:
                    return player_imgs[selected]

    return None


def choose_location():
    locations = [
        {"name": "Актовый зал", "image": pygame.image.load('location1.png')},
        {"name": "Парадная", "image": pygame.image.load('background.png')},
        {"name": "Коридор", "image": pygame.image.load('location2.png')}
    ]

    choosing = True
    selected = 0
    while choosing:
        screen.blit(background_img, (0, 0))
        draw_text("Выберите локацию", big_font, BLUE, WIDTH // 2, 100)

        for i, loc in enumerate(locations):
            img = pygame.transform.scale(loc["image"], (200, 150))
            screen.blit(img, (WIDTH // 2 - 300 + i * 250, HEIGHT // 2 - 75))
            if i == selected:
                pygame.draw.rect(screen, RED, (WIDTH // 2 - 305 + i * 250,
                                               HEIGHT // 2 - 80,
                                               210, 160), 5)
            draw_text(loc["name"], font, BLUE, WIDTH // 2 - 200 + i * 250, HEIGHT // 2 + 100)

        draw_text("Нажмите ПРОБЕЛ для выбора", font, BLUE, WIDTH // 2, HEIGHT - 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(locations)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(locations)
                elif event.key == pygame.K_SPACE:
                    return locations[selected]

    return None


# Функция для отображения кнопки начала игры
def show_start_game_button():
    button_width, button_height = 200, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT - 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    pygame.draw.rect(screen, RED, button_rect)
    draw_text("Start", font, WHITE, WIDTH // 2, HEIGHT - 75)

    return button_rect

# Класс для препятствий и бонусов
class GameObject:
    def __init__(self, x, y, img):
        self.rect = pygame.Rect(x, y, img.get_width(), img.get_height())
        self.img = img


# Основная функция игры
def game(player_img, location):
    # Игрок
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    player_speed = 5
    background_img = location["image"]
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    # Препятствия и бонусы
    obstacle_speed = 3
    obstacles = []
    bonuses = []
    max_obstacles = 2  # Максимальное количество препятствий на экране

    # Счет и уровень
    score = 0
    level = 1

    # Время
    start_time = pygame.time.get_ticks()

    # Функция для создания нового препятствия
    def create_obstacle():
        if len(obstacles) < max_obstacles:
            x = random.randint(0, WIDTH - obstacle_size)
            y = -obstacle_size
            img = random.choice(obstacle_imgs)
            obstacles.append(GameObject(x, y, img))

    # Функция для создания нового бонуса
    def create_bonus():
        x = random.randint(0, WIDTH - bonus_size)
        y = -bonus_size
        img = random.choice(bonus_imgs)
        bonuses.append(GameObject(x, y, img))

    # Игровой цикл
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed


        # Создание новых препятствий и бонусов
        if random.randint(1, 60) == 1 and len(obstacles) < max_obstacles:
            create_obstacle()
        if random.randint(1, 180) == 1:
            create_bonus()


        # Увеличение скорости со временем
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # в секундах
        obstacle_speed = 3 + (elapsed_time // 10) * 0.5  # Увеличение скорости на 0.5 каждые 10 секунд

        # Движение препятствий и бонусов
        for obj in obstacles[:]:
            obj.rect.y += obstacle_speed
            if obj.rect.top > HEIGHT:
                obstacles.remove(obj)
                score += 5  # Добавляем 5 очков за каждое пропущенное препятствие

        for obj in bonuses[:]:
            obj.rect.y += obstacle_speed
            if obj.rect.top > HEIGHT:
                bonuses.remove(obj)

        # Проверка столкновений
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for obj in obstacles:
            if player_rect.colliderect(obj.rect):
                return score

        for obj in bonuses[:]:
            if player_rect.colliderect(obj.rect):
                bonuses.remove(obj)
                score += random.randint(5, 25)  # Добавляем случайное количество очков от 10 до 20

        # Проверка уровня
        if score >= 100 * level:
            level += 1
            obstacle_speed += 1  # Увеличиваем скорость при переходе на новый уровень

        # Отрисовка
        screen.blit(background_img, (0, 0))
        screen.blit(player_img, (player_x, player_y))
        for obj in obstacles:
            screen.blit(obj.img, obj.rect)
        for obj in bonuses:
            screen.blit(obj.img, obj.rect)

        # Отображение счета и уровня
        draw_text(f"Счет: {score}", font, BLACK, 70, 20)
        draw_text(f"Уровень: {level}", font, BLACK, 70, 60)

        pygame.display.flip()
        clock.tick(60)


def music_selection_screen():
    music_list = [
        {"name": "Forgotten feelings", "path": "song1.mp3"},
        {"name": "Night aesthetics", "path": "song2.mp3"},
        {"name": "Lost Angeles", "path": "song3.mp3"},
    ]

    button_width, button_height = 150, 30
    back_button = pygame.Rect(10, 10, button_width, button_height)

    selected_song = None
    waiting = True
    while waiting:
        screen.fill(WHITE)
        draw_text("Выберите музыку", big_font, BLUE, WIDTH // 2, 50)

        for i, song in enumerate(music_list):
            y = 150 + i * 50
            draw_text(song["name"], font, BLACK, WIDTH // 2 - 100, y)
            play_button = pygame.Rect(WIDTH // 2 + 100, y - 15, button_width, button_height)
            pygame.draw.rect(screen, RED, play_button)
            draw_text("Играть", font, WHITE, WIDTH // 2 + 175, y)

        pygame.draw.rect(screen, BLUE, back_button)
        draw_text("Назад", font, WHITE, 85, 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    waiting = False
                for i, song in enumerate(music_list):
                    play_button = pygame.Rect(WIDTH // 2 + 100, 150 + i * 50 - 15, button_width, button_height)
                    if play_button.collidepoint(event.pos):
                        selected_song = song["path"]
                        waiting = False

        pygame.display.flip()

    return selected_song


def load_gif(filename):
    gif = Image.open(filename)
    frames = []
    try:
        while True:
            frame = gif.copy()
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            pygame_image = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

game_over_frames = load_gif('game_over.gif')

facts = [
    "Первым директором гимназии стал Сергей Павлович Моравский.",
    "Заведение было основано в сентябре 1910 года на деньги петербуржского купца \t А.Л.Кекина.",
    "В 1912 году в гимназии была обустроена астрономическая обсерватория.",
    "Алексей Леонтьевич Кекин был известным благотворителем Ростова.",
    "На сегодняшний день в нашей школе проводятся экскурсии.",
]


def show_fact():
    fact = random.choice(facts)
    fact_surface = pygame.Surface((WIDTH - 100, 200))
    fact_surface.fill(WHITE)
    pygame.draw.rect(fact_surface, BLACK, fact_surface.get_rect(), 3)

    words = fact.split()
    lines = []
    current_line = []
    for word in words:
        if font.size(' '.join(current_line + [word]))[0] <= WIDTH - 150:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))

    y = 20
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        fact_surface.blit(text_surface, ((WIDTH - 100 - text_surface.get_width()) // 2, y))
        y += 40

    screen.blit(fact_surface, (50, (HEIGHT - 200) // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False


def start_screen():
    start_img = pygame.image.load('start_background.png')
    start_img = pygame.transform.scale(start_img, (WIDTH, HEIGHT))

    button_width, button_height = 300, 50
    button_x = WIDTH - button_width - 300
    button_y = HEIGHT // 2 - button_height // 2

    start_button = pygame.Rect(button_x, button_y, button_width, button_height)
    music_button = pygame.Rect(button_x, button_y + button_height + 20, button_width, button_height)
    fact_button = pygame.Rect(button_x, button_y + 2 * (button_height + 20), button_width, button_height)

    waiting = True
    selected_music = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False
                elif music_button.collidepoint(event.pos):
                    selected_music = music_selection_screen()
                elif fact_button.collidepoint(event.pos):
                    show_fact()

        screen.blit(start_img, (0, 0))
        pygame.draw.rect(screen, RED, start_button)
        draw_text("Start", font, WHITE, button_x + button_width // 2, button_y + button_height // 2)

        pygame.draw.rect(screen, BLUE, music_button)
        draw_text("Выбрать музыку", font, WHITE, button_x + button_width // 2, button_y + button_height * 1.5 + 20)

        pygame.draw.rect(screen, YELLOW, fact_button)
        draw_text("Факт", font, BLACK, button_x + button_width // 2, button_y + button_height * 2.5 + 40)

        pygame.display.flip()

    return selected_music

# Основной цикл программы

# Основной цикл программы
while True:
    selected_music = start_screen()
    player_img = choose_character()
    if player_img is None:
        break

    location = choose_location()
    if location is None:
        break

    # Отображение экрана с кнопкой начала игры
    waiting_for_start = True
    while waiting_for_start:
        screen.blit(background_img, (0, 0))
        screen.blit(player_img, (WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2))
        start_button = show_start_game_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting_for_start = False

    if selected_music:
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.play(-1)

    final_score = game(player_img, location)
    if final_score is None:
        break

    pygame.mixer.music.stop()

    # Отображение экрана Game Over
    screen.fill(BLACK)

    # Инициализация для анимации GIF
    frame_index = 0
    frame_count = len(game_over_frames)
    last_frame_time = pygame.time.get_ticks()
    frame_duration = 100  # Длительность каждого кадра в миллисекундах

    # Отображение анимации Game Over и ожидание нажатия клавиши
    waiting = True
    while waiting:
        current_time = pygame.time.get_ticks()

        if current_time - last_frame_time > frame_duration:
            frame_index = (frame_index + 1) % frame_count
            last_frame_time = current_time

        screen.fill(BLACK)

        # Отображение текущего кадра GIF
        current_frame = game_over_frames[frame_index]
        frame_rect = current_frame.get_rect()
        frame_rect.center = (WIDTH // 2, HEIGHT // 2 - 150)
        screen.blit(current_frame, frame_rect)

        draw_text("GAME OVER", big_font, RED, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(f"Финальный счет: {final_score}", font, YELLOW, WIDTH // 2, HEIGHT // 2 + 120)
        draw_text("Нажмите любую клавишу для продолжения", font, WHITE, WIDTH // 2, HEIGHT - 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


    # Ожидание нажатия клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Завершение игры
pygame.quit()
