"""
This code is entirely made by JPB and does not include any copyrights.

To change anything go to "configurations.py"

"""

import pygame
import random
from configurations import *
from bird import Bird
from pipe import (Pipe, create_pipe)
from cloud import (Cloud, create_cloud)

"""Where all the functions are"""

def check_colisions(bird, pipe):
    return pygame.sprite.collide_mask(bird, pipe) != None

def check_events():
    global playing
    global running
    global score
    global text
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSLASH:
                colisions = not colisions
            if event.key == pygame.K_ESCAPE:
                playing = False
                running = False
            if event.key == pygame.K_8:
                score += 999

def create_objects():
    global text
    global score
    if frames%120 == 0:
            pipe_list.append(create_pipe(random.randint(PIPE_GAP+100, SCY-100)))
            score += 1

    if frames%240 == 0:
        cloud_list.append(create_cloud((random.randint(SCX, SCX+300), random.randint(100, SCY-200))))

    if score > -1:
        strscore = str(score)
        text = font.render(strscore, True, (255,255,255))

def reset():
    global player
    global pipe_list
    global cloud_list
    global running
    global colisions
    global score
    global strscore
    global text
    global frames

    player = Bird((SCX//4, SCY//2))

    pipe_list = []
    cloud_list = []

    running = True

    colisions = True

    score = -(PIPE_DELAY//250)
    strscore = 'j'

    text = font.render("0", True, (255,255,255))

    frames = 0

def draw_sprites():
    global running
    for cloud in cloud_list:
        cloud.update()
        screen.blit(cloud.surf, cloud.rect)
    player.update()
    screen.blit(player.surf, player.rect)
    for pipes in pipe_list:
        for pipe in pipes:
            if check_colisions(player, pipe) and colisions:
                running = False
            pipe.update()
            screen.blit(pipe.surf, pipe.rect)
    screen.blit(text, (SCX//2-((len(strscore)//2)*30), 10))

def play():
    global playing
    global frames

    reset()

    while running:
        check_events()

        create_objects()
        
        screen.fill((0,255,255))
        draw_sprites()

        pygame.display.flip()

        clock.tick(60)

        frames = (frames+1)%240
    
    pygame.time.delay(200)

    game_over(player, cloud_list, pipe_list)
    player.kill()
    for pipes in pipe_list:
        for pipe in pipes:
            pipe.kill()
    for cloud in cloud_list:
        cloud.kill()

def game_over(player, cloud_list, pipe_list):
    while player.rect.bottom < SCY:
        pygame.event.get()
        screen.fill((0,255,255))
        player.update()
        for cloud in cloud_list:
            cloud.update()
            screen.blit(cloud.surf, cloud.rect)
        for pipes in pipe_list:
            for pipe in pipes:
                screen.blit(pipe.surf, pipe.rect)
        screen.blit(player.surf, player.rect)
        pygame.display.flip()
        clock.tick(60)

    gom = game_over_font.render("GAME OVER", True, (255,0,0))
    under = under_font.render("Press (p) to continue", True, (255,255,255))

    screen.blit(gom, ((SCX//2)-9*19, SCY//2-40))
    screen.blit(under, ((SCX//2)-12*6, SCY//2+40))
    pygame.display.flip()

"""Where all the code is"""

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

playing = True

font = pygame.font.Font(None, 100)

under_font = pygame.font.Font(None, 25)

game_over_font = pygame.font.Font(None, 80)

clock = pygame.time.Clock()

play()

while playing:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
    if pygame.key.get_pressed()[pygame.K_p]:
        play()

pygame.quit()