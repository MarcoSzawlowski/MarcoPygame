import sys
import pygame
from player.characters import *
from controls.controller import *
from pygame.locals import *


class Human(Controller):
    def handle_input(self):
        using_controller = True
        if (using_controller):
            self.handle_controller()
        else:
            self.handle_keyboard()

    def handle_controller(self):
        #print(self.mychar.input.get_name())
        deadzone = 0.25
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == JOYAXISMOTION:
                    # 0: x axis left stick (-1.0 to 1.0)
                    # 1: y axis left stick (-1.0 to 1.0)
                    # 2: -1.0 to 0 is right trigger, 0.0 to 1.0 is left trigger
                    if event.axis == 0:
                        #print (' axis 0', event.value)
                        if event.value > deadzone:
                            self.mychar.set_accel_x(event.value)
                        elif event.value < -deadzone:
                            self.mychar.set_accel_x(event.value)
                        else:
                            self.mychar.set_accel_x(0)
                    elif event.axis == 1:
                        print(' axis 1', event.value)
                        if event.value > deadzone + 0.70:
                            self.mychar.down()
                        elif event.value < -deadzone:
                            pass
                        else:
                            pass
                    elif event.axis == 2:
                        pass
                        #print (' axis 2', event.value)
                    elif event.axis == 3:
                        pass
                        #print (' axis 3', event.value)
                    elif event.axis == 4:
                        pass
                        #print (' axis 4', event.value)
                elif event.type == JOYBUTTONDOWN:
                    # button 0: a
                    # button 1: b
                    # button 2: x
                    # button 3: y
                    # button 4: lb
                    # button 5: rb
                    # button 6: select
                    # button 7: start
                    #print ("Joystick '", event.type,"' button",event.button,"up.")
                    if event.button == 0:
                        pass
                    elif event.button == 1:
                        pass
                    elif event.button == 2 or event.button == 3:
                        self.mychar.jump()
                elif event.type == JOYBUTTONUP:
                    #print ("Joystick '", event.type,"' button",event.button,"up.")
                    if event.button == 0:
                        pass
                    elif event.button == 1:
                        pass
                    elif event.button == 2 or event.button == 3:
                        self.mychar.unjump()
                elif event.type == JOYHATMOTION:
                    print ("Joystick hat",event.value," moved.")

    def handle_keyboard(self):
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
                        self.mychar.debug_collision = not self.mychar.debug_collision
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