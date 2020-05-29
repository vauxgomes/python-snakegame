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
DELAY = 250
DELAY_MIN = 75
DELAY_STEP = 100

# Direções
D_UP, D_DOWN, D_LEFT, D_RIGHT = [0, 2, 1, 3]

# Constantes de cores
TEXT = (45, 45, 42)
BACKGROUND = (6, 214, 160)
SNAKE = (45, 45, 42)
GRID = (63, 94, 90)
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
        self.belly = []

    def hit(self, c: Cube):
        return self.body[0].position == c.position

    def eat(self):
        self.belly.append(Cube(self.body[0].position, GRID))
        self.dirs.append(self.dirs[0])

    def collided(self):
        for i in range(1, len(self.body)):
            if self.hit(self.body[i]):
                return True

        return False


    def move(self, dir_=None):
        if dir_ is None or abs(dir_ - self.dirs[0]) == 2:
            dir_ = self.dirs[0]

        self.dirs.insert(0, dir_)
        self.dirs = self.dirs[:-1]

        for i, c in enumerate(self.body):
            c.move(self.dirs[i])

    def draw(self, surface):
        if len(self.belly) > 0:
            b = self.belly[0]
            hit_ = False

            for c in self.body:
                if c.position == b.position:
                    hit_ = True
                    break

            if not hit_:
                self.belly.remove(b)
                self.body.append(b)

        for c in self.body:
            c.draw(surface)


class Window:
    ''' Classe que exibe os elementos de tela '''

    @staticmethod
    def draw(surface, score=0):
        # Background
        surface.fill(BACKGROUND)

        # Grade
        u = BORDER
        
        for i in range(0, ROWS + 1):
            pygame.draw.line(surface, GRID,
                             (u, BORDER), (u, HEIGHT - BORDER))

            pygame.draw.line(surface, GRID,
                             (BORDER, u), (WIDTH - BORDER, u))

            u += BLOCK

        # Score
        text = Window.font.render(f'PONTOS: {score}', True, TEXT)
        surface.blit(text, (BORDER, BORDER - 26))
    
    @staticmethod
    def end(surface, score):
        # Background
        surface.fill(BACKGROUND)

        # Logo
        font = pygame.font.SysFont('arial', 40)

        text = font.render('SnakeGame', True, TEXT)
        textRect = text.get_rect()
        textRect.center = (WIDTH//2, HEIGHT//2 - 20)
        surface.blit(text, textRect)

        # Score
        text = Window.font.render(f'PONTOS: {score}', True, TEXT)
        textRect = text.get_rect()
        textRect.center = (WIDTH//2, (HEIGHT//2) + 10)
        surface.blit(text, textRect)

def main():
    # PyGame
    pygame.init()

    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('SnakeGame')

    Window.font = pygame.font.SysFont('arial', 24)

    # Auxiliares
    ext = False

    # Jogo
    score = 0
    delay = DELAY
    collided = False

    # Elementos
    snake = Snake()
    bait = Cube((3, 2), BAIT)

    # Laço principal
    while not ext:
        # Delay
        pygame.time.delay(max(DELAY_MIN, delay))

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

        # Não colidiu
        if not collided:
            if snake.collided():
                collided = True
                continue

            if snake.hit(bait):
                snake.eat()
                bait.position =  (rnd.randint(0, ROWS-1), rnd.randint(0, ROWS-1))
                score += 1

                if score % 3 == 0:
                    delay -= DELAY_STEP

            # Ações
            snake.move(dir_)

            # Desenhar os elementos
            Window.draw(surface, score)
            bait.draw(surface)
            snake.draw(surface)
        
        # Colidiu
        else:
            Window.end(surface, score)

        # Atualização
        pygame.display.update()

    # Fim do jogo
    pygame.quit()


if __name__ == '__main__':
    main()
