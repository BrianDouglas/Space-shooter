import pygame
import math
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image #required by parent
        self.OG_image = image
        self.rect = self.image.get_rect() #required by parent
        self.rect.center = (location)
        self.vel_cap = 10
        self.speed_cap = math.hypot(self. vel_cap,self.vel_cap)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 0
        self.accel_rate = 0.5
        self.accel_x = 0
        self.accel_y = 0
        self.frame = 0
        self.angle = 0 #this is in radians
        self.blink_distance = 100
        self.blink_charge_rate = 2
        self.blink_charge_max = 500
        self.blink_charge = self.blink_charge_max
        self.font = pygame.font.Font('freesansbold.ttf',12)
        

    def update(self): #required def from parent
        self.rotate() #rotate the ship based on mouse position
        self.rect.center = (self.rect.center[0] + self.vel_x, self.rect.center[1] + self.vel_y) #update ship position
        #check for chip exiting the screen
        if self.rect.right < 0:
            self.rect.left = settings.WIDTH - 1
        if self.rect.left > settings.WIDTH:
            self.rect.right = 1
        if self.rect.bottom < 0:
            self.rect.top = settings.HEIGHT - 1
        if self.rect.top > settings.HEIGHT:
            self.rect.bottom = 1
        #recharge blink
        if self.blink_charge < self.blink_charge_max:
            self.blink_charge += self.blink_charge_rate

    def velCap(self): ###need to update to account for angular velocity###
        #control for max speed
        if self.speed > self.speed_cap:
            self.vel_x = self.vel_x/abs(self.speed) * self.speed_cap
            self.vel_y = self.vel_y/abs(self.speed) * self.speed_cap
        #if abs(self.vel_y) > self.vel_cap:
            #self.vel_y = self.vel_y/abs(self.vel_y) * self.vel_cap
        #if abs(self.vel_x) >= self.vel_cap:
            #self.vel_x = self.vel_x/abs(self.vel_x) * self.vel_cap

    def decel(self,axis):
        if axis == "x":
            self.vel_x *= 0.98
            if -0.5 < self.vel_x < 0:
                self.vel_x = 0
        if axis == "y":
            self.vel_y *= 0.98
            if -0.5 < self.vel_y < 0:
                self.vel_y = 0

    def control(self,x,y):
        #based on positive, negate or 0 sent
        if x == 1:
            self.accel_x = self.accel_rate
        elif x == -1:
            self.accel_x = -self.accel_rate
        else:
            self.accel_x = 0
        if y == 1:
            self.accel_y = self.accel_rate
        elif y == -1:
            self.accel_y = -self.accel_rate
        else:
            self.accel_y = 0
        self.vel_y += self.accel_y
        self.vel_x += self.accel_x
        self.speed = math.hypot(self.vel_x, self.vel_y)

        self.velCap()

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        self.angle = math.atan2(-rel_y, rel_x) % (2*math.pi)
        self.image = pygame.transform.rotate(self.OG_image, math.degrees(self.angle) - 90)
        self.rect = self.image.get_rect(center = self.rect.center)

    def blink(self): #blink towards cursor
        if (self.blink_charge - self.blink_distance) > 0:
            self.rect.center = (self.rect.center[0] + (math.cos(self.angle) * self.blink_distance), self.rect.center[1] - (math.sin(self.angle) * self.blink_distance))
            self.blink_charge -= self.blink_distance

    def altBlink(self,direction): #blink on direction pressed
        if (self.blink_charge - self.blink_distance) > 0:
            if direction == "a":
                self.rect.center = ((self.rect.center[0] - self.blink_distance), self.rect.center[1])
            elif direction == "d":
                self.rect.center = ((self.rect.center[0] + self.blink_distance), self.rect.center[1])
            elif direction == "w":
                self.rect.center = (self.rect.center[0], (self.rect.center[1] - self.blink_distance))
            elif direction == "s":
                self.rect.center = (self.rect.center[0], (self.rect.center[1] + self.blink_distance))
            self.blink_charge -= self.blink_distance

    def playerStats(self,screen):
        #debug data
        stats = self.font.render(f"Position: ({self.rect.x} ,{self.rect.y})    Velocity: ({round(math.hypot(self.vel_x,self.vel_y), 2)})    Accel: ({self.accel_x},{self.accel_y})   Angle: {round(math.degrees(self.angle),2)}   BlinkCharge: {self.blink_charge}",True,(0,255,0))
        #blink bar
        blink_charge_percent = self.blink_charge / self.blink_charge_max
        blink_bar_length = settings.WIDTH - 20
        blink_bar_tick_offset = (self.blink_distance / self.blink_charge_max) * blink_bar_length
        pygame.draw.rect(screen, settings.BLUE,(10, settings.HEIGHT - 20, (blink_bar_length)*blink_charge_percent, 20),0)
        for i in range(int(self.blink_charge_max/self.blink_distance)):
            pygame.draw.line(screen, settings.GREEN, (10 + blink_bar_tick_offset*(i+1), settings.HEIGHT - 20),(10 + blink_bar_tick_offset*(i+1), settings.HEIGHT))
        screen.blit(stats, (10,10))
        
        