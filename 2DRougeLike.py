# Markus Koski
# Miika Musta
# Frans-Emil Vuori
# TITE23

import pygame
import sys

# pygame asetukset
pygame.init()
naytto = pygame.display.set_mode((1280, 720))
kello = pygame.time.Clock()
kaynnissa = True
dt = 0

pelaaja_sijainti = pygame.Vector2(naytto.get_width() / 2, naytto.get_height() / 2)

while kaynnissa:
    # tapahtumien tarkistaminen
    # pygame.QUIT tapahtuma tarkoittaa, että käyttäjä napsautti X sulkeakseen ikkunan
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            kaynnissa = False

    # täytä näyttö väreillä, jotta edellinen kuva poistuu
    naytto.fill("purple")

    # piirrä ympyrä pelaajan sijaintiin
    pygame.draw.circle(naytto, "red", pelaaja_sijainti, 40)

    # tarkistetaan, onko näppäimiä painettu
    napit = pygame.key.get_pressed()
    if napit[pygame.K_w]:
        pelaaja_sijainti.y -= 300 * dt
    if napit[pygame.K_s]:
        pelaaja_sijainti.y += 300 * dt
    if napit[pygame.K_a]:
        pelaaja_sijainti.x -= 300 * dt
    if napit[pygame.K_d]:
        pelaaja_sijainti.x += 300 * dt

    # flip() näyttää päivitykset näytöllä
    pygame.display.flip()

    # rajoittaa FPS:n 60:een
    # dt on aikaväli edellisen ruudun ja nykyisen ruudun välillä sekunteina,
    # jota käytetään ruudunpäivityksestä riippumattomassa fysiikassa.
    dt = kello.tick(60) / 1000

pygame.quit()