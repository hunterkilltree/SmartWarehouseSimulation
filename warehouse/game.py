import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.running = 1
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(0, 0, 640, 480)

    def reDraw(self):
        pygame.display.flip()

    def tick(self, fps):
        self.clock.tick(fps)