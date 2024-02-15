import random
import pygame

pygame.init()
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#set clock
FPS = 60
clock = pygame.time.Clock()

#set game values
player_starting_lives = 5
player_velocity = 10
ball_start_velocity = 5
ball_acceleration = 1
buffer_distance = -100
score = 0
player_lives = player_starting_lives
ball_velocity = 5


#set colors
GREEN = (0,255,0)
DARK_GREEN = (10,50,10)
WHITE = (255,255,255)
BLACK =  (0,0,0)
RED = (255,0,0)
GRASS = (100,200,0)
PINK = (255,105,180)
BROWN =(150,75,0)
YELLOW =(255)

#set fonts
font = pygame.font.Font('SfSportsNight-rrdL.ttf', 35)

#set text
score_text = font.render('Score:' + str(score), True,PINK,DARK_GREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = font.render('GOAL KEEPER!', True, BROWN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH / 2
title_rect.y = 10

lives_text = font.render('Lives:' + str(player_starting_lives), True, PINK, DARK_GREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = WINDOW_WIDTH - 15, 10

game_over_text = font.render('GAMEOVER', True, BLACK, WHITE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT//2

continue_text = font.render('Press any key to play again', True, BLACK, WHITE)
continue_rect = continue_text.get_rect()
continue_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT - 75

#set sounds
miss_sound = pygame.mixer.Sound("miss_sound.wav")
save_sound = pygame.mixer.Sound("save_sound.wav")
pygame.mixer.music.load("battle-time-178551.mp3")

#set images
player_image = pygame.image.load('football-player.png')
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

ball_image = pygame.image.load('football_4.png')
ball_rect = ball_image.get_rect()
ball_rect.x = WINDOW_WIDTH + buffer_distance
ball_rect.y = random.randint(64, WINDOW_HEIGHT -32)

pygame.mixer.music.play(-1,0.0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    if ball_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        ball_rect.x = WINDOW_WIDTH + buffer_distance
        ball_rect.y = random.randint(64, WINDOW_HEIGHT -32)

    else:
        ball_rect.x -= ball_velocity

    if player_rect.colliderect(ball_rect):
        score += 1
        save_sound.play()
        ball_velocity += ball_acceleration
        ball_rect.x = WINDOW_WIDTH + buffer_distance
        ball_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    #update hud
    score_text = font.render('Score:' + str(score), True, PINK, DARK_GREEN)
    lives_text = font.render('Lives:' + str(player_lives), True, PINK, DARK_GREEN)

    #game over check
    if player_lives == 0:
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()

        #pause game until player presses a key and reset

        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_starting_lives
                    player_rect.y = WINDOW_HEIGHT//2
                    ball_velocity = ball_start_velocity
                    pygame.mixer.music.play(-1,0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    
    display_surface.fill(GRASS)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 4)
    pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT-64), (WINDOW_WIDTH, WINDOW_HEIGHT-64), 4)
    pygame.draw.line(display_surface, WHITE, (WINDOW_WIDTH//2, 64), (WINDOW_WIDTH//2, WINDOW_HEIGHT), 4)
    pygame.draw.circle(display_surface, WHITE, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (150), 4)
    pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT//4), (20, WINDOW_HEIGHT//4), 4)
    pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT * 0.75), (20, WINDOW_HEIGHT * 0.75), 4)
    pygame.draw.line(display_surface, WHITE, (20, WINDOW_HEIGHT//4), (20, WINDOW_HEIGHT * 0.75), 4)




    display_surface.blit(player_image, player_rect)
    display_surface.blit(ball_image, ball_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

