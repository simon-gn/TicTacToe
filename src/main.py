import pygame
import numpy as np
from game import TicTacToe

def main():
    pygame.init()
    pygame.font.init()
    game = TicTacToe()
    game.run()

if __name__ == "__main__":
    main()