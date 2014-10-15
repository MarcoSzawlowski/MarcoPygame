from Game import *
import pygame


# initialize window and begin game


def main():
    print('simulation starting')

    pygame.init()
    win = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Simulation')

    clock = pygame.time.Clock()

    game = Game(win, clock)
    game.gameloop()

    print('exited simulation')


if __name__ == "__main__":
    main()