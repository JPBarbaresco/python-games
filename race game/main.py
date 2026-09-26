import pygame
import math

from car import Car
from camera import Camera
from timer import Timer
from menu import Menu
from button import *

from configurations import *

from pygame.locals import (
    K_a,
    K_w,
    K_s,
    K_d,
    K_LEFT,
    K_UP,
    K_DOWN,
    K_RIGHT
)

def play():
    global friction
    global friction2
    
    global world
    
    global car
    global car2

    global car_old_x
    global car_old_y
    global car2_old_x
    global car2_old_y
    
    global timer
    global timer2
    
    global camera
    global camera2
    
    global walls_collision_mask
    global grass_collision_mask
    
    global finish_line_x
    global finish_line_y0
    global finish_line_y1
    
    global lap_count

    global total_delta
    global old_total_delta

    delta = clock.tick(FPS)/1000

    total_delta += delta

    world.fill((0,0,0))

    pressed_keys = pygame.key.get_pressed()

    last_car_x = car.x
    last_car2_x = car2.x

    if int(total_delta) != old_total_delta:
        car_old_x, car_old_y = car.x, car.y
        car2_old_x, car2_old_y = car2.x, car2.y
        old_total_delta = int(total_delta)

    if timer.lap_number <= lap_count:
        car.update(pressed_keys, friction, delta)
    else:
        car.update([], 5*friction, delta)
    
    if timer2.lap_number <= lap_count:
        car2.update(pressed_keys, friction2, delta)
    else:
        car2.update([], 5*friction, delta)

    car_on_grass = grass_collision_mask.overlap(car.mask, (int(car.x - car.radius), int(car.y - car.radius)))
    car2_on_grass = grass_collision_mask.overlap(car2.mask, (int(car2.x - car2.radius), int(car2.y - car2.radius)))

    check_wall_colision(car_old_x, car_old_y, car2_old_x, car2_old_y)

    if (last_car_x < finish_line_x <= car.x) and (finish_line_y0 <= car.y <= finish_line_y1):
        timer.complete_lap()

    if (last_car2_x < finish_line_x <= car2.x) and (finish_line_y0 <= car2.y <= finish_line_y1):
        timer2.complete_lap()

    if car_on_grass != None:
        friction = GRASS_FRICTION
    else:
        friction = TRACK_FRICTION
    
    if car2_on_grass != None:
        friction2 = GRASS_FRICTION
    else:
        friction2 = TRACK_FRICTION
        
    camera.update()
    camera2.update()

    if 0 < timer.lap_number <= lap_count:
        timer.update(delta)
    if 0 < timer2.lap_number <= lap_count:
        timer2.update(delta)

def check_wall_colision(car_old_x, car_old_y, car2_old_x, car2_old_y):
    car_hit_wall = walls_collision_mask.overlap(car.mask, (int(car.x - car.radius), int(car.y - car.radius)))
    car2_hit_wall = walls_collision_mask.overlap(car2.mask, (int(car2.x - car2.radius), int(car2.y - car2.radius)))

    if car_hit_wall != None:
        car.x = car_old_x
        car.y = car_old_y
        car.speed = 0

    if car2_hit_wall != None:
        car2.x = car2_old_x
        car2.y = car2_old_y
        car2.speed = 0

def draw_game():
    world.blit(track, (0,0))

    world.blit(car.surf, car.rect)
    world.blit(car2.surf, car2.rect)

    screen.blit(world, (0,0), camera.rect)
    screen.blit(world, (SCREENX//2, 0), camera2.rect)

    timer.draw(timer_font, screen, (2,2))
    timer2.draw(timer_font, screen, (SCREENX//2+4, 2))

    timer.draw_lap_info(small_font, screen, (5, 15))
    timer2.draw_lap_info(small_font, screen, (SCREENX//2+7, 15))

    pygame.draw.circle(world, car.color, car.rect.center, 35)
    pygame.draw.circle(world, car2.color, car2.rect.center, 35)

    mini_map = pygame.transform.scale(world, (80, 45))
    mini_map_rect = mini_map.get_rect(center = (SCREENX//2, 27*SCREENY//32))
    mini_map.set_colorkey((108, 203, 104))

    if timer.lap_number > lap_count:
        screen.blit(finish_screen_veil, (0,0))
    if timer2.lap_number > lap_count:
        screen.blit(finish_screen_veil, (SCREENX//2,0))

    pygame.draw.line(screen, (255,255,255), (SCREENX//2, 0), (SCREENX//2, SCREENY), 3)

    pygame.draw.rect(screen, (255,255,255), (mini_map_rect.x-3, mini_map_rect.y-3, mini_map_rect.width+6, mini_map_rect.height+6))
    pygame.draw.rect(screen, (81,81,81), (mini_map_rect.x, mini_map_rect.y, mini_map_rect.width, mini_map_rect.height))

    screen.blit(mini_map, mini_map_rect)

    if timer.lap_number > lap_count:
        final_time = buttons_font.render(timer.format_time(sum(timer.lap_times)), False, (255,255,255))
        screen.blit(final_time, final_time.get_rect(center = (SCREENX//4, SCREENY//2)))
    if timer2.lap_number > lap_count:
        final_time2 = buttons_font.render(timer2.format_time(sum(timer2.lap_times)), False, (255,255,255))
        screen.blit(final_time2, final_time2.get_rect(center = (3*SCREENX//4, SCREENY//2)))

def start_game(car1_color, car2_color):
    global camera
    global camera2
    
    global car
    global car2

    global car_old_x
    global car_old_y
    global car2_old_x
    global car2_old_y
    
    global timer
    global timer2
    
    global track
    
    global friction
    global friction2
    
    global world
    
    global grass_collision_mask
    global walls_collision_mask

    global walls
    
    global finish_line_x
    global finish_line_y0
    global finish_line_y1

    global lap_count

    global finish_screen_veil

    car_start_position = (600, 175)
    car2_start_position = (600, 200)

    car = Car(CAR_SIZE, car_start_position, car1_color, [K_a, K_w, K_s, K_d])
    car2 = Car(CAR_SIZE, car2_start_position, car2_color, [K_LEFT, K_UP, K_DOWN, K_RIGHT])
    
    car_old_x, car_old_y = car.x, car.y
    car2_old_x, car2_old_y = car2.x, car2.y

    camera = Camera((SCREENX//2, SCREENY), (0, 0), car)
    camera2 = Camera((SCREENX//2, SCREENY), (0, 0), car2)

    finish_screen_veil = pygame.surface.Surface((SCREENX//2, SCREENY))
    finish_screen_veil.set_alpha(200)

    timer = Timer()
    timer2 = Timer()

    track = pygame.image.load(r"assets\track0.png")
    track = pygame.transform.scale_by(track, 1)

    finish_line_x = 625
    finish_line_y0 = 100
    finish_line_y1 = 250

    pygame.draw.line(track, (255,255,255), (finish_line_x, finish_line_y0+45), (finish_line_x, finish_line_y1-20))
    pygame.draw.line(track, (255,255,255), (finish_line_x+2, finish_line_y0+45), (finish_line_x+2, finish_line_y1-20))

    friction = TRACK_FRICTION
    friction2 = TRACK_FRICTION

    world = pygame.Surface((track.get_width(), track.get_height()))

    grass_collision_mask = pygame.mask.from_threshold(track, (108, 203, 104), (1,1,1))
    walls_collision_mask = pygame.mask.from_threshold(track, (81,81,81), (1,1,1))

    walls_rect = walls_collision_mask.get_rect()

    walls = pygame.sprite.Sprite()

    lap_count = 3

def display_color_preview(car1_color, car2_color):
    car1_display = car1_sprite.copy()
    car2_display = car2_sprite.copy()

    car1_display_color_area = car1_display.copy()
    pygame.transform.threshold(car1_display_color_area, car1_display, (155,155,155), (100,100,100))
    car1_display_color_area.set_colorkey((0,0,0))
    
    car2_display_color_area = car2_display.copy()
    pygame.transform.threshold(car2_display_color_area, car2_display, (155,155,155), (100,100,100))
    car2_display_color_area.set_colorkey((0,0,0))

    car1_display_color_area.fill(car1_color, special_flags=pygame.BLEND_MULT)
    car2_display_color_area.fill(car2_color, special_flags=pygame.BLEND_MULT)

    car1_display.blit(car1_display_color_area, (0,0))
    car2_display.blit(car2_display_color_area, (0,0))
    
    screen.blit(car1_display, car1_display.get_rect(center = (3*SCREENX//16, 5*SCREENY//8)))
    screen.blit(car2_display, car2_display.get_rect(center = (13*SCREENX//16, 5*SCREENY//8)))

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.FULLSCREEN)

timer_font = pygame.font.SysFont('pressstart2pregular', 12)
small_font = pygame.font.SysFont('pressstart2pregular', 8)

title_font = pygame.font.SysFont('pressstart2pregular', 20)
buttons_font = pygame.font.SysFont('pressstart2pregular', 15)

car_colors = [(255, 0, 0), (255, 100, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0,100,255), (0, 0, 255), (100, 0, 255), (255, 0, 255), (255, 255, 255), (150,150,150), (50,50,50)]

title_menu = Menu(
    SCREEN_SIZE, (0,0), 255,
    
    2, RoundButtom, [(160, 30), (160, 30)], 
    
    [(0, 255, 0), (255, 0, 0)], ["Start Game", "Quit"], [(0,0,0), (0,0,0)], buttons_font, 
    1, 
    
    "Racing Game", title_font, (255,255,255)
    
    )

customization_menu = Menu(
    SCREEN_SIZE, (0,0), 255,

    2*len(car_colors) + 1, Button, [(12, 12) for _ in range(2*len(car_colors))] + [(80, 25)],

    car_colors*2 + [(0,255,0)], ['' for _ in range(2*len(car_colors))] + ["Start"], [(0,0,0) for _ in range(2*len(car_colors))] + [(0,0,0)], buttons_font, 
    4,

    "Choose Car Colors", buttons_font, (255,255,255)

    )

in_title_menu = True
in_customization_menu = False

car_sprite = pygame.image.load(r'assets\car.png')
car_sprite = pygame.transform.rotate(car_sprite, 90)

car1_sprite = pygame.transform.scale_by(car_sprite, 6)
car2_sprite = pygame.transform.scale_by(car_sprite, 6)

car1_color = (0, 255, 255)
car2_color = (255, 255, 0)

car_old_x, car_old_y = 0,0
car2_old_x, car2_old_y = 0,0

total_delta = 0
old_total_delta = 0

clock = pygame.time.Clock()

fullscreen = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if in_title_menu:
                    running = False
                else:
                    in_title_menu = True
            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | 1)

    screen.fill((0,0,0))

    if in_title_menu:
        pressed_buttons = title_menu.update(pygame.mouse.get_pos())
        if pressed_buttons[0]:
            in_title_menu = False
            in_customization_menu = True
        elif pressed_buttons[1]:
            running = False

        title_menu.draw(screen)
    elif in_customization_menu:
        pressed_buttons = customization_menu.update(pygame.mouse.get_pos())
        if pressed_buttons[-1]:
            start_game(car1_color, car2_color)
            in_customization_menu = False
        for buttom in pressed_buttons[:len(car_colors)]:
            if buttom:
                car1_color = car_colors[pressed_buttons.index(buttom)]
        for buttom in pressed_buttons[len(car_colors):2*len(car_colors)]:
            if buttom:
                car2_color = car_colors[pressed_buttons.index(buttom)-len(car_colors)]
        
        customization_menu.draw(screen)
        
        display_color_preview(car1_color, car2_color)

        pygame.draw.line(screen, (255,255,255), (SCREENX//2, SCREENY//4), (SCREENX//2, len(car_colors)//2*16+SCREENY//4))

    else:
        play()

        draw_game()
    
    pygame.display.flip()

pygame.quit()
