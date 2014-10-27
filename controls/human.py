import sys
import pygame
from player.characters import *
from controls.controller import *


class Human(Controller):
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
                        self.mychar.jump()
                    elif event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_s:
                        self.mychar.down()
                    elif event.key == pygame.K_a:
                        self.mychar.set_accel_x(-1)
                    elif event.key == pygame.K_d:
                        self.mychar.set_accel_x(1)
                    elif event.key == pygame.K_q:
                        self.mychar.hurt(25)
                    elif event.key == pygame.K_e:
                        self.mychar.heal(25, 0)
                    elif event.key == pygame.K_f:
                        self.mychar.debug_collision = not self.char.debug_collision
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_SPACE:
                        self.mychar.unjump()
                    elif event.key == pygame.K_s:
                        pass
                    elif event.key == pygame.K_a:
                        self.mychar.set_accel_x(0)
                    elif event.key == pygame.K_d:
                        self.mychar.set_accel_x(0)