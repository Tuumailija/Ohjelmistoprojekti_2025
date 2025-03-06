import pygame

Vihollisen_koko = 32
Vihollisen_nopeus = 3 
Vihollisen_vari = (140, 20, 15)

class Vihollinen:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, Vihollisen_koko, Vihollisen_koko)

    def piirrä(self, näyttö, cam_x, cam_y):
        pygame.draw.rect(näyttö, Vihollisen_vari, self.rect.move(-cam_x, -cam_y))

