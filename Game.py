from platform.platforms import *
from player.characters.prototype.prototype import *
from player.players import *


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
        self.font2 = pygame.font.Font(None, 120)
        self.controllercount = pygame.joystick.get_count()

        ## setup controller
        #self.testcontroller = pygame.joystick.Joystick(0)
        #self.testcontroller.init()

        ## gameObjects are the players

        # if controller:
            #self.gameObjects.append(Prototype(550, 400, 50, 100, 40, 6, "Human", self.testcontroller))
        # if keyboard:
        self.gameObjects.append(Prototype(550, 400, 50, 100, 40, 6, "Human", 0))
        self.gameObjects.append(Prototype(600, 400, 50, 100, 30, 6, "CPU", 0))

        ## add some platforms
        self.platforms.append(Platform(300,500,1500,100,0))
        self.platforms.append(Platform(100,300,200,10,1))
        self.platforms.append(Platform(800,200,400,100,0))
        self.platforms.append(Platform(500,100,400,10,1))
        self.platforms.append(Platform(-200,1000,700,10,1))


    def gameloop(self):
        while True:
            # GAME: 60tick, update and draw n (60 for now) times a second
            self.time += self.clock.tick(60)

            # CONTROLS: main event handling
            for objects in self.gameObjects:
                objects.handle_input()
            # GAME: call all important updates and draw methods
            self.update()
            self.draw()


            # DISPLAY: update the screen
            pygame.display.update()

    def update(self):
        for objects in self.gameObjects:
            objects.update(self.platforms)

        for plats in self.platforms:
            plats.update()

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
            offset_players += 400
            offset_lives = 0
            playerpercent = self.font.render(str(players.health) + "%", 1, (0,0,0))
            charactername = self.font.render("Proto", 1, (0,0,0))
            lives = self.font.render("x" + str(players.lives), 1, (0,100,0))
            #playerpercent2 = self.font2.render(str(players.health) + "%", 1, (0,0,0))
            #self.win.blit(playerpercent2, (offset_players - 2, 720 - 120 - 5))
            self.win.blit(playerpercent, (offset_players, 720 - 120))
            self.win.blit(charactername, (offset_players - 50, 720 - 65))
            if players.lives > 5:
                pygame.draw.circle(self.win, (0,100,0), (offset_players + offset_lives, 720 - 160), 20, 0)
                self.win.blit(lives, (offset_players + 30, 720 - 195))
            else:
                for i in range(0,players.lives):
                    pygame.draw.circle(self.win, (0,100,100), (offset_players + offset_lives, 720 - 160), 20, 0)
                    offset_lives += 40