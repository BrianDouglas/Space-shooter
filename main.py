import pygame, random, os
import actor
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
player_img = pygame.image.load(os.path.join(asset_folder, "ship.png"))
player_bull_img = pygame.image.load(os.path.join(asset_folder, "player_bullet.png"))
all_sprites = pygame.sprite.Group()
player = actor.Player(player_img,(settings.WIDTH/2,settings.HEIGHT/2))
all_sprites.add(player)

#game loop
running = True
while running:
    #slows loop to our FPS
    clock.tick(settings.FPS)
    
                


    #directional movement controls. acceleration on key pressed, else decel
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

    #Process events (single press)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and keys[pygame.K_a]:
                player.altBlink("a")
            elif event.key == pygame.K_SPACE and keys[pygame.K_d]:
                player.altBlink("d")
            elif event.key == pygame.K_SPACE and keys[pygame.K_w]:
                player.altBlink("w")
            elif event.key == pygame.K_SPACE and keys[pygame.K_s]:
                player.altBlink("s")
            elif event.key == pygame.K_SPACE:
                player.altBlink("w")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = actor.Bullet(player_bull_img,player.rect.center,player.angle,5)
            all_sprites.add(bullet)

    #Update
    all_sprites.update()
    #Render
    screen.fill((125,125,125))
    all_sprites.draw(screen)
    player.playerStats(screen)
    
    pygame.display.flip() #after rendering everything, flip the display (double-buffering)

pygame.quit()
