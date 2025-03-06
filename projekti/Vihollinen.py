import pygame
import random

# Vihollisen asetukset
VIHOLLISET_KOKO = 32
VIHOLLISET_NOPEUS = 3
VIHOLLISET_VARI = (255, 255, 255)

class Vihollinen:
    def __init__(self, x, y):
        # Alustaa vihollisen annettuun sijaintiin
        self.rect = pygame.Rect(x, y, VIHOLLISET_KOKO, VIHOLLISET_KOKO)

    def piirrä(self, näyttö, cam_x, cam_y):
        # Piirtää vihollisen ruudulle ottaen huomioon kameran sijainnin
        pygame.draw.rect(näyttö, VIHOLLISET_VARI, self.rect.move(-cam_x, -cam_y))

def luo_viholliset(määrä, kartan_leveys, kartan_korkeus, tile_koko):
    # Luo annettun määrän vihollisia satunnaisiin paikkoihin kartalla
    viholliset = []
    for _ in range(määrä):
        x = random.randint(1, kartan_leveys - 2) * tile_koko
        y = random.randint(1, kartan_korkeus - 2) * tile_koko
        viholliset.append(Vihollinen(x, y))
    return viholliset
