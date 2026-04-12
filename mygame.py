import pygame
import random
from pygame.locals import(
    K_a,
    K_s,
    K_d,
    K_w,
    K_LEFT,
    K_DOWN,
    K_RIGHT,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

global enemy_controler
enemy_controler = 1

RESOLUTION = WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = X, Y = 50,50
PLAYER_SPEED = 20
BACKGROUND_COLOR = R, G, B = 0, 0, 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((PLAYER_SIZE))
        self.surf.fill((0,0,255))
        self.rect = self.surf.get_rect(
            center = (WIDTH/2,HEIGHT)
            )
    
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0,-PLAYER_SPEED)
        if pressed_keys[K_s]:
            self.rect.move_ip(0,PLAYER_SPEED)
        if pressed_keys[K_a]:
            self.rect.move_ip(-PLAYER_SPEED,0)
        if pressed_keys[K_d]:
            self.rect.move_ip(PLAYER_SPEED,0)

        if self.rect.left < 0 :
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 50:
            self.rect.top = 50
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((PLAYER_SIZE))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(
            center = (WIDTH/2 , 50)      
        )
           
    def update(self, direction, pressed_keys):
        if enemy_controler == 0:
            if direction == 1:
                self.rect.move_ip(0, -PLAYER_SPEED)
            elif direction == 2:
                self.rect.move_ip(0, PLAYER_SPEED)
            elif direction == 3:
                self.rect.move_ip(-PLAYER_SPEED, 0)
            elif direction == 4:
                self.rect.move_ip(PLAYER_SPEED, 0)
        else:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0,-PLAYER_SPEED)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,PLAYER_SPEED)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PLAYER_SPEED,0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PLAYER_SPEED,0)
        
        if self.rect.left < 0 :
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 50:
            self.rect.top = 50
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((X/2, Y/2))
        self.surf.fill((255,100,0))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(Y, WIDTH - Y/2),
                random.randint(50 + X/2, HEIGHT - X/2),
            )
        )
    
pygame.init()

running = True
screen = pygame.display.set_mode(RESOLUTION)
direction = 2
duration = 60
player_score_value = 0
enemy_score_value = 0

secret = pygame.font.SysFont('trebucbd.ttf', 7)
font = pygame.font.SysFont('trebucbd.ttf', 30)
enemy_text_position = textx, texty = 5, 5
player_text_position = textx, texty = WIDTH-260, 5

UPDATENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATENEMY, 250)

TIME = pygame.USEREVENT + 1
pygame.time.set_timer(TIME, 1000)

player = Player()
enemy = Enemy()
new_food = Food()

foods = pygame.sprite.Group()

all_surfaces = pygame.sprite.Group()
all_surfaces.add(player)
all_surfaces.add(enemy)
all_surfaces.add(new_food)

foods.add(new_food)

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                enemy_controler = 0
        if event.type == UPDATENEMY:
            direction = random.randint(1,4)
        if event.type == TIME:
            duration -= 1
            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemy.update(direction, pressed_keys)
    
    screen.fill(BACKGROUND_COLOR)

    player_score = font.render(f"Blue Score:{player_score_value}", True, (0,0,255))
    screen.blit(player_score, (player_text_position))
    
    enemy_score = font.render(f"Red Score:{enemy_score_value}", True, (255,0,0))
    screen.blit(enemy_score, (enemy_text_position))

    time = font.render(f"{duration}", True, (255,255,255))
    screen.blit(time, (WIDTH/2 - 45,5))

    for entity in all_surfaces:
        screen.blit(entity.surf, entity.rect)

    if duration == 0:
        font2 = pygame.font.SysFont("trebucbd.ttf", 50)
        final_runing = True
        if player_score_value > enemy_score_value:
            final_message = font2.render("BLUE WINS!", True, (0,0,255))
        elif player_score_value < enemy_score_value:
            final_message = font2.render("RED WINS!", True, (255,0,0))
        else:
            final_message = font2.render("DRAW!", True, (0,255,0))
        
        while final_runing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    final_runing = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        final_runing = False
                        duration = 60
                        
            screen.blit(final_message, ((WIDTH / 2) - 250, HEIGHT/2 - 50))
        
            pygame.display.flip()
    
    secret_text = secret.render('Made by: JP', True, (255,255,255))
    screen.blit(secret_text, (WIDTH - 45, HEIGHT - 12))

    #print(pygame.sprite.spritecollideany(player, foods) != None)
    #print(new_food.rect)

    if pygame.sprite.spritecollideany(player, foods) != None:
        new_food.kill()
        new_food = Food()
        foods.add(new_food)
        all_surfaces.add(new_food)
        player_score_value += 1
    
    if pygame.sprite.spritecollideany(enemy, foods) != None:
        new_food.kill()
        new_food = Food()
        foods.add(new_food)
        all_surfaces.add(new_food)
        enemy_score_value += 1

    pygame.display.flip()

    clock.tick(30)