import pygame
import random
import math
from pygame.locals import (
    K_a,
    K_s,
    K_d,
    K_w,
    K_F11,
    QUIT,
    K_SPACE,
    K_ESCAPE,
)

RESOLUTION = SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 640

PLAYER_SIZE = PX, PY = 20, 20
PLAYER_CENTER = PCX, PCY = PX/2,PY/2
PLAYER_COLOR = PR, PG, PB = 0,255,0
PLAYER_SPEED = 5
DASH_SPEED = 1

BULLET_SIZE = BX, BY = 10,10
BULLET_COLOR = BR, BG, BB = 255,0,0
BULLET_CENTER = BCX, BCY = 5,5
BULLET_SPEED = BULLET_SPEED_MIN, BULLET_SPEED_MAX = 5,10
BULLET_NUMBER = 10

LAZER_WIDTH = 50

MAX_DURATION = 10
STARTING_LEVEL = 1
STARTING_STAGE = 1

lists = list_x, list_y = [random.randint(-20,-10),random.randint(SCREEN_WIDTH+10,SCREEN_WIDTH+20)], [random.randint(-20,-10),random.randint(SCREEN_HEIGHT+10,SCREEN_HEIGHT+20)]
functions_list = [(random.choice(list_x),random.randint(50,SCREEN_HEIGHT)),(random.randint(50,SCREEN_WIDTH),random.choice(list_y))]

DASH = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface(PLAYER_SIZE)
        self.circle = pygame.draw.circle(self.surf, PLAYER_COLOR, PLAYER_CENTER, PX/2)
        self.radius = 3*((PX/2)/4)
        self.rect = self.surf.get_rect(
            center = (SCREEN_WIDTH/2-PX, SCREEN_HEIGHT/2-PY)
        )
        self.speed_multipliyer = 1.0

    def update(self, pressed_keys, DASH):
        global player_speed_multiplyer
        player_speed_multiplyer = round(self.speed_multipliyer, 20)
        #diagonal dash
        if pressed_keys[K_s] and pressed_keys[K_a] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(-math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer,math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer)
            #DASH = False
        elif pressed_keys[K_s] and pressed_keys[K_d] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer,math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer)
            #DASH  = False
        elif pressed_keys[K_w] and pressed_keys[K_a] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(-math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer,-math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer)
            #DASH  = False
        elif pressed_keys[K_w] and pressed_keys[K_d] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer,-math.sqrt((DASH_SPEED*PLAYER_SPEED)**2/2)*self.speed_multipliyer)
            #DASH  = False
        #normal dash
        elif pressed_keys[K_w] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(0,-DASH_SPEED*PLAYER_SPEED*self.speed_multipliyer)
            #DASH  = False
        elif pressed_keys[K_a] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(-DASH_SPEED*PLAYER_SPEED*self.speed_multipliyer,0)
            #DASH  = False
        elif pressed_keys[K_s] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(0,DASH_SPEED*PLAYER_SPEED*self.speed_multipliyer)
            #DASH  = False
        elif pressed_keys[K_d] and pressed_keys[K_SPACE] and DASH:
            self.rect.move_ip(DASH_SPEED*PLAYER_SPEED*self.speed_multipliyer,0)
            #DASH  = False
        #diagonal movement
        elif pressed_keys[K_w] and pressed_keys[K_d]:
            self.rect.move_ip(math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer,-math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer)
        elif pressed_keys[K_w] and pressed_keys[K_a]:
            self.rect.move_ip(-math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer,-math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer)
        elif pressed_keys[K_s] and pressed_keys[K_d]:
            self.rect.move_ip(math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer,math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer)
        elif pressed_keys[K_s] and pressed_keys[K_a]:
            self.rect.move_ip(-math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer,math.sqrt(PLAYER_SPEED**2/2)*self.speed_multipliyer)
        #normal movement
        elif pressed_keys[K_w]:
            self.rect.move_ip(0,-PLAYER_SPEED*self.speed_multipliyer)
        elif pressed_keys[K_a]:
            self.rect.move_ip(-PLAYER_SPEED*self.speed_multipliyer,0)
        elif pressed_keys[K_s]:
            self.rect.move_ip(0,PLAYER_SPEED*self.speed_multipliyer)
        elif pressed_keys[K_d]:
            self.rect.move_ip(PLAYER_SPEED*self.speed_multipliyer,0)
        
        #wall colisions
        if self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_multipliyer += 0.01
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.speed_multipliyer += 0.01
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
            self.speed_multipliyer += 0.01
        elif self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
            self.speed_multipliyer += 0.01

class Bullet(pygame.sprite.Sprite):
    def __init__(self,functions_list):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface(BULLET_SIZE)
        self.circle = pygame.draw.circle(self.surf, BULLET_COLOR, BULLET_CENTER, BX/2)
        self.radius = BX/2
        self.rect = self.surf.get_rect(
            center = (random.choice(functions_list))
        )
        self.speed = random.randint(BULLET_SPEED_MIN, BULLET_SPEED_MAX)
        self.surf.set_colorkey((0,0,0))
    
    def direction(self):
        if self.rect.centerx <= 0:
            self.deirectionx = "right"
        elif self.rect.centerx >= SCREEN_WIDTH:
            self.deirectionx = "left"
        else:
            self.deirectionx = 0

        if self.rect.centery <= 0:
            self.deirectiony = "down"
        elif self.rect.centery >= SCREEN_HEIGHT:
            self.deirectiony = "up"
        else:
            self.deirectiony = 0
    
    def update(self):
        if self.deirectionx == "right":
            self.rect.move_ip(self.speed, 0)
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
        elif self.deirectionx == "left":
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right <= 0:
                self.kill()
        if self.deirectiony == "down":
            self.rect.move_ip(0, self.speed)
            if self.rect.top >= SCREEN_HEIGHT:
                self.kill()
        elif self.deirectiony == "up":
            self.rect.move_ip(0, -self.speed)
            if self.rect.bottom <= 0:
                self.kill()
        
class Lazer(pygame.sprite.Sprite):
    def __init__(self):
        super(Lazer, self).__init__()
        a = random.randint(1,2)
        if a == 1:
            self.surf = pygame.Surface((LAZER_WIDTH,SCREEN_HEIGHT))
            self.line = pygame.draw.line(self.surf, (100,0,0), (LAZER_WIDTH/2-5,0), (LAZER_WIDTH/2-5,SCREEN_HEIGHT), 5)
            self.rect = self.surf.get_rect(
                center = (random.randint(40, SCREEN_WIDTH-40), SCREEN_HEIGHT/2)
            )
        else:
            self.surf = pygame.Surface((SCREEN_WIDTH,LAZER_WIDTH))
            self.line = pygame.draw.line(self.surf, (100,0,0), (0,LAZER_WIDTH/2-5), (SCREEN_WIDTH,LAZER_WIDTH/2-5), 5)
            self.rect = self.surf.get_rect(
                center = (SCREEN_WIDTH/2, random.randint(40, SCREEN_HEIGHT-40))
            )
        self.surf.set_colorkey((0,0,0))
    
    def update(self, lazer_timer):
        if lazer_timer == 1:
            self.surf.fill(BULLET_COLOR)
        if lazer_timer >= 4:
            self.kill()

class Boss1(pygame.sprite.Sprite): #do later
    def __init__(self):
        super(Boss1, self).__init__()
        self.surf = pygame.Surface((10*PX, 10*PY))
        self.circle = pygame.draw.circle(self.surf, BULLET_COLOR, (5*PX, 5*PY), 5*PX)
        self.rect = self.surf.get_rect(
            center = (SCREEN_WIDTH/2 - 5*PX, SCREEN_HEIGHT/2 - 5*PY)
        )
        self.counter = 0
    
    def bullet(self):
        self.bullets = pygame.Surface(BULLET_SIZE)
        self.bullets_circle = pygame.draw.circle(self.bullets, BULLET_COLOR, BULLET_CENTER, BX/2)
        self.bullets_rect = self.bullets.get_rect(
            center = (SCREEN_WIDTH/2 - 5*PX, SCREEN_HEIGHT/2 - 5*PY)
        )
        self.counter += 1
    
    def bullet_direction(self):
        if self.counter%2 == 0:
            i = random.randint(1,2)
            if i == 1:
                self.bullets.move_ip(0, -random.randint(BULLET_SPEED))
            else:
                self.bullets.move_ip(0, random.randint(BULLET_SPEED))
            
            if self.bullets_rect.top == SCREEN_HEIGHT:
                self.bullets.kill()
            elif self.bullets_rect.bottom == 0:
                self.bullets.kill()
        else:
            i = random.randint(1,2)
            if i == 1:
                self.bullets.move_ip(-random.randint(BULLET_SPEED), 0)
            else:
                self.bullets.move_ip(random.randint(BULLET_SPEED), 0)
            
            if self.bullets_rect.left == SCREEN_WIDTH:
                self.bullets.kill()
            elif self.bullets_rect.right == 0:
                self.bullets.kill()
    
    def attack2(self):
        i = random.randint(1,2)
        if i == 1:
            self.lazer = pygame.Surface(RESOLUTION)
            self.lazer.line = pygame.draw.line(self.lazer, (100,0,0), (0,random.randint(0, SCREEN_HEIGHT)), (SCREEN_WIDTH, random.randint(0,SCREEN_HEIGHT)), 5)
        else:
            self.lazer = pygame.surface(RESOLUTION)
            self.lazer.line = pygame.draw.line(self.lazer, (100,0,0), (random.randint(0, SCREEN_WIDTH), 0), (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT), 5)
        
    def update_lazers(self):
        if lazer_timer == 2:
            self.killer = pygame.draw.line(self.lazer, (255,0,0), self.lazer.line, LAZER_WIDTH)
        if lazer_timer == 4:
            self.lazer.kill()

def game_over_screen(pressed_keys, level, all_sprites):
    while not pressed_keys[K_ESCAPE]:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            screen.fill((0,0,0))
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
            pressed_keys = pygame.key.get_pressed()
            game_over = font.render("GAME OVER", True, (155,0,0))
            game_over_level = fps_font.render(f"You died at level{level}", True, (255,255,255))
            screen.blit(game_over, text_position)
            screen.blit(game_over_level, (textx+65, texty+45))
            pygame.display.flip()
    for entity in all_sprites:
        entity.kill()

def check_collisions(players, bullets, lazers, all_sprites, lazer_timer, pressed_keys, level):
    for new_player in players:
        for entity in bullets:
            if pygame.sprite.collide_circle(new_player, entity):
                game_over_screen(pressed_keys, level, all_sprites)
                new_player = Player()
                all_sprites.add(new_player)
                players.add(new_player)
                return True
        for entity in lazers:
            if pygame.sprite.collide_rect_ratio(0.75)(new_player, entity) and (lazer_timer >= 1 and lazer_timer <= 4):
                game_over_screen(pressed_keys, level, all_sprites)
                new_player = Player()
                all_sprites.add(new_player)
                players.add(new_player)  
                return True             

pygame.init()
running = True
boss = True

bullet_coolldown = 0

generate_bullet = pygame.USEREVENT+1
pygame.time.set_timer(generate_bullet, BULLET_NUMBER)

time = pygame.USEREVENT+2
pygame.time.set_timer(time, 1000)

level = STARTING_LEVEL
level_stage = STARTING_STAGE

next_level_stage = pygame.USEREVENT+3
pygame.time.set_timer(next_level_stage, 10000)

lazer_timer = 0
used_lazers = 0

duration = MAX_DURATION

font = pygame.font.SysFont('trebucbd.ttf', 40)
fps_font = pygame.font.SysFont('trebucbd.ttf', 10)
text_position = textx, texty = SCREEN_WIDTH/2-90, SCREEN_HEIGHT/2-20

new_player = Player()
#new_bullet = Bullet(functions_list)
#new_bullet.direction()

players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
lazers = pygame.sprite.Group()
bosses = pygame.sprite.Group()
all_sprites.add(new_player)
#all_sprites.add(new_bullet)
#bullets.add(new_bullet)
players.add(new_player)

screen = pygame.display.set_mode(RESOLUTION)

clock = pygame.time.Clock()
spawned_bullet = False

while running:
    functions_list = [(random.choice(list_x),random.randint(0,SCREEN_HEIGHT)),(random.randint(0,SCREEN_WIDTH),random.choice(list_y))]
    fps = pygame.time.Clock.get_fps(clock)
    #print(level < 20)

    if lazer_timer > 4:
        lazer_timer = -1
        used_lazers = 0

    for event in pygame.event.get():
        #print(event.type == next_level_stage)
        if event.type == QUIT:
            running = False
        
        if event.type == generate_bullet:
            bullet_coolldown += 1
        
        if event.type == next_level_stage:
            level_stage += 1
            lazer_timer = 0

        if event.type == time:
            duration -= 1
            lazer_timer += 1
    
    #print(DASH)
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_F11]:
        level = 50
        level_stage = 1
        duration = MAX_DURATION
    
    players.update(pressed_keys, DASH)
    bullets.update()
    lazers.update(lazer_timer)
    
    screen.fill((0,0,0))

    if bullet_coolldown == int(1000/BULLET_NUMBER)+1 - level and level_stage%2 != 0: #and level%5 != 0:
        #boss = True
        bullet_coolldown = 0
        for shoot in range(0,level):
            functions_list = [(random.choice(list_x),random.randint(0,SCREEN_HEIGHT)),(random.randint(0,SCREEN_WIDTH),random.choice(list_y))]
            new_bullet = Bullet(functions_list)
            new_bullet.direction()
            all_sprites.add(new_bullet)
            bullets.add(new_bullet)
    elif level_stage%2 == 0: #and level%5 != 0:
        bullet_coolldown = 0
        while used_lazers < level and lazer_timer == 0:
            new_lazer = Lazer()
            all_sprites.add(new_lazer)
            lazers.add(new_lazer)
            used_lazers += 1
    
    #if level%5 == 0 and boss:
        #new_boss = Boss1()
        #all_sprites.add(new_boss)
        #bosses.add(new_boss)
        #boss = False
    #elif level%5 == 0 and level_stage%2 != 0:
        #if bullet_coolldown == 21 - level:
            #new_bullet = new_boss.attack1()
            #bullets.add(new_bullet)
            #all_sprites.add(new_bullet)
            #spawned_bullet = True
        #if spawned_bullet:
            #new_boss.bullet_direction()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    show_level = font.render(f"level{level}", True, (255,255,255))
    screen.blit(show_level, (SCREEN_WIDTH/2-90,10))

    fps_show = fps_font.render(f"fps: {int(fps)}/120", True, (255,255,255))
    screen.blit(fps_show, (0,0))

    speed_multiplyer = fps_font.render(f"x{round(player_speed_multiplyer, 2)}", True, (255,255,255))
    screen.blit(speed_multiplyer, (SCREEN_WIDTH-50,0))

    if check_collisions(players, bullets, lazers, all_sprites, lazer_timer, pressed_keys, level):
        check_collisions(players, bullets, lazers, all_sprites, lazer_timer, pressed_keys, level)
        level = STARTING_LEVEL
        level_stage = STARTING_STAGE
        duration = MAX_DURATION

    if duration == 0:
        duration = MAX_DURATION
        level += 1
        
    pygame.display.flip()

    clock.tick(120)