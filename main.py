from Game import *
import pygame


# initialize window and begin game


def main():
    print('Marco Bros Starting')

    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Marco Bros')

    clock = pygame.time.Clock()

    game = Game(win, clock)
    game.gameloop()

    print('exited game')


if __name__ == "__main__":
    main()