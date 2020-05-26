'''
TODO-list:
 - Criar Snake.hit
 - Guardar pontuação
 - Ajustar Window.draw para exibir pontuação
 - Criar configuração de nível/velocidade
 
 - Criar Snake.eat
 - Ajustar Snake.draw
  
 - Criar Snake.collided e finalização do jogo
 - Criar tela de fim
'''

# Bibliotecas
import pygame
import random as rnd

from pygame.locals import *

# Variáveis de tela
WIDTH = 500
HEIGHT = 500
BORDER = 50
ROWS = 10
BLOCK = (WIDTH - 2*BORDER)//ROWS

# Jogo
DELAY = 200

# Direções
D_UP, D_DOWN, D_LEFT, D_RIGHT = [0, 1, 2, 3]

# Constantes de cores
TEXT = (45, 45, 42)
BACKGROUND = (6, 214, 160)
SNAKE = (45, 45, 42)
LINE = (63, 94, 90)
BAIT = (239, 71, 111)


class Cube:
    ''' Classe que representa um elemento simples do jogo '''

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def move(self, dir_):
        if dir_ == D_UP:
            self.position = (self.position[0], self.position[1] - 1)
        elif dir_ == D_DOWN:
            self.position = (self.position[0], self.position[1] + 1)
        elif dir_ == D_LEFT:
            self.position = (self.position[0] - 1, self.position[1])
        elif dir_ == D_RIGHT:
            self.position = (self.position[0] + 1, self.position[1])

        # Verificando limite de tela
        if self.position[0] >= ROWS:
            self.position = (0, self.position[1])
        elif self.position[0] < 0:
            self.position = (ROWS - 1, self.position[1])

        if self.position[1] >= ROWS:
            self.position = (self.position[0], 0)
        elif self.position[1] < 0:
            self.position = (self.position[0], ROWS - 1)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (BORDER + self.position[0]*BLOCK, BORDER + self.position[1]*BLOCK, BLOCK, BLOCK))


class Snake:
    ''' Classe que representa a entidade principal do jogo '''

    def __init__(self):
        self.body = [Cube((0, 0), SNAKE)]
        self.dirs = [D_RIGHT]

    def move(self, dir_=None):
        if dir_ is None:
            dir_ = self.dirs[0]

        self.dirs.insert(0, dir_)
        self.dirs = self.dirs[:-1]

        for i, c in enumerate(self.body):
            c.move(self.dirs[i])

    def draw(self, surface):
        for c in self.body:
            c.draw(surface)


class Window:
    ''' Classe que exibe os elementos de tela '''

    @staticmethod
    def draw(surface, points=0):
        # Background
        surface.fill(BACKGROUND)

        u = BORDER
        # Grade

        for i in range(0, ROWS + 1):
            pygame.draw.line(surface, LINE,
                             (u, BORDER), (u, HEIGHT - BORDER))

            pygame.draw.line(surface, LINE,
                             (BORDER, u), (WIDTH - BORDER, u))

            u += BLOCK


def main():
    # PyGame
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('SnakeGame IFCE')

    # Auxiliares
    ext = False

    # Elementos
    s = Snake()
    b = Cube((3, 2), BAIT)

    # Laço principal
    while not ext:
        # Delay
        pygame.time.delay(DELAY)

        # Eventos
        events = pygame.event.get()

        # Auxiliares
        dir_ = None

        for e in events:
            # Evento de clique no X da janela
            if e.type == QUIT:
                ext = True

            # Teclado
            if e.type == KEYDOWN:
                if e.key in (K_UP, K_w):
                    dir_ = D_UP
                elif e.key in (K_DOWN, K_s):
                    dir_ = D_DOWN
                elif e.key in (K_LEFT, K_a):
                    dir_ = D_LEFT
                elif e.key in (K_RIGHT, K_d):
                    dir_ = D_RIGHT
                elif e.key == K_ESCAPE:
                    ext = True

        if s.body[0].position[0] == b.position[0] and s.body[0].position[1] == b.position[1]:
            b = Cube((rnd.randint(0, ROWS-1),
                      rnd.randint(0, ROWS-1)), BAIT)

        # Ações
        s.move(dir_)

        # Desenhar os elementos
        Window.draw(surface)
        b.draw(surface)
        s.draw(surface)

        # Atualização
        pygame.display.update()

    # Fim do jogo
    pygame.quit()


if __name__ == '__main__':
    main()
