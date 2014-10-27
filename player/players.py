import pygame

class Players:
    def __init__(self, x, y, width, height, maxjump, lives):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
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
        self.maxfall = 9
        self.state = 0 #default standing state

    # UPDATE:
    # player_states:
    # 0: default standing
    # 1: jumping
    # 2: falling
    # 3: second jump
    # 4: falling without anymore jump
    # 5: hurt
    # 6: walking
    # 7: fast fall

    def handle_state(self, action):
        pass


    def update(self, collide_list):

        # DO ACCELERATION FIRST

        # if the player is just coming to a stop without movement, we want them to decelerate naturally (friction)
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
            if self.state == 2 or self.state == 4:
                speed_max = 8
            else:
                speed_max = 12
            if self.velocity[0] > speed_max:
                self.velocity[0] = speed_max
            elif self.velocity[0] < -speed_max:
                self.velocity[0] = -speed_max

        # now vertical (gravity)
        self.velocity[1] += 1

        # vertical other forces
        self.velocity[1] += self.acceleration[1]

        # make sure we aren't falling too fast
        if self.velocity[1] > self.maxfall:
            self.velocity[1] = self.maxfall

        print(self.jumpcounter, " ", self.state)
        # make sure we arent jumping too fast
        if self.state == 1 or self.state == 3:
            if self.velocity[1] < -15:
                self.velocity[1] = -15

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
        if self.state == 1 or self.state == 3:
            if self.jumpcounter < 0:
                self.unjump()
            else:
                self.jumpcounter -= 5

        # Death / Respawn
        if self.position[0] < -300 or self.position[1] < -300 or self.position[0] > 1580 or self.position[1] > 1080:
            self.die()
        #print("jumping: " + str(self.isjump) + "  In air: " + str(self.inair))

    # MOVEMENT: SPACE TO JUMP
    def jump(self):
        if self.state == 0:
            self.state = 1
            self.acceleration[1] = -7
        elif self.state == 2:
            self.state = 3
            self.jumpcounter = self.maxjump
            self.acceleration[1] = -7

    def unjump(self):
        self.jumpcounter = 0
        if self.state == 1:
            self.state = 2
        elif self.state == 3:
            self.state = 4
        self.acceleration[1] = 0

    def down(self):
        if self.state == 1 or self.state == 2 or self.state == 3 or self.state == 4:
            self.state = 7
            self.maxfall = 24
            self.set_accel_y(15)
        elif self.state == 0:
            self.state = 8

    def set_accel_x(self, value):
        self.acceleration[0] = value

    def set_accel_y(self, value):
        self.acceleration[1] = value

    def draw(self, win):
        pass

    def xset_vel(self, x):
        self.velocity[0] = x

    def yset_vel(self, y):
        self.velocity[1] = y

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
        self.state = 0
        self.position = [550, 400]

# COLLISION WORLD: handles collisions with world map objects
    # Types
    #   0: Solid block
    #   1: one way block
    def collidemap_vertical(self, p, box, down):
        for plats in p:
            if box.colliderect(plats.box):
                if down:
                    # If player is pressing down
                    if self.state == 7 or self.state == 8:
                        if plats.type == 0:
                            self.state = 2
                            self.maxfall = 8
                            self.jumpcounter = self.maxjump
                            self.yset_vel(6)
                            return (1, plats.position[1] - self.height)
                    else:
                        self.state = 0
                        self.maxfall = 8
                        self.jumpcounter = self.maxjump
                        self.yset_vel(6)
                        return (1, plats.position[1] - self.height)
                else:
                    if plats.type == 0:
                        print("underddd")
                        return (1, plats.position[1] + plats.length + 1)

        # player just walked off edge
        if self.state == 0:
            self.state = 2
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

