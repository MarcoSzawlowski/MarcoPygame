import pygame


class Platform:

    def __init__(self, x, y, width, length, type):
        self.position = [x, y]
        self.width = width
        self.length = length
        self.type = type
        self.box = pygame.Rect(self.position[0],self.position[1],self.width,self.length)

    def update(self):
        pass

    def draw(self, win):
        if self.type == 0:
            pygame.draw.rect(win, (0, 0, 0), self.box, 0)
        if self.type == 1:
            pygame.draw.rect(win, (100, 100, 100), self.box, 1)
