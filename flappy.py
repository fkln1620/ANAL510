# prompt: use pygame to create a flappy bird game and make it a bit easier to play, also use an actual bird and pipes

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Load images
bird_image = pygame.image.load("bird.png") # Replace with your bird image
bird_image = pygame.transform.scale(bird_image, (50, 50))
pipe_image = pygame.image.load("pipe.png") #Replace with your pipe image
pipe_image = pygame.transform.scale(pipe_image, (70, 300))


# Bird properties
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_x = WIDTH
pipe_y = random.randint(100, HEIGHT - pipe_gap - 100)  # Adjust for easier game

# Game variables
score = 0
game_over = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


def draw_bird():
    screen.blit(bird_image, (bird_x, bird_y))


def draw_pipes():
    screen.blit(pipe_image, (pipe_x, pipe_y - pipe_image.get_height())) #top pipe
    screen.blit(pygame.transform.flip(pipe_image, False, True), (pipe_x, pipe_y + pipe_gap)) # bottom pipe



def check_collision():
    global game_over
    bird_rect = bird_image.get_rect(topleft=(bird_x, bird_y))
    top_pipe_rect = pipe_image.get_rect(topleft=(pipe_x, pipe_y - pipe_image.get_height()))
    bottom_pipe_rect = pipe_image.get_rect(topleft=(pipe_x, pipe_y + pipe_gap))
    if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect) or bird_y + bird_image.get_height() > HEIGHT or bird_y < 0:
        game_over = True

def reset_game():
  global bird_y, bird_velocity, pipe_x, pipe_y, score, game_over
  bird_y = HEIGHT // 2
  bird_velocity = 0
  pipe_x = WIDTH
  pipe_y = random.randint(100, HEIGHT - pipe_gap - 100)
  score = 0
  game_over = False



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
              bird_velocity = jump_strength
            if event.key == pygame.K_r and game_over:
              reset_game()


    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity

        pipe_x -= 3  # Adjust pipe speed

        # Check if pipe went offscreen
        if pipe_x + pipe_width < 0:
            pipe_x = WIDTH
            pipe_y = random.randint(100, HEIGHT - pipe_gap - 100)
            score +=1


        check_collision()

    screen.fill(WHITE)
    draw_bird()
    draw_pipes()

    score_text = font.render("Score: " + str(score), True, GREEN)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over! Press 'R' to restart", True, GREEN)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))


    pygame.display.update()
    clock.tick(60)  # Frames per second

pygame.quit()