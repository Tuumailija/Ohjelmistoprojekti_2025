# Vihollinen.py
import pygame
import random

class Vihollinen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.leveys = 40
        self.pituus = 40
        self.vari = (255, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.leveys, self.pituus)

    def piirrä(self, screen, cam_x, cam_y):
        pygame.draw.rect(screen, self.vari, pygame.Rect(self.rect.x - cam_x, self.rect.y - cam_y, self.leveys, self.pituus))
