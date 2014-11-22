import pygame
from player.attack import *


class PrototypeStandingAttack(Attack):
    def __init__(self, player):
        super().__init__(player)
        y = self.player.position[1] + 10
        if self.player.facingright:
            x = self.player.position[0] + self.player.width
            multiple = 3
        else:
            x = self.player.position[0]
            multiple = -3

        for i in range(0, 60):
            self.attack_frames.append(pygame.Rect(x, y, i*multiple, 30))

        print(len(self.attack_frames))

    def draw(self, win):
        print(self.frame)
        pygame.draw.rect(win, (255,0,0), self.attack_frames[self.frame], 2)