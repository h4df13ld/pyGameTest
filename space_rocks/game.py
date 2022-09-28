from turtle import position
import pygame

from utils import load_sprite, get_random_positon
from models import Spaceship, Asteroid

print(7 % 5)

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 125

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        
        self.asteroids = []
        self.lasers = []

        self.spaceship = Spaceship((400, 300), self.lasers.append)
        self.setup_asteroids()

    def setup_asteroids(self):
        for _ in range(6):
            position = get_random_positon(self.screen)
            if position.distance_to(self.spaceship.position) < self.MIN_ASTEROID_DISTANCE:
                break
            self.asteroids.append(Asteroid(position))

    def get_game_objects(self):
        game_objects = [*self.asteroids, *self.lasers]

        if self.spaceship:
            game_objects.append(self.spaceship)
        
        return game_objects

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

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            elif is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.decelerate()
            elif is_key_pressed[pygame.K_SPACE]:
                self.spaceship.shoot()

    def game_logic(self):
        
        for game_object in self.get_game_objects():
            game_object.move(self.screen)
            if isinstance(game_object, Spaceship):
                game_object.natural_deceleration()

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.colides_with(self.spaceship):
                    self.spaceship = None
                    break

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self.get_game_objects():
            game_object.draw(self.screen)
        
        
        pygame.display.flip()
        self.clock.tick(60)
