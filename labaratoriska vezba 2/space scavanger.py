"""ЛЕОН АСАНОВСКИ - 221007 --> Лабараториска вежба 2"""
import pygame
import random
import time

from tetris.tetromino import GREEN

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
rect_x, rect_y, rect_width, rect_height = 100, 100, 200, 20

asteroid_img = pygame.image.load("asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (100, 100))
background_music = "background_music.wav"
energy_crystal = pygame.image.load("energy_crystal.png")
energy_crystal = pygame.transform.scale(energy_crystal, (50, 50))
space_ship_original = pygame.image.load("spaceship.png")
space_ship = pygame.transform.scale(space_ship_original, (100, 80))
space = pygame.image.load("image.jpg")
space = pygame.transform.scale(space, (1400, 750))

clash_sound = pygame.mixer.Sound("clash_sound.wav")
pygame.mixer.music.load(background_music)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

health = 100
crystals_collected = 0
start_time = 0
high_scores = [0, 0, 0]
crystals = []

def draw_health_bar():
    pygame.draw.rect(screen, WHITE, (rect_x - 5, rect_y - 5,
                                     rect_width + 2 * 5, rect_height + 2 * 5), 5)
    pygame.draw.rect(screen, YELLOW, (rect_x, rect_y, health * 2, rect_height))

def draw_hud():
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
    crystals_text = font.render(f"Crystals collected: {crystals_collected}", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 250, 20))
    screen.blit(crystals_text, (SCREEN_WIDTH - 442, 70))

def spawn_crystals():
    crystal_rect = energy_crystal.get_rect(
        midtop=(random.randint(100, SCREEN_WIDTH), random.randint(100, SCREEN_HEIGHT // 2)))
    crystals.append(crystal_rect)

def spawn_asteroid():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        asteroid_rect = asteroid_img.get_rect(midtop=(random.randint(0, SCREEN_WIDTH), 0))
        asteroid_speed = (0, 5)
    elif side == "bottom":
        asteroid_rect = asteroid_img.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT))
        asteroid_speed = (0, -5)
    elif side == "left":
        asteroid_rect = asteroid_img.get_rect(midleft=(0, random.randint(0, SCREEN_HEIGHT)))
        asteroid_speed = (5, 0)
    else:
        asteroid_rect = asteroid_img.get_rect(midright=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)))
        asteroid_speed = (-5, 0)
    return asteroid_rect, asteroid_speed

def display_game_over():
    global high_scores, crystals_collected
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {crystals_collected}", True, WHITE)
    try_again_text = font.render("Press R to Try Again", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    screen.blit(try_again_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 60))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    running_game_loop()
                    waiting_for_input = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def game_loop():
    global health, crystals_collected, start_time, high_scores, crystals
    health = 100
    crystals_collected = 0
    start_time = time.time()
    crystals.clear()
    pygame.mixer.music.play(-1)

    asteroids = []
    player_rect = space_ship.get_rect(topleft=(50, SCREEN_HEIGHT - 150))
    spawn_crystals()

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(space, (0, 0))
        draw_health_bar()
        draw_hud()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_d] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += 5
        if keys[pygame.K_w] and player_rect.top > 0:
            player_rect.y -= 5
        if keys[pygame.K_s] and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += 5

        if crystals_collected in range(0, 10):
            if random.randint(1, 100) == 1 and len(asteroids) < 6:
                asteroid_rect, asteroid_speed = spawn_asteroid()
                asteroids.append([asteroid_rect, asteroid_speed])
            current_level_text = font.render('EASY LEVEL', True, GREEN)

        elif crystals_collected in range(10, 20):
            if random.randint(1, 60) == 1 and len(asteroids) < 8:
                asteroid_rect, asteroid_speed = spawn_asteroid()
                asteroids.append([asteroid_rect, asteroid_speed])
            current_level_text = font.render('MEDIUM LEVEL', True, YELLOW)

        elif crystals_collected in range(20, 30):
            if random.randint(1, 40) == 1 and len(asteroids) < 10:
                asteroid_rect, asteroid_speed = spawn_asteroid()
                asteroids.append([asteroid_rect, asteroid_speed])
            current_level_text = font.render('HARD LEVEL', True, BLUE)

        elif crystals_collected >= 30:
            if random.randint(1, 20) == 1 and len(asteroids) < 12:
                asteroid_rect, asteroid_speed = spawn_asteroid()
                asteroids.append([asteroid_rect, asteroid_speed])
            current_level_text = font.render('EXTREME HARD LEVEL', True, RED)

        screen.blit(current_level_text, (SCREEN_WIDTH // 2 - 150, 50))

        for asteroid, speed in asteroids[:]:
            asteroid.x += speed[0]
            asteroid.y += speed[1]
            if asteroid.colliderect(player_rect):
                health -= 20
                clash_sound.play()
                asteroids.remove([asteroid, speed])
            elif asteroid.top > SCREEN_HEIGHT or asteroid.bottom < 0 or asteroid.left > SCREEN_WIDTH or asteroid.right < 0:
                asteroids.remove([asteroid, speed])

        for crystal in crystals[:]:
            if player_rect.colliderect(crystal):
                crystals_collected += 1
                crystals.remove(crystal)
                spawn_crystals()

        for asteroid, _ in asteroids:
            screen.blit(asteroid_img, asteroid.topleft)
        for crystal in crystals:
            screen.blit(energy_crystal, crystal.topleft)

        if health <= 0:
            pygame.mixer.music.stop()
            high_scores = sorted(high_scores + [crystals_collected], reverse=True)[:3]
            display_game_over()
            running = False

        screen.blit(space_ship, player_rect.topleft)
        pygame.display.flip()
        clock.tick(60)

def running_game_loop():
    game_loop()

if __name__ == '__main__':
    running_game_loop()
    pygame.quit()
