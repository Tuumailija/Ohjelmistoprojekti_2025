import pygame
import os
import random

class Vihollinen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.leveys = 40
        self.pituus = 40
        sprite_path = os.path.join("projekti", "media", "Img", "Vihollinen_testi.png")
        if os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            # Skaalataan sprite vastaamaan vihollisen kokoa
            self.sprite = pygame.transform.scale(self.sprite, (self.leveys, self.pituus))
        else:
            print(f"Spriteä ei löytynyt polusta: {sprite_path}. Käytetään varaväriä.")
            self.sprite = None
            self.vari = (255, 255, 255)  # Vihollinen on valkoinen varavärinä jos spriteä ei löydy

        self.rect = pygame.Rect(self.x, self.y, self.leveys, self.pituus)

    def piirrä(self, screen, cam_x, cam_y):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x - cam_x, self.rect.y - cam_y))
        else:
            # Jos spriteä ei ole, piirretään pelkkä suorakulmio
            pygame.draw.rect(screen, self.vari, pygame.Rect(self.rect.x - cam_x, self.rect.y - cam_y, self.leveys, self.pituus))
