from turtle import distance
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position

UP = Vector2(1, 0)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)


    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)


    def move(self, surface):
        self.position = wrap_position((self.position + self.velocity), surface)


    def colides_with(self, other_object):
        distance = self.position.distance_to(other_object.position)
        return distance < self.radius + other_object.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 5
    ACCELERATION = 0.25

    def __init__(self, position):

        super().__init__(position, load_sprite("ship"), Vector2(0))
        self.direction = Vector2(UP)


    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        print(angle)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += (self.direction) * self.ACCELERATION

    def decelerate(self):
        self.velocity -= (self.direction) * self.ACCELERATION

    def natural_deceleration(self):
        VELOCITY_MIN = 0.1
        

        self.velocity[0] *= 0.975
        self.velocity[1] *= 0.975

        if self.velocity[0] <= VELOCITY_MIN and self.velocity[0] >= -VELOCITY_MIN:
            self.velocity[0] = 0
        
        if self.velocity[1] <= VELOCITY_MIN and self.velocity[1] >= -VELOCITY_MIN:
            self.velocity[1] = 0

class Asteroid(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("asteroid4"), (0, 0))