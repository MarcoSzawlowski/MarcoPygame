import sys
from player.players import *


class Human(Players):
    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.jump()
                    elif event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_s:
                        self.down()
                    elif event.key == pygame.K_a:
                        self.set_accel_x(-1)
                    elif event.key == pygame.K_d:
                        self.set_accel_x(1)
                    elif event.key == pygame.K_q:
                        self.hurt(25)
                    elif event.key == pygame.K_e:
                        self.heal(25, 0)
                    elif event.key == pygame.K_f:
                        self.debug_collision = not self.debug_collision
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_SPACE:
                        self.unjump()
                    elif event.key == pygame.K_s:
                        pass
                    elif event.key == pygame.K_a:
                        self.set_accel_x(0)
                    elif event.key == pygame.K_d:
                        self.set_accel_x(0)

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
                move_horizontal = pygame.Rect(self.position[0] + self.velocity[0], self.position[1], self.velocity[0] , self.height)

            if self.velocity[1] > 0:
                move_vertical = pygame.Rect(self.position[0],self.position[1] + self.height, self.width, self.velocity[1])
            else:
                move_vertical = pygame.Rect(self.position[0],self.position[1] + self.velocity[1], self.width, self.velocity[1])

            pygame.draw.rect(win,(255,50,50), move_vertical, 0)
            pygame.draw.rect(win,(50,250,50), move_horizontal, 0)