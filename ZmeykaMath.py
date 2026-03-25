import pygame
import random
import time
from pygame import mixer

pygame.init()
mixer.init()

RES = 650  
SIZE = 25   
FPS = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((RES, RES))
pygame.display.set_caption("Змейка с математикой")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont('arial', 24)
font_medium = pygame.font.SysFont('arial', 32)
font_large = pygame.font.SysFont('arial', 60)

math_rules = [
    "Правило 1: При умножении двух отрицательных чисел результат положительный",
    "Правило 2: Отрицательное число + отрицательное число = отрицательное число",
    "Правило 3: Число с большим модулем 'сильнее' при сложении",
    "Правило 4: Вычитание отрицательного числа равносильно сложению",
    "Правило 5: Деление двух отрицательных чисел даёт положительный результат"
]

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = current_line + [word]
        test_surface = font.render(' '.join(test_line), True, BLUE)
        if test_surface.get_width() <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def init_game():
    global snake, snake_dir, apple, score, last_rule_time, show_rule, current_rule, rule_start_time, game_paused
    snake = [(RES // 2, RES // 2)]
    snake_dir = (1, 0)
    apple = (random.randrange(0, RES, SIZE), random.randrange(0, RES, SIZE))
    score = 0
    last_rule_time = time.time()
    show_rule = False
    current_rule = ""
    rule_start_time = 0 
    game_paused = False

init_game()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                game_paused = not game_paused
            elif not game_paused:
                if event.key == pygame.K_UP and snake_dir != (0, 1):
                    snake_dir = (0, -1)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -1):
                    snake_dir = (0, 1)
                elif event.key == pygame.K_LEFT and snake_dir != (1, 0):
                    snake_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                    snake_dir = (1, 0)
            elif game_paused and event.key == pygame.K_SPACE:
                show_rule = False
                rule_start_time = 0

    if game_paused:
        continue

    current_time = time.time()
    if current_time - last_rule_time >= 60: 
        show_rule = True
        current_rule = random.choice(math_rules)
        last_rule_time = current_time
        rule_start_time = current_time

    if show_rule and current_time - rule_start_time >= 20:
        show_rule = False
        rule_start_time = 0

    screen.fill(BLACK)

    if not show_rule:
        new_head = (snake[0][0] + snake_dir[0] * SIZE, snake[0][1] + snake_dir[1] * SIZE)
        snake.insert(0, new_head)

        if snake[0] == apple:
            score += 1
            apple = (random.randrange(0, RES, SIZE), random.randrange(0, RES, SIZE))
            FPS += 0.2
        else:
            snake.pop()

        if (snake[0][0] < 0 or snake[0][0] >= RES or
            snake[0][1] < 0 or snake[0][1] >= RES or
            snake[0] in snake[1:]):
            draw_text("GAME OVER", font_large, RED, RES // 2, RES // 2 - 40)
            draw_text(f"Финальный счёт: {score}", font_medium, WHITE, RES // 2, RES // 2 + 20)
            draw_text("Нажмите G для новой игры", font_small, WHITE, RES // 2, RES // 2 + 70)
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_g:
                            init_game()
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            waiting = False
    else:
        wrapped_lines = wrap_text(current_rule, font_medium, RES - 100) 
        line_height = font_medium.get_linesize()
        start_y = RES // 2 - (len(wrapped_lines) * line_height) // 2

        for i, line in enumerate(wrapped_lines):
            draw_text(line, font_medium, BLUE, RES // 2, start_y + i * line_height)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SIZE - 2, SIZE - 2))

    pygame.draw.rect(screen, RED, (apple[0], apple[1], SIZE, SIZE))

    draw_text(f"Счёт: {score}", font_small, WHITE, 70, 40)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
