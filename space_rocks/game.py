import pygame

from utils import load_sprite
from models import GameObject

class SpaceRocks:

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        self.spaceship = GameObject((400, 300), load_sprite("spaceship"), (0, 0))
        self.asteroid = GameObject((400, 300), load_sprite("asteroid"), (1, 0))


    def main_loop(self):
        while True:
            self.handle_input()
            self.game_logic()
            self.draw()


    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

    def game_logic(self):
        self.spaceship.move()
        self.asteroid.move()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        self.asteroid.draw(self.screen)
        pygame.display.flip()