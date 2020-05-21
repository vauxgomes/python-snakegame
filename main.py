# Bibliotecas
import pygame
import random as rnd

from pygame.locals import *

# Variáveis de tela
WIDTH = 500
HEIGHT = 500
ROWS = 20
BLOCK = WIDTH//ROWS

# Jogo
DELAY = 100

# Direções
D_UP, D_DOWN, D_LEFT, D_RIGHT = [0, 1, 2, 3]

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Cube:
    ''' Classe que representa um elemento simples do jogo '''

    def __init__(self):
        pass

    def move(self, dir_):
        pass

    def draw(self, surface):
        pass


class Snake:
    ''' Classe que representa a entidade principal do jogo '''

    def __init__(self):
        pass

    def move(self):
        pass

    def draw(self, surface):
        pass


class Window:
    ''' Classe que exibe os elementos de tela '''

    @staticmethod
    def draw(surface):
        pass


def main():
    ''' Main '''
    pass


if __name__ == '__main__':
    main()
