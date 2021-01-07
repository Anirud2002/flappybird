import pygame, random

pygame.init()
pygame.display.set_caption("Flappy Bird - Anirud")
pygame.display.set_icon(pygame.image.load("assets/bluebird-midflap.png"))
game_font = pygame.font.Font("04B_19.TTF", 30)
score = 0
high_score = 0
screen = pygame.display.set_mode((376, 624))

clock = pygame.time.Clock()

# game variables
gravity = 0.25
bird_movement = 0

game_active = True

bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (376, 624))

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (376, 100))

floor_x_pos = 0

bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_rect = bird_surface.get_rect(center=(80, 272))

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (60, 400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 350, 400, 470]


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 524))
    screen.blit(floor_surface, (floor_x_pos + 376, 524))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(588, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(588, random_pipe_pos - 150))
    return bottom_pipe, top_pipe  # it returns tuple


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 524:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -10 or bird_rect.bottom >= 524:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def score_display(game_state):
    if game_state == "main_text":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(188, 70))
        screen.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(188, 70))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(88, 470))
        screen.blit(high_score_surface, high_score_rect)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 7
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (80, 200)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display("main_text")
    else:
        score_display("game_over")
        high_score = score

    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -376:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
