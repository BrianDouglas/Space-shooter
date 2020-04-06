import pygame, random, os
import player
import settings

settings.init()

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

#set up asset folders and player img
game_folder = os.path.dirname(__file__)
asset_folder = os.path.join(game_folder, "assets")
player_img = pygame.image.load(os.path.join(asset_folder, 'ship.png'))

all_sprites = pygame.sprite.Group()
player = player.Player(player_img,(settings.WIDTH/2,settings.HEIGHT/2))
all_sprites.add(player)

#game loop
running = True
while running:
    #slows loop to our FPS
    clock.tick(settings.FPS)
    #Process input
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False

    #directional movement controls
    #acceleration on key pressed, else decel
    keys = pygame.key.get_pressed()
    #right left control
    if keys[pygame.K_a]:
        player.control(-1,0)
    elif keys[pygame.K_d]:
        player.control(1,0)
    else:
        player.decel("x")
    #up down control
    if keys[pygame.K_s]:
        player.control(0,1)
    elif keys[pygame.K_w]:
        player.control(0,-1)
    else:
        player.decel("y")
    
    #blink when space is pressed
    if keys[pygame.K_SPACE]:
        player.blink()

    #Update
    all_sprites.update()
    #Render
    screen.fill((125,125,125))
    player.playerStats(screen)
    all_sprites.draw(screen)
    
    pygame.display.flip() #after rendering everything, flip the display (double-buffering)

pygame.quit()
