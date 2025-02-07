# Markus Koski
# Miika Musta
# Frans-Emil Vuori
# Tuukka Penttinen
# TITE23

import pygame
import sys
import os
from Aloitusvalikko import Aloitusvalikko

# pygame asetukset
pygame.init()
naytto = pygame.display.set_mode((1280, 720))
kello = pygame.time.Clock()
kaynnissa = True
dt = 0

# Lataa taustakuva
nykyinen_kansio = os.path.dirname(__file__)
kuvapolku = os.path.join(nykyinen_kansio, "..", "media", "Img", "1920x1080_graybackground.jpg")
tausta1 = pygame.image.load(kuvapolku)

# Aloitusvalikon luonti
valikko = Aloitusvalikko(naytto)
valikossa = True

# Pelaajan sijainti (keskellä näyttöä)
pelaaja_sijainti = pygame.Vector2(naytto.get_width() / 2, naytto.get_height() / 2)
pelaaja_sade = 20  # Ympyrän säde

# Seinälistan luonti (Rect-muodossa)
seinät = [ # Rect(x, y, width, height)
    pygame.Rect(390, 180, 375, 10),  # 1. Yläseinä
    pygame.Rect(840, 180, 40, 10),  # 2. Yläseinä
    pygame.Rect(390, 525, 495, 10),  # Alaseinä
    pygame.Rect(390, 180, 10, 240),  # 1. Vasen sivuseinä
    pygame.Rect(390, 490, 10, 40),  # 2. Vasen sivuseinä
    pygame.Rect(875, 180, 10, 350),  # Oikea sivuseinä
]

def tarkista_tormays(x, y):
    """ Tarkistaa, osuisiko pelaaja seinään uudessa sijainnissa. """
    pelaaja_rect = pygame.Rect(x - pelaaja_sade, y - pelaaja_sade, pelaaja_sade * 2, pelaaja_sade * 2)
    for seinä in seinät:
        if pelaaja_rect.colliderect(seinä):
            return True  # Törmäys tapahtuu
    return False  # Ei törmäystä

while kaynnissa:
    # tapahtumien tarkistaminen
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            kaynnissa = False

        # Päivitä valikon tapahtumat, jos ollaan valikkotilassa
        if valikossa:
            valikossa = valikko.paivita_valikko(tapahtuma)

    # Jos ollaan valikossa
    if valikossa:
        if valikko.ohjeet_nakymassa:
            valikko.piirra_ohjeet()  # Piirrä ohjeet näytölle
        else:
            valikko.piirra_valikko()  # Piirrä aloitusvalikko näytölle
    else:
        # Piirrä peli (taustakuva, seinät, pelaaja)
        naytto.blit(tausta1, (0, 0))

        # Piirrä seinät
        for seinä in seinät:
            pygame.draw.rect(naytto, "black", seinä)

        # Piirrä pelaaja
        pygame.draw.circle(naytto, "red", pelaaja_sijainti, pelaaja_sade)

        # Pelaajan liikkuminen
        napit = pygame.key.get_pressed()
        uusi_x, uusi_y = pelaaja_sijainti.x, pelaaja_sijainti.y

        if napit[pygame.K_w]:
            uusi_y -= 200 * dt
        if napit[pygame.K_s]:
            uusi_y += 200 * dt
        if napit[pygame.K_a]:
            uusi_x -= 200 * dt
        if napit[pygame.K_d]:
            uusi_x += 200 * dt

        # Tarkista törmäys ennen päivittämistä
        if not tarkista_tormays(uusi_x, uusi_y):
            pelaaja_sijainti.x = uusi_x
            pelaaja_sijainti.y = uusi_y

    # Päivitä näyttö
    pygame.display.flip()
    dt = kello.tick(60) / 1000

pygame.quit()
