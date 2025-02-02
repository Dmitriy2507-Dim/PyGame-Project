
import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра Pygame")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Шрифт
font = pygame.font.Font(None, 36)

# Общие переменные
current_screen = 0  # 0 - приветствие, 1 - игра, 2 - победа, 3 - проигрыш
user_score = 0
computer_score = 0
level = 1
game_state = "playing"  # "playing", "game_over", "game_win"


# Кнопка
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
# Изменен размер кнопки, для фразы "Играть снова"
restart_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 200, 50)
# Изменено положение кнопки "Выйти", она теперь находится ровно под "Играть снова"
exit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 120, 200, 50)

# Прямоугольники
user_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 20)
computer_rect = pygame.Rect(WIDTH // 2 - 50, 30, 100, 20)

# Исходные позиции прямоугольников
initial_user_rect_x = WIDTH // 2 - 50
initial_user_rect_y = HEIGHT - 50
initial_computer_rect_x = WIDTH // 2 - 50
initial_computer_rect_y = 30

# Скорость верхнего прямоугольника
computer_rect_speed = 4

# Квадрат
square_size = 20
square_rect = pygame.Rect(WIDTH // 2 - square_size // 2, HEIGHT // 2 - square_size // 2, square_size, square_size)

# Исходные скорости квадрата
initial_square_speed_x = 3
initial_square_speed_y = 3
square_speed_x = initial_square_speed_x
square_speed_y = initial_square_speed_y


# Эффект рассыпания
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = 20  # Количество кадров жизни частицы

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size))


particles = []


def create_particles(x, y):
    for _ in range(30):  # Создаем 30 частиц для эффекта
        particles.append(Particle(x, y))


def welcome_screen():
    """Отрисовка приветственного экрана."""
    screen.fill(BLACK)
    text = font.render("Добро пожаловать!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, WHITE, button_rect)
    button_text = font.render("Играть", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    pygame.display.flip()


def game_screen():
    """Отрисовка игрового экрана и логика игры."""
    global computer_rect_speed, square_speed_x, square_speed_y, user_score, computer_score
    global initial_square_speed_x, initial_square_speed_y
    global initial_user_rect_x, initial_user_rect_y, initial_computer_rect_x, initial_computer_rect_y, particles, current_screen, game_state
    
    # Обработка управления нижним прямоугольником
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        user_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        user_rect.x += 5
    # Границы для управляемого прямоугольника
    if user_rect.left < 0:
        user_rect.left = 0
    if user_rect.right > WIDTH:
        user_rect.right = WIDTH

    # Очистка экрана
    screen.fill(BLACK)

    # Движение верхнего прямоугольника (теперь подстраивается под квадрат)
    if square_rect.centerx < computer_rect.centerx:
        computer_rect.x -= computer_rect_speed
    elif square_rect.centerx > computer_rect.centerx:
        computer_rect.x += computer_rect_speed

    # Ограничение движения верхнего прямоугольника
    if computer_rect.left < 0:
        computer_rect.left = 0
    if computer_rect.right > WIDTH:
        computer_rect.right = WIDTH

    # Движение квадрата
    square_rect.x += square_speed_x
    square_rect.y += square_speed_y

    # Обработка столкновений квадрата со стенами и создание частиц
    if square_rect.left < 0:
        create_particles(square_rect.left, square_rect.centery)
        square_speed_x *= -1
    elif square_rect.right > WIDTH:
        create_particles(square_rect.right, square_rect.centery)
        square_speed_x *= -1

    # Обработка столкновений с прямоугольниками - отскок и ускорение
    if square_rect.colliderect(user_rect) or square_rect.colliderect(computer_rect):
        square_speed_y *= -1
        square_speed_x *= 1.1  # Уменьшено ускорение, чтобы не вылетало за границы
        square_speed_y *= 1.1

    # Выход за границы (считаем очки и сбрасываем скорость)
    if square_rect.top > HEIGHT:
        computer_score += 1
        square_rect.center = (WIDTH // 2, HEIGHT // 2)
        square_speed_x = random.choice([-initial_square_speed_x, initial_square_speed_x])
        square_speed_y = -initial_square_speed_y
        # Возвращение прямоугольников в исходные позиции
        user_rect.x = initial_user_rect_x
        user_rect.y = initial_user_rect_y
        computer_rect.x = initial_computer_rect_x
        computer_rect.y = initial_computer_rect_y

    if square_rect.bottom < 0:
        user_score += 1
        square_rect.center = (WIDTH // 2, HEIGHT // 2)
        square_speed_x = random.choice([-initial_square_speed_x, initial_square_speed_x])
        square_speed_y = initial_square_speed_y
        # Возвращение прямоугольников в исходные позиции
        user_rect.x = initial_user_rect_x
        user_rect.y = initial_user_rect_y
        computer_rect.x = initial_computer_rect_x
        computer_rect.y = initial_computer_rect_y

    # Обновление и отрисовка частиц
    particles_to_remove = []
    for p in particles:
        p.update()
        p.draw(screen)
        if p.lifetime <= 0:
            particles_to_remove.append(p)
    for p in particles_to_remove:
        particles.remove(p)

    # Отрисовка объектов
    pygame.draw.rect(screen, RED, user_rect)
    pygame.draw.rect(screen, BLUE, computer_rect)
    pygame.draw.rect(screen, WHITE, square_rect)

    # Отрисовка счета
    score_text = font.render(f"User: {user_score}  |  Computer: {computer_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Проверка счета и переключение на новый экран
    if user_score == 3:
         game_state = "game_win"
    elif computer_score == 3:
        game_state = "game_over"

def game_end_screen():
    """Отображение экрана окончания игры и обработка выбора."""
    global game_state, level, user_score, computer_score, current_screen
    screen.fill(BLACK)
    if game_state == "game_over":
        text = font.render(f"Game Over! Level: {level}, User Score: {user_score}, Computer Score: {computer_score}", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)
        options = ["Играть снова", "Закрыть игру"]
    elif game_state == "game_win":
        text = font.render(f"You Win! Level: {level}, User Score: {user_score}, Computer Score: {computer_score}", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)
        options = ["Играть снова", "Следующий уровень", "Закрыть игру"]

    # Создаем кнопки (упрощенно)
    buttons = []
    for i, option in enumerate(options):
        button_text = font.render(option, True, BLACK)
        button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 * (i + 1)))
        pygame.draw.rect(screen, WHITE, button_rect.inflate(20, 10))  # Нарисовали фон кнопки
        screen.blit(button_text, button_rect)
        buttons.append((button_rect, option))  # Сохранили кнопку и опцию

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "close_game"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, option in buttons:
                    if rect.collidepoint(mouse_pos):
                        return option

        pygame.time.Clock().tick(30)

def win_screen():
    """Отрисовка экрана победы."""
    global game_state, current_screen
    chosen_option = game_end_screen()
    if chosen_option == "Играть снова":
        restart_game()
        current_screen = 1
    elif chosen_option == "Следующий уровень":
      start_next_level()
      current_screen = 1
    elif chosen_option == "close_game":
        pygame.quit()
        sys.exit()


def lose_screen():
    """Отрисовка экрана поражения."""
    global game_state, current_screen
    chosen_option = game_end_screen()
    if chosen_option == "Играть снова":
        restart_game()
        current_screen = 1
    elif chosen_option == "close_game":
        pygame.quit()
        sys.exit()

def start_next_level():
    """Увеличение скорости и переход на следующий уровень."""
    global level, square_speed_x, square_speed_y, computer_rect_speed, game_state
    level += 1
    square_speed_x *= 1.2  # Увеличение скорости
    square_speed_y *= 1.2
    computer_rect_speed *= 1.2
    game_state = "playing"  # Переключение в состояние "игра"
    restart_game()


def restart_game():
    """Сброс параметров игры."""
    global user_score, computer_score, square_rect, square_speed_x, square_speed_y, computer_rect, game_state, particles
    global initial_square_speed_x, initial_square_speed_y, initial_computer_rect_x, initial_computer_rect_y
    user_score = 0
    computer_score = 0
    square_rect.x = WIDTH // 2 - square_size // 2
    square_rect.y = HEIGHT // 2 - square_size // 2
    square_speed_x = initial_square_speed_x
    square_speed_y = initial_square_speed_y
    computer_rect.x = initial_computer_rect_x
    computer_rect.y = initial_computer_rect_y
    game_state = "playing"
    particles = []  # Очищаем частицы

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_screen == 0 and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                current_screen = 1
                
    if current_screen == 0:
        welcome_screen()
    elif current_screen == 1:
         if game_state == "playing":
             game_screen()
         elif game_state == "game_over":
             lose_screen()
         elif game_state == "game_win":
            win_screen()

    pygame.time.delay(20)

pygame.quit()
sys.exit()
