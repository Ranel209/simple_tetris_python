import pygame
from copy import deepcopy
from random import choice, randrange

<<<<<<< HEAD
# Creating the game window
width, height = 10, 15  
tile = 45  
game_res = width * tile, height * tile  
res = 750, 940  
FPS = 60

pygame.init()
sc = pygame.display.set_mode(res)
game_sc = pygame.Surface(game_res)
clock = pygame.time.Clock()

# Creating the grid structure
grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(width) for y in range(height)]

# Tetris figures positions
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
field = [[0 for _ in range(width)] for _ in range(height)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

# Colors
bg_color = (0, 0, 0)
game_bg_color = (40, 40, 40)

# Fonts
main_font = pygame.font.Font(None, 65)
font = pygame.font.Font(None, 45)

# Titles
title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

# Random color generator
get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > width - 1:
        return False
    elif figure[i].y > height - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


def game_over_screen():
    """Display the game over screen with options to retry or exit."""
    while True:
        sc.fill(bg_color)
        game_over_text = main_font.render("GAME OVER", True, pygame.Color('red'))
        retry_text = font.render("Press R to Retry", True, pygame.Color('white'))
        exit_text = font.render("Press ESC to Exit", True, pygame.Color('white'))

        # Display texts
        sc.blit(game_over_text, (res[0] // 2 - game_over_text.get_width() // 2, 300))
        sc.blit(retry_text, (res[0] // 2 - retry_text.get_width() // 2, 450))
        sc.blit(exit_text, (res[0] // 2 - exit_text.get_width() // 2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Retry
                    return True
                elif event.key == pygame.K_ESCAPE:  # Exit
                    pygame.quit()
                    exit()


while True:
    record = get_record()
    dx, rotate = 0, False

    # Fill the main screen and game surface
    sc.fill(bg_color)
    game_sc.fill(game_bg_color)

    # Delay for full lines
    for _ in range(lines):
        pygame.time.wait(200)

    # Player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    # Move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # Move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break

    # Rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # Check lines
    line, lines = height - 1, 0
    for row in range(height - 1, -1, -1):
        count = 0
        for i in range(width):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < width:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Compute score
    score += scores[lines]

    # Draw the grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw the active figure
    for i in range(4):
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        pygame.draw.rect(game_sc, color, figure_rect)

    # Draw the field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * tile, y * tile
                pygame.draw.rect(game_sc, col, figure_rect)

    # Draw the next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * tile + 380
        figure_rect.y = next_figure[i].y * tile + 185
        pygame.draw.rect(sc, next_color, figure_rect)

    # Draw titles and score
    sc.blit(game_sc, (20, 20))
    sc.blit(title_tetris, (485, -10))
    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
    sc.blit(title_record, (525, 650))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 710))

    # Game over check
    for i in range(width):
        if field[0][i]:
            set_record(record, score)
            if not game_over_screen():
                pygame.quit()
                exit()
            field = [[0 for _ in range(width)] for _ in range(height)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            break

    pygame.display.flip()
    clock.tick(FPS)
=======
width, height = 10, 15  # Width and Height of the game grid
tile = 45  # Size of a tile
game_res = width * tile, height * tile  # Game surface resolution
res = 750, 940  # Window resolution
FPS = 60

pygame.init()
sc = pygame.display.set_mode(res)  # Main screen
game_sc = pygame.Surface(game_res)  # Game surface (grid area)
clock = pygame.time.Clock()
>>>>>>> 22a2f6e (game window)
