import pygame

from utils import load_sprite
from models import Spaceship, GameObject

print(7 % 5)

class SpaceRocks:

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship((400, 300))
        # self.spaceship2 = GameObject((200, 200), load_sprite("ship"), (0, 0))


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

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.spaceship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.spaceship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.spaceship.accelerate()

    def game_logic(self):
        self.spaceship.move(self.screen)
        # self.spaceship2.move()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        # self.spaceship2.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
