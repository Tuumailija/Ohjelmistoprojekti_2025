import pygame
import random

class Vihollinen:
    def __init__(self, x, y, size=32):
        # Asetetaan vihollisen sijainti ja koko
        self.rect = pygame.Rect(x, y, size, size)

    def update(self, dt):
        # Placeholder – tähän voi myöhemmin lisätä liikettä tai muuta logiikkaa.
        pass

    def draw(self, surface, cam_x, cam_y):
        # Piirretään vihollinen punaisena neliönä
        pygame.draw.rect(surface, (255, 0, 0),
                         pygame.Rect(self.rect.x - cam_x, self.rect.y - cam_y,
                                     self.rect.width, self.rect.height))
