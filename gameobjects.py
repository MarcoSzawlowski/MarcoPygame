__author__ = 'Marco'
import pygame
from random import randrange


class GameObject:
    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += 3.6

    def draw(self, win):
        pass

    def xset_vel(self, x):
        self.velocity[0] = x

    def yset_vel(self, y):
        self.velocity[1] = y


class Player(GameObject):

    def __init__(self, x, y, width, height, maxjump, lives):
        super().__init__(x, y)
        self.health = 0
        self.lives = lives
        self.debug_collision = 0
        self.inair = False
        self.isjump = False
        self.maxjump = maxjump
        self.jumpcounter = 0
        self.ishurt = False
        self.canjump = False
        self.width = width
        self.height = height
        self.yset_vel(3.6)
        self.facingright = 1

# MOVEMENT: SPACE TO JUMP
    def jump(self):
        self.isjump = True
        if self.canjump:
            self.yset_vel(-12.6)

    def unjump(self):
        #if self.jumpcounter <= self.maxjump and self.jumpcounter >= self.maxjump - 5:
          #  pass
       # else:
        self.isjump = False
        self.yset_vel(3.6)

# UPDATE:
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Change direction
        if (self.velocity[0] > 0):
            self.facingright = 1
        elif (self.velocity[0] < 0):
            self.facingright = 0

        # handle jumping
        if self.isjump:
            if self.jumpcounter < 0:
                self.canjump = False
                self.unjump()
            elif self.jumpcounter > 0 and self.jumpcounter < self.maxjump * 0.75:
                self.velocity[1] +=1
                self.jumpcounter -= 1
            else:
                self.jumpcounter -= 1

        # Death / Respawn
        if self.position[0] < -300 or self.position[1] < -300 or self.position[0] > 1580 or self.position[1] > 1080:
            self.die()
        #print("jumping: " + str(self.isjump) + "  In air: " + str(self.inair))

# DAMAGE: player takes damage, damage animation (handled in draw) and invulnerability for 1 second
    def hurt(self, amount):
        self.health += amount
        if self.health > 999:
            self.health = 999

# HEAL: player heals amount
    def heal(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

# DEATH: when player loses all health bars / instant death
    def die(self):
        print("You have died ")
        self.respawn()


# RESPAWN: will handle checkpoints
    def respawn(self):
        print("Respawning")
        self.position = [550, 400]

# COLLISION WORLD: handles collisions with world map objects
    def collide_map(self, p, win):
        playerbox = pygame.Rect(self.position[0],self.position[1],self.width,self.height)
        playerfeet = pygame.Rect(self.position[0],self.position[1],self.width,self.height)
        self.inair = True
        #print(self.jumpcounter)
        for plats in p:
            if plats.type == 0:
                if self.velocity[1] > 0 and playerbox.colliderect(plats.box):
                    self.inair = False
                    self.canjump = True
                    self.jumpcounter = self.maxjump
                    self.position[1] = plats.position[1] - self.height
            elif plats.type == 1:
                if self.velocity[1] > 0 and playerbox.colliderect(plats.box):
                    self.inair = False
                    self.canjump = True
                    self.jumpcounter = self.maxjump
                    self.position[1] = plats.position[1] - self.height

    def draw(self, win):
        # Figure out where we draw the person (either they are on screen or off)
        offscreen = 0

        if self.position[0] < 0 - self.width:
            offscreen = 1
            drawx = self.height / 2
        elif self.position[0] > 1280 + self.width:
            offscreen = 1
            drawx = 1280 - self.width - self.height / 2
        else:
            drawx = self.position[0]
            offscreen = 0 or offscreen

        if self.position[1] < 0 - self.height:
            offscreen = 1
            drawy = 20
        elif self.position[1] > 720 + self.height:
            offscreen = 1
            drawy = 720 - self.height - 20
        else:
            drawy = self.position[1]
            offscreen = 0 or offscreen



        # DRAW: face + face movement (probably will change for final game to sprites)
        x = drawx + 10
        y = drawy+ 10
        if (self.facingright):
            x += 5
        else:
            x-= 5

        if (self.velocity[0] > 0):
           x += 5
        elif (self.velocity[0] < 0):
            x -= 5
        if (self.velocity[1] > 0):
            y += 5
        elif (self.velocity[1] < 0):
            y -= 5

       # DRAW: body
        pygame.draw.rect(win, (0,0,0,50), (drawx,drawy,self.width,self.height), 0)

        # DRAW: head
        pygame.draw.rect(win, (0,255,0), (x,y,30,30), 0)

        # DRAW: hurt animation
        if (self.ishurt):
            if(self.hurtcounter == 0):
                self.ishurt = False
            elif (self.hurtcounter % 6 == 1):
                pygame.draw.rect(win, (0,0,0), (drawx,drawy,self.width,self.height), 0)
                self.hurtcounter -= 1
            else:
                self.hurtcounter -= 1

        # DRAW: offscreen bubble
        if offscreen:
            #print('got here')
            pygame.draw.circle(win, (200,0,0), (int(drawx + self.width/2), int(drawy + self.height/2)), int(self.height/2) + 20, 5)

class Platform(GameObject):

    def __init__(self, x, y, width, length, type):
        super().__init__(x, y)
        self.width = width
        self.length = length
        self.type = type
        self.box = pygame.Rect(self.position[0],self.position[1],self.width,self.length)

    def update(self):
        pass

    def draw(self, win):
        if self.type == 0:
            pygame.draw.rect(win, (0, 0, 0), self.box, 0)
        if self.type == 1:
            pygame.draw.rect(win, (100, 100, 100), self.box, 1)
