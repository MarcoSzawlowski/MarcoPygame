import pygame
import sys
from gameobjects import *


class Game():
    gameObjects = []
    win = None
    clock = None
    time = 0
    grid = []

    def __init__(self, window, clock):
        self.win = window
        self.win.fill((250, 250, 250))
        self.clock = clock
        self.debug_map = False
        ## gameObjects[0] IS ALWAYS THE PLAYER
        self.gameObjects.append(Player(70, 70, 5))
        self.gameObjects.append(GameObject(0, 0))

        # MAP GRID: make map
        self.grid = [[0]*12 for i in range(16)]

        self.grid[5][5] = 1
        self.grid[5][6] = 1
        self.grid[6][5] = 1
        self.grid[6][6] = 1
        self.grid[7][7] = 2
        for i in range(0,12):
            self.grid[10][i] = 3
        for i in range(0,16):
            self.grid[i][0] = 1
            self.grid[i][11] = 1
        for i in range (0,12):
            self.grid[0][i] = 1
            self.grid[15][i] = 1
        print(self.grid)

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
                    elif event.key == pygame.K_w:
                        self.gameObjects[0].yset_vel(-3)
                    elif event.key == pygame.K_s:
                        self.gameObjects[0].yset_vel(3)
                    elif event.key == pygame.K_a:
                        self.gameObjects[0].xset_vel(-3)
                    elif event.key == pygame.K_d:
                        self.gameObjects[0].xset_vel(3)
                    elif event.key == pygame.K_q:
                        self.gameObjects[0].hurt(1)
                    elif event.key == pygame.K_e:
                        self.gameObjects[0].heal(1)
                    elif event.key == pygame.K_LSHIFT:
                        self.gameObjects[0].shift = 1
                    elif event.key == pygame.K_f:
                        self.gameObjects[0].debug_collision = not self.gameObjects[0].debug_collision
                        self.debug_map = not self.debug_map
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.gameObjects[0].yset_vel(0)
                    elif event.key == pygame.K_s:
                        self.gameObjects[0].yset_vel(0)
                    elif event.key == pygame.K_a:
                        self.gameObjects[0].xset_vel(0)
                    elif event.key == pygame.K_d:
                        self.gameObjects[0].xset_vel(0)
                    elif event.key == pygame.K_LSHIFT:
                        self.gameObjects[0].shift = 0

            # GAME: call all important updates and draw methods
            self.update()
            self.draw()

            # DISPLAY: update the screen
            pygame.display.update()

    def update(self):
        for objects in self.gameObjects:
            objects.update()

        self.gameObjects[0].collide_map(self.grid, self.win)

    def draw(self):

        # DISPLAY: clear the screen
        self.win.fill((250, 250, 250))

        # DISPLAY: Draw Grid first (background)
        for i in range(0,16):
            for j in range (0,12):
                if self.grid[i][j] == 0:
                    if self.debug_map:
                        pygame.draw.rect(self.win, (100,100,100), (i*40,j*40,40,40), 1)
                elif self.grid[i][j] == 1:
                    pygame.draw.rect(self.win, (0,0,0), (i*40,j*40,40,40), 0)
                elif self.grid[i][j] == 2:
                    pygame.draw.rect(self.win, (255,10,10), (i*40,j*40,40,40), 0)
                elif self.grid[i][j] == 3:
                    pygame.draw.rect(self.win, (255,10,10), (i*40,j*40,40,40), 3)

        # DISPLAY: Draw all the game objects now
        for objects in self.gameObjects:
            objects.draw(self.win)