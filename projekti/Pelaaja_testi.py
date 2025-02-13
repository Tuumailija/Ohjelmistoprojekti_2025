# Markus Koski
# Miika Musta
# Frans-Emil Vuori
# Tuukka Penttinen
# TITE23

import pygame
import os
from Pelaaja import *

# pygame asetukset
pygame.init()
naytto = pygame.display.set_mode((1280, 720))
kello = pygame.time.Clock()
dt = 0

# Lataa taustakuva
nykyinen_kansio = os.path.dirname(__file__)
kuvapolku = os.path.join(nykyinen_kansio, "..", "media", "Img", "1920x1080_graybackground.jpg")
tausta1 = pygame.image.load(kuvapolku)

# Seinälistan luonti (Rect-muodossa)
seinat = [ # Rect(x, y, width, height)
    pygame.Rect(390, 180, 375, 10),  # 1. Yläseinä
    pygame.Rect(840, 180, 40, 10),  # 2. Yläseinä
    pygame.Rect(390, 525, 495, 10),  # Alaseinä
    pygame.Rect(390, 180, 10, 240),  # 1. Vasen sivuseinä
    pygame.Rect(390, 490, 10, 40),  # 2. Vasen sivuseinä
    pygame.Rect(875, 180, 10, 350),  # Oikea sivuseinä
]

player = Player()

while True:
    # tapahtumien tarkistaminen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    # Piirrä peli (taustakuva, seinät, pelaaja)
    naytto.blit(tausta1, (0, 0))
    pygame.draw.circle(naytto, "red", player.position, player.sade)
    player.update(seinat)

    # Piirrä seinät
    for seina in seinat:
        pygame.draw.rect(naytto, "black", seina)

    # Päivitä näyttö
    pygame.display.flip()
    dt = kello.tick(60) / 1000