import pygame
from player.attack import *


class PrototypeStandingAttack(Attack):
    def __init__(self, player):
        super().__init__(player)
        for i in range(0, 60):
            self.attack_frames.append(pygame.Rect(self.player.position[0] + self.player.width, self.player.position[1] + 10, 30 + i, 30 + i))

        print(len(self.attack_frames))

    def draw(self, win):
        print(self.frame)
        pygame.draw.rect(win, (255,0,0), self.attack_frames[self.frame], 2)