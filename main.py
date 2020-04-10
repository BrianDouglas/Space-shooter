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

#set up asset folder
game_folder = os.path.dirname(__file__)
asset_folder = os.path.join(game_folder, "assets")

#load images
player_img = pygame.image.load(os.path.join(asset_folder, "ship.png"))
player_bull_img = pygame.image.load(os.path.join(asset_folder, "player_bullet.png"))
fence_corner_img = pygame.image.load(os.path.join(asset_folder, "fence_pylon.png"))
fence_vertical_img = pygame.image.load(os.path.join(asset_folder, "fence1.png"))
fence_horizontal_img = pygame.transform.rotate(fence_vertical_img, 90)

#creats sprite group
all_sprites = pygame.sprite.Group()

#create and add to group
player = actor.Player(player_img,(settings.WIDTH/2,settings.HEIGHT/2))
all_sprites.add(player)
#the fence pieces
fence_corner_NE = actor.Actor(fence_corner_img,(settings.WIDTH - 10, 10))
all_sprites.add(fence_corner_NE)

fence_corner_NW = actor.Actor(fence_corner_img,(10, 10))
fence_corner_NW.rotateTo(90)
all_sprites.add(fence_corner_NW)

fence_corner_SW = actor.Actor(fence_corner_img,(10, settings.HEIGHT-30))
fence_corner_SW.rotateTo(180)
all_sprites.add(fence_corner_SW)

fence_corner_SE = actor.Actor(fence_corner_img,(settings.WIDTH - 10, settings.HEIGHT-30))
fence_corner_SE.rotateTo(270)
all_sprites.add(fence_corner_SE)

for i in range(30, settings.HEIGHT - 30,20):
    fence_segment = actor.Actor(fence_vertical_img,(10,i))
    all_sprites.add(fence_segment)
    fence_segment = actor.Actor(fence_vertical_img,(settings.WIDTH - 10,i))
    all_sprites.add(fence_segment)

for i in range(30, settings.WIDTH - 20, 20):
    fence_segment = actor.Actor(fence_horizontal_img,(i, 10))
    all_sprites.add(fence_segment)
    fence_segment = actor.Actor(fence_horizontal_img,(i, settings.HEIGHT - 30))
    all_sprites.add(fence_segment)
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
            bullet = actor.Bullet(player_bull_img, player.rect.center, player.angle)
            all_sprites.add(bullet)

    #Update
    all_sprites.update()
    #Render
    screen.fill((125,125,125))
    all_sprites.draw(screen)
    player.playerStats(screen)
    
    pygame.display.flip() #after rendering everything, flip the display (double-buffering)

pygame.quit()
