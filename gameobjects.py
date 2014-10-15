import pygame
from random import randrange


class GameObject:
    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.ishurt = False

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self, win):
        pass

    def xset_vel(self, x):
        print("x " + str(int((self.position[0] + 50)/40)))
        self.velocity[0] = x

    def yset_vel(self, y):
        print("Y " + str(int((self.position[1] + 50)/40)))
        self.velocity[1] = y


class Player(GameObject):
    maxhealth = 0
    health = 0

    def __init__(self, x, y, maxhealth):
        super().__init__(x, y)
        self.maxhealth = maxhealth
        self.health = maxhealth
        self.shift = 0
        self.shiftvalue = 2
        self.debug_collision = 0

# MOVEMENT: SHIFT KEY makes speed boost
    def update(self):
        if self.shift:
            self.position[0] += self.velocity[0] * self.shiftvalue
            self.position[1] += self.velocity[1] * self.shiftvalue
        else:
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]

# DAMAGE: player takes damage, damage animation (handled in draw) and invulnerability for 1 second
    def hurt(self, amount):
        self.health -= amount;
        if self.health < 0:
            self.health = 0
            self.die()
        self.ishurt = True;
        self.hurtcounter = 60;

# HEAL: player heals amount
    def heal(self, amount):
        self.health += amount;
        if self.health > self.maxhealth:
            self.health = self.maxhealth;

# DEATH: when player loses all health bars / instant death
    def die(self):
        print("You have died")

# RESPAWN: will handle checkpoints
    def respawn(self):
        print("Respawning")

# COLLISION WORLD: handles collisions with world map objects
    def collide_map(self, m, win):
        x = int(self.position[0]/40)
        y = int(self.position[1]/40)
        playerbox = pygame.Rect(self.position[0],self.position[1],50,50)

        # COLLISION: lists of collide objects in a 4 40x40 box radius around the player
        rectlist = []
        dangerlist = []
        dangerwalk = []

        # COLLISION: add collision boxes around player depending on the type of material on map grid
        if m[x][y] == 1:
            rectlist.append(pygame.Rect(x*40,y*40,40,40))
        elif m[x][y] == 2:
            dangerlist.append(pygame.Rect(x*40,y*40,40,40))
        elif m[x][y] == 3:
            dangerwalk.append(pygame.Rect(x*40,y*40,40,40))

        if m[x+1][y] == 1:
            rectlist.append(pygame.Rect((x+1)*40,y*40,40,40))
        elif m[x+1][y] == 2:
            dangerlist.append(pygame.Rect((x+1)*40,y*40,40,40))
        elif m[x+1][y] == 3:
            dangerwalk.append(pygame.Rect((x+1)*40,y*40,40,40))

        if m[x][y+1] == 1:
            rectlist.append(pygame.Rect(x*40,(y+1)*40,40,40))
        elif m[x][y+1] == 2:
            dangerlist.append(pygame.Rect(x*40,(y+1)*40,40,40))
        elif m[x][y+1] == 3:
            dangerwalk.append(pygame.Rect(x*40,(y+1)*40,40,40))

        if m[x+1][y+1] == 1:
            rectlist.append(pygame.Rect((x+1)*40,(y+1)*40,40,40))
        elif m[x+1][y+1] == 2:
            dangerlist.append(pygame.Rect((x+1)*40,(y+1)*40,40,40))
        elif m[x+1][y+1] == 3:
            dangerwalk.append(pygame.Rect((x+1)*40,(y+1)*40,40,40))


        if self.shift:
            mult = self.shiftvalue
        else:
            mult = 1

        if playerbox.collidelist(rectlist) > -1:
            self.position[0] -= self.velocity[0] * mult
            self.position[1] -= self.velocity[1] * mult
        elif playerbox.collidelist(dangerlist) > -1:
            self.position[0] -= self.velocity[0] * mult
            self.position[1] -= self.velocity[1] * mult
            if not self.ishurt:
                self.hurt(1)
        elif playerbox.collidelist(dangerwalk) > -1:
            if not self.ishurt:
                self.hurt(1)

    def draw(self, win):
        x = self.position[0] + 10
        y = self.position[1] + 10
        if (self.velocity[0] > 0):
           x += 10
        elif (self.velocity[0] < 0):
            x -= 10
        if (self.velocity[1] > 0):
            y += 10
        elif (self.velocity[1] < 0):
            y -= 10

       # DRAW: body
        pygame.draw.rect(win, (0,0,0,50), (self.position[0],self.position[1],50,50), 0)

        # DRAW: head
        if self.health == self.maxhealth:
            pygame.draw.rect(win, (0,255,0), (x,y,30,30), 0)
        elif self.health == 1:
            pygame.draw.rect(win, (255,0,0), (x,y,30,30), 0)
        elif self.health == 0:
            pygame.draw.rect(win, (100,100,100), (x,y,30,30), 0)
        else:
            pygame.draw.rect(win, (255 - (255/(self.maxhealth-self.health)),255 - (255/(self.health)),0), (x,y,30,30), 0)

        # DRAW: hurt animation
        if (self.ishurt):
            if(self.hurtcounter == 0):
                self.ishurt = False
            elif (self.hurtcounter % 6 == 1):
                pygame.draw.rect(win, (0,0,0), (self.position[0],self.position[1],50,50), 0)
                self.hurtcounter -= 1
            else:
                self.hurtcounter -= 1

        ## DEBUG: see collision boxes
        if self.debug_collision:
            x = int(self.position[0]/40)
            y = int(self.position[1]/40)
            pygame.draw.rect(win, (255,0,0), ((x+1)*40,y*40,40,40), 3)
            pygame.draw.rect(win, (0,255,0), (x*40,(y+1)*40,40,40), 3)
            pygame.draw.rect(win, (30,30,255), ((x+1)*40,(y+1)*40,40,40), 3)
            pygame.draw.rect(win, (200,30,200), (x*40,y*40,40,40), 3)