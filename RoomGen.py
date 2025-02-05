
import pygame
import sys
import os
import random

# Pygame asetukset
pygame.init()
naytto = pygame.display.set_mode((1280, 720))
kello = pygame.time.Clock()
kaynnissa = True
dt = 0

# Lataa taustakuva
nykyinen_kansio = os.path.dirname(__file__)
kuvapolku = os.path.join(nykyinen_kansio, "1920x1080_graybackground.jpg")
tausta1 = pygame.image.load(kuvapolku)

# Pelaajan sijainti (keskellä näyttöä)
pelaaja_sijainti = pygame.Vector2(naytto.get_width() / 2, naytto.get_height() / 2)
pelaaja_sade = 20  # Ympyrän säde
ovi_koko = pelaaja_sade * 4  # Oviaukko on 2x pelaajan halkaisija

# Huoneen parametrit
seinan_paksuus = 10
huone_leveys = 500
huone_korkeus = 500
x_offset = 240
y_offset = 110

# Satunnaisten ovien generointi
ovet = []
while len(ovet) < 2:
    ovi_sijainti = random.choice(["vasen", "oikea", "ylä", "ala"])
    if ovi_sijainti == "vasen":
        ovi_x = x_offset
        ovi_y = random.randint(y_offset + 10, y_offset + huone_korkeus - ovi_koko - 10)
        ovet.append(pygame.Rect(ovi_x, ovi_y, seinan_paksuus, ovi_koko))
    elif ovi_sijainti == "oikea":
        ovi_x = x_offset + huone_leveys
        ovi_y = random.randint(y_offset + 10, y_offset + huone_korkeus - ovi_koko - 10)
        ovet.append(pygame.Rect(ovi_x, ovi_y, seinan_paksuus, ovi_koko))
    elif ovi_sijainti == "ylä":
        ovi_x = random.randint(x_offset + 10, x_offset + huone_leveys - ovi_koko - 10)
        ovi_y = y_offset
        ovet.append(pygame.Rect(ovi_x, ovi_y, ovi_koko, seinan_paksuus))
    elif ovi_sijainti == "ala":
        ovi_x = random.randint(x_offset + 10, x_offset + huone_leveys - ovi_koko - 10)
        ovi_y = y_offset + huone_korkeus
        ovet.append(pygame.Rect(ovi_x, ovi_y, ovi_koko, seinan_paksuus))

# Seinien generointi oven molemmille puolille
seinät = [
    pygame.Rect(x_offset, y_offset, huone_leveys, seinan_paksuus),  # Yläseinä
    pygame.Rect(x_offset, y_offset + huone_korkeus, huone_leveys, seinan_paksuus),  # Alaseinä
    pygame.Rect(x_offset, y_offset, seinan_paksuus, huone_korkeus),  # Vasen seinä
    pygame.Rect(x_offset + huone_leveys, y_offset, seinan_paksuus, huone_korkeus),  # Oikea seinä
]

# Poista seinän osia ovien kohdalta
seinät_uudet = []
for seina in seinät:
    osia = [seina]
    for ovi in ovet:
        uudet_osat = []
        for osa in osia:
            if osa.colliderect(ovi):
                if osa.width > osa.height:  # Vaakaseinä
                    if osa.x < ovi.x:
                        uudet_osat.append(pygame.Rect(osa.x, osa.y, ovi.x - osa.x, osa.height))
                    if osa.x + osa.width > ovi.x + ovi.width:
                        uudet_osat.append(pygame.Rect(ovi.x + ovi.width, osa.y, (osa.x + osa.width) - (ovi.x + ovi.width), osa.height))
                else:  # Pystyseinä
                    if osa.y < ovi.y:
                        uudet_osat.append(pygame.Rect(osa.x, osa.y, osa.width, ovi.y - osa.y))
                    if osa.y + osa.height > ovi.y + ovi.height:
                        uudet_osat.append(pygame.Rect(osa.x, ovi.y + ovi.height, osa.width, (osa.y + osa.height) - (ovi.y + ovi.height)))
            else:
                uudet_osat.append(osa)
        osia = uudet_osat
    seinät_uudet.extend(osia)
seinät = seinät_uudet

# Törmäystarkistus
def tarkista_tormays(x, y):
    """ Tarkistaa, osuisiko pelaaja seinään uudessa sijainnissa. """
    pelaaja_rect = pygame.Rect(x - pelaaja_sade, y - pelaaja_sade, pelaaja_sade * 2, pelaaja_sade * 2)
    for seinä in seinät:
        if pelaaja_rect.colliderect(seinä):
            return True  # Törmäys tapahtuu
    return False  # Ei törmäystä

while kaynnissa:
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            kaynnissa = False

    naytto.blit(tausta1, (0, 0))

    for seinä in seinät:
        pygame.draw.rect(naytto, "black", seinä)

    for ovi in ovet:
        pygame.draw.rect(naytto, "gray", ovi)

    pygame.draw.circle(naytto, "red", pelaaja_sijainti, pelaaja_sade)

    napit = pygame.key.get_pressed()
    uusi_x, uusi_y = pelaaja_sijainti.x, pelaaja_sijainti.y

    # Liikkuminen eri suunnissa ja törmäysten käsittely
    uusi_x_temp, uusi_y_temp = uusi_x, uusi_y
    if napit[pygame.K_w]:
        uusi_y_temp -= 200 * dt
    if napit[pygame.K_s]:
        uusi_y_temp += 200 * dt
    if not tarkista_tormays(uusi_x, uusi_y_temp):
        uusi_y = uusi_y_temp
    
    uusi_x_temp = uusi_x
    if napit[pygame.K_a]:
        uusi_x_temp -= 200 * dt
    if napit[pygame.K_d]:
        uusi_x_temp += 200 * dt
    if not tarkista_tormays(uusi_x_temp, uusi_y):
        uusi_x = uusi_x_temp
    
    pelaaja_sijainti.x = uusi_x
    pelaaja_sijainti.y = uusi_y

    pygame.display.flip()
    dt = kello.tick(60) / 1000

pygame.quit()
