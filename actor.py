'''
Contains the Actor class which is a child of pygame.sprite.Sprite
The actor class is for all objects in game which move and are displayed in the game
Actor has several sub classes:
-Bullet
-Player
-*more to come*
alsdfkja;sldfk
'''

import pygame
import math
import settings

class Actor(pygame.sprite.Sprite):
    def __init__(self,image,location,angle=0,speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.OG_image = image
        self.rect = self.image.get_rect()
        self.rect.center = (location)
        self.angle = angle
        self.velocity = pygame.math.Vector2((speed*math.cos(angle),-speed*math.sin(angle)))

    def update(self):
        pass

    def rotateTo(self,angle):
        self.image = pygame.transform.rotate(self.OG_image, angle)
        self.rect = self.image.get_rect(center = self.rect.center)

class Bullet(Actor):
    def __init__(self,image,location,angle,speed = 20):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.OG_image = image
        self.rect = self.image.get_rect()
        self.rect.center = (location)
        self.float_pos = pygame.math.Vector2(location) #for accuracy
        self.angle = angle
        self.velocity = pygame.math.Vector2((speed*math.cos(angle),-speed*math.sin(angle)))
        self.rotateTo(math.degrees(self.angle) - 90)
        print(self.velocity)

    def update(self):
        self.float_pos += self.velocity #add to float position for accuracy
        self.rect.center = self.float_pos #rect.center converts to INT

        if self.rect.right < 0:
            print("bullet dead")
            self.kill()
        if self.rect.left > settings.WIDTH:
            print("bullet dead")
            self.kill()
        if self.rect.bottom < 0:
            print("bullet dead")
            self.kill()
        if self.rect.top > settings.HEIGHT:
            print("bullet dead")
            self.kill()


class Player(Actor):
    def __init__(self,image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image #required by sprite
        self.OG_image = image
        self.rect = self.image.get_rect() #required by sprite
        self.rect.center = (location)
        self.vel_cap = 10
        self.speed_cap = math.hypot(self. vel_cap,self.vel_cap)
        self.velocity = pygame.math.Vector2(0,0)
        self.speed = 0
        self.accel_rate = 0.5
        self.accel = pygame.math.Vector2(0,0)
        self.accel_x = 0
        self.accel_y = 0
        self.frame = 0
        self.angle = 0 #this is in radians
        self.blink_distance = 100
        self.blink_charge_rate = 2
        self.blink_charge_max = 500
        self.blink_charge = self.blink_charge_max
        self.font = pygame.font.Font('freesansbold.ttf',12)
        

    def update(self): #required def from sprite
        self.calcAngleToMouse()
        self.rotateTo(math.degrees(self.angle) - 90) 
        self.rect.center += self.velocity #update ship position
        #check for ship exiting the screen
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

    def velCap(self):
        #control for max speed
        if self.speed > self.speed_cap:
            self.velocity.x = self.velocity.x/abs(self.speed) * self.speed_cap
            self.velocity.y = self.velocity.y/abs(self.speed) * self.speed_cap

    def decel(self,axis):
        if axis == "x":
            self.velocity.x *= 0.98
            if -0.5 < self.velocity.x < 0:
                self.velocity.x = 0
        if axis == "y":
            self.velocity.y *= 0.98
            if -0.5 < self.velocity.y < 0:
                self.velocity.y = 0

    def control(self,x,y):
        #based on positive, negate or 0 sent
        if x == 1:
            self.accel.x = self.accel_rate
        elif x == -1:
            self.accel.x = -self.accel_rate
        else:
            self.accel.x = 0
        if y == 1:
            self.accel.y = self.accel_rate
        elif y == -1:
            self.accel.y = -self.accel_rate
        else:
            self.accel.y = 0
        self.velocity += self.accel
        self.speed = self.velocity.magnitude()


        self.velCap()

    def calcAngleToMouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        self.angle = math.atan2(-rel_y, rel_x) % (2*math.pi)

    def blink(self): #blink towards cursor
        if (self.blink_charge - self.blink_distance) > 0:
            self.rect.center = (
                self.rect.center[0] + (math.cos(self.angle) * self.blink_distance), 
                self.rect.center[1] - (math.sin(self.angle) * self.blink_distance)
                )
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
        debug_str = "off" #f"Position: ({self.rect.x} ,{self.rect.y})    Velocity: ( {self.velocity.magnitude()} )    Accel: ({self.accel.magnitude()})   Angle: {round(math.degrees(self.angle),2)}   BlinkCharge: {self.blink_charge}"
        stats = self.font.render(debug_str, True, settings.GREEN) 
        #blink bar
        blink_charge_percent = self.blink_charge / self.blink_charge_max
        blink_bar_length = settings.WIDTH - 20
        blink_bar_tick_offset = (self.blink_distance / self.blink_charge_max) * blink_bar_length
        pygame.draw.rect(
            screen, 
            settings.BLUE,
            (10, settings.HEIGHT - 20, (blink_bar_length)*blink_charge_percent, 20), #x,y,w,h
            0
            )
        for i in range(int(self.blink_charge_max/self.blink_distance)):
            pygame.draw.line(
                screen, 
                settings.GREEN, 
                (10 + blink_bar_tick_offset*(i+1), settings.HEIGHT - 20),
                (10 + blink_bar_tick_offset*(i+1), settings.HEIGHT)
            )
        screen.blit(stats, (10,10))
        
        