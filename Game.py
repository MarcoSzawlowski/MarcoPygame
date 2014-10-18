__author__ = 'Marco'
import pygame
import sys
from gameobjects import *


class Game():
    gameObjects = []
    win = None
    clock = None
    time = 0
    grid = []
    platforms = []

    def __init__(self, window, clock):
        self.win = window
        self.win.fill((250, 250, 250))
        self.clock = clock
        self.debug_map = False
        self.font = pygame.font.Font(None, 100)
        ## gameObjects[0] IS ALWAYS THE PLAYER
        self.gameObjects.append(Player(550, 400, 50, 100, 40, 3))

        self.platforms.append(Platform(300,500,1500,100,0))
        self.platforms.append(Platform(500,300,400,10,1))
        self.platforms.append(Platform(500,100,400,10,1))
        self.platforms.append(Platform(-200,1000,700,10,1))

    def gameloop(self):
        while True:
            # GAME: 60tick, update and draw n (60 for now) times a second
            self.time += self.clock.tick(60)

            # CONTROLS: main event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.gameObjects[0].jump()
                    elif event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_s:
                        self.gameObjects[0].yset_vel(12)
                    elif event.key == pygame.K_a:
                        self.gameObjects[0].xset_vel(-6)
                    elif event.key == pygame.K_d:
                        self.gameObjects[0].xset_vel(6)
                    elif event.key == pygame.K_q:
                        self.gameObjects[0].hurt(25)
                    elif event.key == pygame.K_e:
                        self.gameObjects[0].heal(25)
                    elif event.key == pygame.K_f:
                        self.gameObjects[0].debug_collision = not self.gameObjects[0].debug_collision
                        self.debug_map = not self.debug_map
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_SPACE:
                        self.gameObjects[0].unjump()
                    elif event.key == pygame.K_s:
                        pass
                    elif event.key == pygame.K_a:
                        self.gameObjects[0].xset_vel(0)
                    elif event.key == pygame.K_d:
                        self.gameObjects[0].xset_vel(0)
            # GAME: call all important updates and draw methods
            self.update()
            self.draw()

            # DISPLAY: update the screen
            pygame.display.update()

    def update(self):
        for objects in self.gameObjects:
            objects.update()

        for plats in self.platforms:
            plats.update()

        self.gameObjects[0].collide_map(self.platforms, self.win)

    def draw(self):

        # DISPLAY: clear the screen
        self.win.fill((250, 250, 250))

        # DISPLAY: Draw all the game objects now
        for objects in self.gameObjects:
            objects.draw(self.win)

        # DISPLAY: Draw platforms and stages
        for plats in self.platforms:
            plats.draw(self.win)

        # DISPLAY: Health / Lives
        offset_players = 0
        for players in self.gameObjects:
            offset_players += 100
            offset_lives = 0
            playerpercent = self.font.render(str(players.health) + "%", 1, (0,0,0))
            self.win.blit(playerpercent, (offset_players, 720 - 120))
            for i in range(0,players.lives):
                pygame.draw.circle(self.win, (0,100,100), (offset_players + offset_lives, 720 - 160), 20, 0)
                offset_lives += 40