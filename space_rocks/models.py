from turtle import distance
from pygame.math import Vector2

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)


    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)


    def move(self):
        self.position = self.position + self.velocity


    def colides_with(self, other_object):
        distance = self.position.distance_to(other_object.position)
        return distance < self.radius + other_object.radius
