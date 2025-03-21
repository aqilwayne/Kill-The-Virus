import pygame
import os
import random

pygame.init()
pygame.mixer.init()

screen_width= 900
screen_height = int(screen_width * 0.8)

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Kill the Virus")

backsound = pygame.mixer.Sound("audio/backsound.mp3")
backsound.set_volume(0.1)

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
TILE_SIZE = 100

#define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

#load images
background_img = pygame.image.load("img/background/final.jpeg").convert_alpha()
#bullet
bullet_img = pygame.image.load("img/icons/bullet.png").convert_alpha()
enemy_bullet_img = pygame.image.load("img/icons/enemy_bullet.png").convert_alpha()
#grenade
grenade_img = pygame.image.load("img/icons/grenade.png").convert_alpha()
#item boxes
hp_box_img = pygame.image.load("img/icons/hp_box.png").convert_alpha()
ammo_box_img = pygame.image.load("img/icons/ammo_box.png").convert_alpha()
grenade_box_img = pygame.image.load("img/icons/grenade_box.png").convert_alpha()
item_boxes = {
   "health"    : hp_box_img,
   "ammo"      : ammo_box_img,
   "grenade"   : grenade_box_img,
}

#define color
BG = (135,206,235)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,250,154)
BLACK = (0,0,0)

#define font
font = pygame.font.SysFont("Futura", 30)

def draw_text(text, font, text_col, x, y):
   img = font.render(text, True, text_col)
   screen.blit(img,(x,y))

def draw_bg():
   screen.blit(background_img, (-300,-50))

class Character(pygame.sprite.Sprite):
   def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.char_type = char_type
    self.speed = speed
    self.shoot_cooldown = 0
    self.grenades= grenades
    self.health = 1000
    self.max_health = self.health
    self.ammo = ammo
    self.start_ammo = ammo
    self.direction = 1
    self.vel_y = 0
    self.jump = False
    self.in_air = True
    self.flip = False
    self.animation_list = []
    self.frame_index = 0
    self.action = 0
    self.update_time = pygame.time.get_ticks()
    #ai specific variables
    self.move_counter = 0
    self.vision = pygame.Rect(0,0,150,20)
    self.idling = False
    self.idling_counter = 0

    #load all images for the player
    animation_types = ["idle","run","jump","death","shooting"]
    for animation in animation_types :
         #reset animation list for the players
         temp_list= []
         #count number of files in folder
         num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
         for i in range (num_of_frames):
            img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png").convert_alpha()
            img = pygame.transform.scale(img , (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
         self.animation_list.append(temp_list)

    self.image = self.animation_list[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)

   def update(self):
      self.update_animation()
      self.check_alive()
      #update cooldown
      if self.shoot_cooldown > 0:
         self.shoot_cooldown -= 1 
   

   def move(self, moving_left, moving_right):
       #reset movement variables
       dx = 0 
       dy = 0

       #assignment moving left/right
       if moving_left:
          dx = -self.speed
          self.flip = True
          self.direction = -1
       if moving_right:
          dx = self.speed
          self.flip = False
          self.direction = 1

       #jump
       if self.jump == True and self.in_air == False:
          self.vel_y = -17
          self.jump = False
          self.in_air = True

       #apply gravitY
       self.vel_y += GRAVITY
       if self.vel_y > 10 :
          self.vel_y 
       dy += self.vel_y

       #check collision with floor
       if self.rect.bottom + dy > 600 :
          dy = 600 - self.rect.bottom
          self.in_air = False

       #update rectangle position
       self.rect.x += dx
       self.rect.y += dy


   def shoot(self):
       if self.shoot_cooldown == 0 and self.ammo > 0:
          self.shoot_cooldown = 20
          bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0]* self.direction), self.rect.centery, self.direction)
          enemy_bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0]* self.direction), self.rect.centery, self.direction)
          bullet_group.add(bullet)
          enemy_bullet_group.add(enemy_bullet)
          #reduce ammo
          self.ammo -= 1

   def ai(self):
       if self.alive and player.alive:
          if self.idling == False and random.randint(1,200) == 1:
             self.update_action(0)
             self.idling = True
             self.idling_counter = 50
         #chechk if the ai near the player
          if self.vision.colliderect(player.rect):
            #stop running and face the player
             self.update_action(0)
            #shoot
             self.shoot()
          else:
            if self.idling == False :
               if self.direction == 1:
                   ai_moving_right = True
               else :
                   ai_moving_right = False
               ai_moving_left = not ai_moving_right   
               self.move(ai_moving_left, ai_moving_right) 
               self.update_action(0)     
               self.move_counter +=1
               #update enemy vision as their direction
               self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

               if self.move_counter > TILE_SIZE:
                  self.direction *= -1
                  self.move_counter *= -1
            else :
               self.idling_counter -= 1
               if self.idling_counter <= 0:
                  self.idling = False
             

   def update_animation(self):
       #update animation
       ANIMATION_COOLDOWN = 100
       #update image depending on current frame
       self.image = self.animation_list[self.action][self.frame_index]
       #check if enough time passed since the last update
       if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN :
          self.update_time = pygame.time.get_ticks()
          self.frame_index += 1
       #reset running 
       if self.frame_index>= len(self.animation_list[self.action]):
          if self.action == 3 :
             self.frame_index = len(self.animation_list[self.action]) - 1
          else :
             self.frame_index = 0
          

   def update_action(self, new_action):
       if new_action != self.action :
          self.action = new_action
          self.frame_index = 0
          self.update_time = pygame.time.get_ticks()
             

   def check_alive(self):
      if self.health <= 0:
         self.health = 0
         self.speed = 0
         self.alive = False
         self.update_action(3)

   def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class ItemBox(pygame.sprite.Sprite):
   def __init__(self, item_type, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.item_type = item_type
      self.image = item_boxes[self.item_type]
      self.rect = self.image.get_rect()
      self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

   def update(self):
      #check if player has picked up the box
      if pygame.sprite.collide_rect(self, player):
         #check what kind of box
         if self.item_type == "health":
            player.health += 200
            if player.health > player.max_health :
               player.health = player.max_health
         elif self.item_type == "ammo":
            player.ammo += 20
            if player.ammo >= 30 :
               player.ammo = 30
         elif self.item_type == "grenade":
            player.grenades += 3
         #delete the item box
         self.kill()

class HealthBar():
   def __init__(self, x, y, health, max_health):
      self.x = x
      self.y = y
      self.health = health
      self.max_health = max_health

   def draw(self, health):
      #update with new health
      self.health = health
      #calculate health ratio
      ratio = self.health / self.max_health
      pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2,154, 24))
      pygame.draw.rect(screen, RED, (self.x, self.y,150, 20))
      pygame.draw.rect(screen, GREEN, (self.x, self.y,150 * ratio, 20))

class Bullet(pygame.sprite.Sprite):
   def __init__(self, x, y, direction):
      pygame.sprite.Sprite.__init__(self)
      self.speed = 10
      self.image = bullet_img
      self.enemy_bullet = enemy_bullet_img
      self.rect = self.image.get_rect()
      self.enemy_rect = self.enemy_bullet.get_rect()
      self.rect.center = (x,y)
      self.direction = direction

   def update(self):
         #move bullet
         self.rect.x += (self.direction * self.speed)

         #check if bullet gone off screen
         if self.rect.right <0 or self.rect.left > screen_width:
            self.kill()
 
         #chechk collision with character
         if pygame.sprite.spritecollide(player, bullet_group, False) :
            if player.alive :
               player.health -= 20
               self.kill()

         for enemy in enemy_group :
            if pygame.sprite.spritecollide(enemy, bullet_group, False) :
               if enemy.alive :
                  enemy.health -= 50
                  self.kill()  
       
class Grenade(pygame.sprite.Sprite):
   def __init__(self, x, y, direction):
      pygame.sprite.Sprite.__init__(self)
      self.timer = 100
      self.vel_y = -11
      self.speed = 7
      self.image = grenade_img
      self.rect = self.image.get_rect()
      self.rect.center = (x,y)
      self.direction = direction

   def update(self):
      self.vel_y += GRAVITY
      dx = self.direction * self.speed
      dy = self.vel_y

      #check collision with floor
      if self.rect.bottom + dy > 600 :
          dy = 600 - self.rect.bottom
          self.speed = 0

      #check collision with walls
      if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
          self.direction *= -1

      #update grenade position
      self.rect.x += dx
      self.rect.y += dy

      #countdown timer
      self.timer -= 1
      if self.timer <= 0:
         self.kill()
         explosion = Explosion(self.rect.x, self.rect.y, 0.5)
         explosion_group.add(explosion)
         #area damage
         if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
            abs(self.rect.centery - player.rect.centerx) < TILE_SIZE * 2 :
                player.health -= 50
         for enemy in enemy_group :
            if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
               abs(self.rect.centery - enemy.rect.centerx) < TILE_SIZE * 2 :
                enemy.health -= 50
            


class Explosion(pygame.sprite.Sprite):
   def __init__(self, x, y, scale):
      pygame.sprite.Sprite.__init__(self)
      self.images = []
      for num in range (1,6):
         img = pygame.image.load(f"img/explosion/exp{num}.png").convert_alpha()
         img = pygame.transform.scale(img, (int(img.get_width()* scale * 3), int(img.get_height()* scale* 3)))
         self.images.append(img)
      self.frame_index = 0
      self.image = self.images[self.frame_index]
      self.rect = self.image.get_rect()
      self.rect.center = (x,y)
      self.counter = 0

   def update(self):
      EXPLOSION_SPEED = 4
      #update explosion animation
      self.counter += 1
      if self.counter >= EXPLOSION_SPEED:
         self.counter = 0
         self.frame_index += 1
         #if the animation is complete, delete animation
         if self.frame_index >= len(self.images):
            self.kill()
         else :
            self.image = self.images[self.frame_index]

#creating sprite group
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#temp - creating item box
item_box = ItemBox("health", 100,150)
item_box_group.add(item_box)
item_box = ItemBox("ammo", 300,500)
item_box_group.add(item_box)
item_box = ItemBox("grenade", 700,300)
item_box_group.add(item_box)

player = Character("player",100,500,0.3,7,20,5)
health_bar = HealthBar(10,10, player.health, player.health)

enemy = Character("enemy",300,425,0.4,3,100,0)
enemy_health_bar = HealthBar(700,10, enemy.health, enemy.health)
enemy_group.add(enemy)

run = True
while run :
    
    backsound.play()

    clock.tick(FPS)

    draw_bg()
    #show player health
    health_bar.draw(player.health)
    enemy_health_bar.draw(enemy.health)
    #show ammo
    draw_text("HP ", font, WHITE, 15, 11)
    draw_text("ENEMY HP ", font, WHITE, 700, 11)
    draw_text("AMMO = ", font, WHITE, 10, 35)
    for x in range(player.ammo):
       screen.blit(bullet_img, (90 + (x * 15), 30))
    #show grenades
    draw_text("GRENADE = ", font, WHITE, 10, 60)
    for x in range(player.grenades):
       screen.blit(grenade_img, (140 + (x * 25),60))

    player.update()
    player.draw()

    for enemy in enemy_group :
         enemy.ai()
         enemy.update() 
         enemy.draw()

    #update and draw groups
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()

    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)
    #update player action
    if player.alive :
       #shoot bullets
       if shoot :
          player.shoot()
       #throw grenade
       elif grenade and grenade_thrown == False and player.grenades > 0:
          grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] *player.direction),player.rect.top, player.direction)
          grenade_group.add(grenade)
          #reduces grenade
          player.grenades -= 1
          grenade_thrown = True
       if player.in_air :
          player.update_action(2) # 2. jump
       elif moving_left or moving_right:
          player.update_action(1) # 1.run
       else:
          player.update_action(0) # 0.idle
       player.move(moving_left,moving_right)

       # Check enemy bullets' collision with the player

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT :
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_a:
              moving_left = True
           if event.key == pygame.K_d:
              moving_right = True
           if event.key == pygame.K_SPACE:
              shoot = True
           if event.key == pygame.K_q:
              grenade = True
           if event.key == pygame.K_w and player.alive :
              player.jump = True
           if event.key == pygame.K_ESCAPE:
              run = False
        #keyboard button released
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_a:
              moving_left = False
           if event.key == pygame.K_d:
              moving_right = False
           if event.key == pygame.K_SPACE:
              shoot = False
           if event.key == pygame.K_q:
              grenade = False
              grenade_thrown = False
   
    pygame.display.update()

pygame.quit()