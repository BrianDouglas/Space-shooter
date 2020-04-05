import pygame, random, os
import player



#our configuration constants
WIDTH = 800 #game window dimensions
HEIGHT = 400 #game window dimensions
FPS = 30 #framerate
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PLAYER_ACCEL = 4

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

#set up asset folders and player img
game_folder = os.path.dirname(__file__)
asset_folder = os.path.join(game_folder, "assets")
player_img = pygame.image.load(os.path.join(asset_folder, 'ship.png'))

all_sprites = pygame.sprite.Group()
player = player.Player(player_img,(WIDTH/2,HEIGHT/2))
all_sprites.add(player)

#game loop
running = True
while running:
    #slows loop to our FPS
    clock.tick(FPS)
    #Process input
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.control(-PLAYER_ACCEL,0)
    if keys[pygame.K_d]:
        player.control(PLAYER_ACCEL,0)
    if keys[pygame.K_s]:
        player.control(0,PLAYER_ACCEL)
    if keys[pygame.K_w]:
        player.control(0,-PLAYER_ACCEL)
    #Update
    all_sprites.update()
    #Render
    screen.fill((125,125,125))
    player.playerStats(screen)
    all_sprites.draw(screen)
    
    pygame.display.flip() #after rendering everything, flip the display (double-buffering)

pygame.quit()
