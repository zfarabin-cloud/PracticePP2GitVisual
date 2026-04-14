# ball
import pygame as pg

class Ball:
    def __init__(self, x=25, y=25, radius=25, color='Red'):
        """
        Initializes the ball's properties based on the original script.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 20  # Movement step size from original code

    def update(self, keys, screen_width, screen_height):
        """
        Updates the ball's position based on keyboard input while maintaining 
        boundaries.
        """
        if keys[pg.K_RIGHT]:
            if self.x + self.speed <= screen_width - self.radius:
                self.x += self.speed
        if keys[pg.K_LEFT]:
            if self.x - self.speed >= self.radius:
                self.x -= self.speed
        if keys[pg.K_UP]:
            if self.y - self.speed >= self.radius:
                self.y -= self.speed
        if keys[pg.K_DOWN]:
            if self.y + self.speed <= screen_height - self.radius:
                self.y += self.speed

    def draw(self, screen):
        """
        Renders the ball onto the provided pygame surface.
        """
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)