import pygame
import button

pygame.init()

FPS = 60
clock = pygame.time.Clock()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 7
current_tile = 0

#define colour 
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,250,154)
BLACK = (0,0,0)

#define game variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images
lab = pygame.image.load("img/background/final.jpeg").convert_alpha()
img_list= []
for x in range (TILE_TYPES):
    img = pygame.image.load(f"img/tiles/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
    
#create empty tile list
world_data = []
for row in range (ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0

#create function for drawing background
def draw_bg():
    width = lab.get_width()
    screen.fill(GREEN)
    for x in range (4):
        screen.blit(lab,((x * width)-scroll * 0.5,0))

def draw_grid():
    #vertical lines
    for c in range(MAX_COLS):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE) )


#create button 
button_list = []
button_col = 0
button_row = 0
for i in range (len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col)+ 50, 75 * button_row + 50, img_list[i],1)
    button_list.append(tile_button)
    button_col =+ 1
    if button_col == 1:
        button_row += 1
        button_col = 0

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    #draw tile panel
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0 , SIDE_MARGIN, SCREEN_HEIGHT))

    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
       if i.draw(screen):
           current_tile = button_count

    #highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)
    

    #scroll the map
    if scroll_left == True:
        scroll -= 5 * scroll_speed
    if scroll_right == True:
        scroll += 5 * scroll_speed

    #add tile to the screen
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll // TILE_SIZE)
    y = pos[1] // TILE_SIZE

    #check thar coordinate are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
               world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[0] == 1:
                world_data[y][x] =  -1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
