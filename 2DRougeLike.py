# Markus Koski
# Miika Musta
# Frans-Emil Vuori
# Tuukka Penttinen
# TITE23

# https://app.clickup.com/9012306078/v/s/90123033370 <-- ClickUp-tiimilinkki projektiin

import pygame
import sys
import os

# pygame asetukset
pygame.init()
naytto = pygame.display.set_mode((1280, 720))
kello = pygame.time.Clock()
kaynnissa = True
dt = 0

# Lataa taustakuva
nykyinen_kansio = os.path.dirname(__file__)
kuvapolku = os.path.join(nykyinen_kansio, "Metsa.png")
tausta1 = pygame.image.load(kuvapolku)

# Pelaajan sijainti (keskellä näyttöä)
pelaaja_sijainti = pygame.Vector2(naytto.get_width() / 2, naytto.get_height() / 2)
pelaaja_sade = 20  # Ympyrän säde

# Seinälistan luonti (Rect-muodossa)
seinät = [
    pygame.Rect(200, 200, 200, 50),  # Esimerkkiseinä
    pygame.Rect(500, 400, 300, 50),  # Toinen seinä
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

    # Piirrä taustakuva
    naytto.blit(tausta1, (0, 0))

    # Piirrä seinät
    for seinä in seinät:
        pygame.draw.rect(naytto, "blue", seinä)

    # Piirrä pelaaja
    pygame.draw.circle(naytto, "red", pelaaja_sijainti, pelaaja_sade)

    # Pelaajan liikkuminen
    napit = pygame.key.get_pressed()
    uusi_x, uusi_y = pelaaja_sijainti.x, pelaaja_sijainti.y

    if napit[pygame.K_w]:
        uusi_y -= 300 * dt
    if napit[pygame.K_s]:
        uusi_y += 300 * dt
    if napit[pygame.K_a]:
        uusi_x -= 300 * dt
    if napit[pygame.K_d]:
        uusi_x += 300 * dt

    # Tarkista törmäys ennen päivittämistä
    if not tarkista_tormays(uusi_x, uusi_y):
        pelaaja_sijainti.x = uusi_x
        pelaaja_sijainti.y = uusi_y

    # Päivitä näyttö
    pygame.display.flip()
    dt = kello.tick(60) / 1000

pygame.quit()
