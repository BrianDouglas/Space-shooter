import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image #required by parent
        self.OG_image = image
        self.rect = self.image.get_rect() #required by parent
        self.rect.center = (location)
        self.vel_x = 0
        self.vel_y = 0
        self.accel_x = 0
        self.accel_y = 0
        self.frame = 0
        self.angle = 0
        self.font = pygame.font.Font('freesansbold.ttf',12)
        

    def update(self): #required def from parent
        self.rotate()
        self.rect.x = self.rect.x + self.vel_x
        self.rect.y = self.rect.y + self.vel_y
        if self.rect.right < 0:
            self.rect.left = 800
        if self.rect.left > 800:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = 400
        if self.rect.top > 400:
            self.rect.bottom = 0
        
        ###move version 1 code:
        #self.vel_x = 0
        #self.vel_y = 0

    def control(self,x,y):
        #increase velocity by acceleration sent
        self.accel_x = x
        self.accel_y = y
        self.vel_y += self.accel_y
        self.vel_x += self.accel_x
        ###move version 1 code:
        #self.vel_x = x
        #self.vel_y = y
        
        ###cursor movement experiment
        #self.rect.center = (self.rect.center[0] + (math.cos(self.angle) * self.vel_x), self.rect.center[1] - (math.sin(self.angle) * self.vel_y))

        if abs(self.vel_y) > 5:
            self.vel_y -= y
        if abs(self.vel_x) >= 5:
            self.vel_x -= x

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        self.angle = int((180 / math.pi) * -math.atan2(rel_y, rel_x)) - 90
        self.image = pygame.transform.rotate(self.OG_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        
    def playerStats(self,screen):
        stats = self.font.render(f"Position: ({self.rect.x} ,{self.rect.y}) Velocity: ({round(self.vel_x, 2)} ,{round(self.vel_y,2)})   Angle: {self.angle}",True,(0,255,0))
        screen.blit(stats, (10,10))
        
        