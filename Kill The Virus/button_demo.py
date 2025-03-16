import pygame

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

BLUE = (135,206,235)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,250,154)
BLACK = (0,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Button")

#load images
start_img = pygame.image.load("img/start_btn.png").convert_alpha()
exit_img = pygame.image.load("img/exit_btn.png").convert_alpha()

#button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#create button instances
start_button = Button(200,200, start_img, 0.8)
exit_button = Button(400,200, exit_img, 0.8)



#game loop
run = True
while run:

    screen.fill(BLUE)

    if start_button.draw():
        print("START")

    if exit_button.draw():
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()