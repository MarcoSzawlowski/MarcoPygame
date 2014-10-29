import pygame

from controls.human import *
from controls.cpu import *
from player.attack import *

class Players:
    # player_states:
    # -1: loading
    # 0: default standing
    # 1: jumping
    # 2: falling
    # 3: second jump
    # 4: falling without anymore jump
    # 5: hurt
    # 6: walking
    # 7: fast fall
    # 8: crouching (from standing still)
    # 9: ledge grab
    # 10: hurt (can't do input)
    # 11: attacking (can't do input, will have different animation depending on attack)

    def __init__(self, x, y, width, height, maxjump, lives, control, in_control):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.health = 0
        self.lives = lives
        self.debug_collision = 0
        self.maxjump = maxjump
        self.jumpcounter = 0
        self.ishurt = False
        self.width = width
        self.height = height
        self.yset_vel(3.6)
        self.facingright = 1
        self.maxfall = 9
        self.state = 0 #default standing state
        self.input = in_control
        self.attacks = Attack(self)
        self.type = control

        if control == "Human":
            self.controller = Human(self)
        else:
            self.controller = CPU(self, "jump")


    # Might need this later
    def handle_state(self, action):
        pass

    # Handle input
    def handle_input(self):
        self.controller.handle_input()

    # UPDATE:
    def update(self, collide_list):
        # Attack quick test:
        self.attacks.frame += 1
        if self.attacks.frame == 60:
            print("got here")
            self.attacks = Attack(self)

        # DO ACCELERATION FIRST
        if not self.state == 9:
            self.handle_movement()

        # Make a collision rectangle for the movement of the character
        horizontal = 0
        vertical = 0
        if self.velocity[0] > 0:
            horizontal = 1
            move_horizontal = pygame.Rect(self.position[0] + self.width, self.position[1], self.velocity[0], self.height)
        else:
            move_horizontal = pygame.Rect(self.position[0] + self.velocity[0], self.position[1], self.velocity[0], self.height)

        if self.velocity[1] > 0:
            vertical = 1
            move_vertical = pygame.Rect(self.position[0],self.position[1] + self.height, self.width, self.velocity[1])
        else:
            move_vertical = pygame.Rect(self.position[0],self.position[1] + self.velocity[1], self.width, self.velocity[1])

        # collidemap will return duple where first element is either true or false for collision and second element
        #  is the new position due to collision
        map_collision = self.collidemap_vertical(collide_list, move_vertical, vertical)

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
        if self.state == 0 or self.state == 9:
            self.state = 1
            self.acceleration[1] = -12
        elif self.state == 2:
            self.state = 3
            self.jumpcounter = self.maxjump
            self.acceleration[1] = -12

    # MOVEMENT: after jump finishes (either by jump counter running down or letting go of space)
    def unjump(self):
        self.jumpcounter = 0
        if self.state == 1:
            self.state = 2
        elif self.state == 3:
            self.state = 4
        self.acceleration[1] = 0

    # MOVEMENT: pressing down (either crouches or fast fall)
    def down(self):
        # for allowing drop when jumping if self.state == 1 or self.state == 2 or self.state == 3 or self.state == 4 or self.state == 8:
        if self.state == 2 or self.state == 4:
            self.state = 7
            self.maxfall = 24
            self.set_accel_y(15)
        elif self.state == 0:
            self.state = 8

    # MOVEMENT: set accel and velocities if needed
    def set_accel_x(self, value):
        self.acceleration[0] = value

    def set_accel_y(self, value):
        self.acceleration[1] = value

    def xset_vel(self, x):
        self.velocity[0] = x

    def yset_vel(self, y):
        self.velocity[1] = y

# DAMAGE: player takes damage, damage animation (handled in draw) and invulnerability for 1 second
    def hurt(self, amount):
        self.health += amount
        ishurt = True;
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

# Handle Movement:
    def handle_movement(self):
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
    # else make sure we aren't moving too fast (depending on if in air or on ground)
        else:
            self.velocity[0] += self.acceleration[0]
            if self.state == 2 or self.state == 4:
                speed_max = 6
            else:
                speed_max = 10
            if self.velocity[0] > speed_max:
                self.velocity[0] = speed_max
            elif self.velocity[0] < -speed_max:
                self.velocity[0] = -speed_max

        # now vertical (gravity)
        self.velocity[1] += 3

        # vertical other forces
        self.velocity[1] += self.acceleration[1]

        # make sure we aren't falling too fast
        if self.velocity[1] > self.maxfall:
            self.velocity[1] = self.maxfall

        #print(self.jumpcounter, " ", self.state, " ", self.velocity)
        # make sure we arent jumping too fast
        if self.state == 1 or self.state == 3:
            if self.velocity[1] < -20:
                self.velocity[1] = -20

# COLLISION WORLD: handles collisions with world map objects
    # Types
    #   0: Solid block
    #   1: one way block
    def collidemap_vertical(self, p, box, down):
        for plats in p:
            if box.colliderect(plats.box):
                # If player is falling down
                if down:
                    # If player is pressing down (go through one way blocks)
                    if self.state == 7 or self.state == 8:
                        if plats.type == 0:
                            self.state = 0
                            self.maxfall = 8
                            self.jumpcounter = self.maxjump
                            #self.yset_vel(6)
                            return (1, plats.position[1] - self.height)
                        else:
                            if self.state == 8:
                                self.state = 2
                            return(1, self.position[1] + plats.length)
                    else:
                        self.state = 0
                        self.maxfall = 8
                        self.jumpcounter = self.maxjump
                        #self.yset_vel(6)
                        return (1, plats.position[1] - self.height)
                # If player is going upwards
                else:
                    if plats.type == 0:
                        return (1, plats.position[1] + plats.length)
        if self.state == 0:
            self.state = 1
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
                        if box.colliderect(plats.top_left):
                            self.state = 9
                            self.position[1] = plats.position[1]
                            self.jumpcounter = self.maxjump
                            self.velocity = [0,0]
                        return (1, plats.position[0] - self.width)
                    else:
                        if box.colliderect(plats.top_right):
                            self.state = 9
                            self.position[1] = plats.position[1]
                            self.jumpcounter = self.maxjump
                            self.velocity = [0,0]
                        return (1, plats.position[0] + plats.width)
        return (0, 0)

    def attack(self, attack_type):
        # put it in an animation attacking state
        self.state = 11
        # put the attack frames inside the attack vector
        self.attacks = attack_type

    def draw(self, win):
        pass



