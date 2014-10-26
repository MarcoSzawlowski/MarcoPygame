import pygame
from player.players import *


class Human(Players):

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

    def set_accel(self, value):
        self.acceleration[0] = value

# UPDATE:
    def update(self, collide_list):
        # DO ACCELERATION FIRST
        if (self.acceleration[0] == 0):
            if self.velocity[0] > 0:
                self.velocity[0] -= 1
                if self.velocity[0] <= 0:
                    self.velocity[0] = 0
            elif self.velocity[0] < 0:
                self.velocity[0] += 1
                if self.velocity[0] >= 0:
                    self.velocity[0] = 0
        else:
            self.velocity[0] += self.acceleration[0]
            if self.velocity[0] > 12:
                self.velocity[0] = 12
            elif self.velocity[0] < -12:
                self.velocity[0] = -12

        # Make a collision rectangle for the movement of the character
        horizontal = 0
        vertical = 0
        if self.velocity[0] > 0:
            horizontal = 1
            move_horizontal = pygame.Rect(self.position[0] + self.width, self.position[1], self.velocity[0], self.height)
        else:
            move_horizontal = pygame.Rect(self.position[0] - self.velocity[0], self.position[1], self.velocity[0], self.height)

        if self.velocity[1] > 0:
            vertical = 1
            move_vertical = pygame.Rect(self.position[0],self.position[1] + self.height, self.width, self.velocity[1])
        else:
            move_vertical = pygame.Rect(self.position[0],self.position[1] - self.velocity[1], self.width, self.velocity[1])

        map_collision = self.collidemap_vertical(collide_list, move_vertical, vertical)

        # collidemap will return duple where first element is either true or false for collision
        if map_collision[0]:
            self.position[1] = map_collision[1]
        else:
            self.position[1] += self.velocity[1]

        map_collision = self.collidemap_horizontal(collide_list, move_horizontal, horizontal)

        if map_collision[0]:
            self.position[0] = map_collision[1]
            print(self.position[0])
        else:
            self.position[0] += self.velocity[0]


        # Determine direction
        if (self.velocity[0] > 0):
            self.facingright = 1
        elif (self.velocity[0] < 0):
            self.facingright = 0

        # Handle jumping
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
    def heal(self, amount, type):
        self.health -= amount
        if self.health < 0:
            self.health = 0

# DEATH: when player loses all health bars / instant death
    def die(self):
        print("You have died ")
        self.lives -= 1
        if self.lives < 1:
            self.lives = 0
            print('Game OVER')
        self.respawn()


# RESPAWN: will handle checkpoints
    def respawn(self):
        print("Respawning")
        self.position = [550, 400]

# COLLISION WORLD: handles collisions with world map objects
    # Types
    #   0: Solid block
    #   1: one way block
    def collidemap_vertical(self, p, box, down):
        self.inair = True
        for plats in p:
            if (plats.type == 0 or plats.type == 1) and down:
                if box.colliderect(plats.box):
                    self.inair = False
                    self.canjump = True
                    self.jumpcounter = self.maxjump
                    self.yset_vel(6)
                    return (1, plats.position[1] - self.height)
            elif down == 0 and plats.type == 0:
                if box.colliderect(plats.box):
                    return (1, plats.position[1] + plats.length)
        return (0, 0)

    def collidemap_horizontal(self, p, box, right):
        #self.inair = True
        for plats in p:
             if plats.type == 0:
                 if box.colliderect(plats.box):
                    #self.inair = False
                    #self.canjump = True
                    #self.jumpcounter = self.maxjump
                    if right:
                        return (1, plats.position[0] - self.width)
                    else:
                        print(plats.position[0] + plats.width)
                        return (1, plats.position[0] + plats.width)
        return (0, 0)

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

        # DRAW: off-screen bubble around a player view
        if offscreen:
            pygame.draw.circle(win, (200,0,0), (int(drawx + self.width/2), int(drawy + self.height/2)), int(self.height/2) + 20, 5)

        if self.debug_collision:
            if self.velocity[0] > 0:
                move_horizontal = pygame.Rect(self.position[0] + self.width, self.position[1], self.velocity[0], self.height)
            else:
                move_horizontal = pygame.Rect(self.position[0] - self.velocity[0], self.position[1], self.velocity[0], self.height)

            if self.velocity[1] > 0:
                vertical = 1
                move_vertical = pygame.Rect(self.position[0],self.position[1] + self.height, self.width, self.velocity[1])
            else:
                move_vertical = pygame.Rect(self.position[0],self.position[1] - self.velocity[1], self.width, self.velocity[1])

            pygame.draw.rect(win,(255,50,50), move_vertical, 0)
            pygame.draw.rect(win,(50,250,50), move_horizontal, 0)