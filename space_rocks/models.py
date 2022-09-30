from turtle import distance
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position, get_random_velocity

UP = Vector2(0, -1)

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
    LASER_SPEED = 3

    def __init__(self, position, create_laser_callback):
        self.create_laser_callback = create_laser_callback

        super().__init__(position, load_sprite("ship2"), Vector2(0))
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



    def shoot(self):
        laser_velocity = self.direction * self.LASER_SPEED + self.velocity

        
        direction = self.direction
        laser = Laser(self.position, laser_velocity, self)
        self.create_laser_callback(laser)


class Asteroid(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("asteroid4"), get_random_velocity(1, 3))


    def colides_with(self, other_object):
        distance = self.position.distance_to(other_object.position)
        return distance < (self.radius + other_object.radius) * 0.5


class Laser(GameObject):
    def __init__(self, position, velocity, spaceship):
        super().__init__(position, load_sprite("laser"), velocity)
        self.spaceship = spaceship
        self.direction = spaceship.direction

        self.set_rotation()


    def set_rotation(self):
        angle = self.direction.angle_to(UP)
        self.rotated_surface = rotozoom(self.sprite, angle, 1)
        self.rotated_surface_size = Vector2(self.rotated_surface.get_size())

    def draw(self, surface):
        blit_position = self.position - self.rotated_surface_size * 0.5
        surface.blit(self.rotated_surface, blit_position)