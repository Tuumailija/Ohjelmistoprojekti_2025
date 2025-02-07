import pygame
import sys
import os
import random

# Pygame asetukset
pygame.init()
naytto = pygame.display.set_mode((1920, 1080))
kello = pygame.time.Clock()
kaynnissa = True
dt = 0

# Lataa taustakuva
nykyinen_kansio = os.path.dirname(__file__)
kuvapolku = os.path.join(nykyinen_kansio, "..", "media", "Img", "1920x1080_graybackground.jpg")
tausta1 = pygame.image.load(kuvapolku)

# Pelaajan säde
pelaaja_sade = 20  # Ympyrän säde
ovi_koko = pelaaja_sade * 4  # Oviaukko on 2x pelaajan halkaisija

# Seinän paksuus
seinan_paksuus = 10

# **Satunnaisten huonekokojen generointi**
perus_koko = 400  # Pienimmän huoneen koko
huone_suhteet = [(1, 1), (1, 2), (2, 1)]  # Suhdeparit
suhde = random.choice(huone_suhteet)  # Valitaan yksi satunnaisesti

# Lasketaan huoneen leveys ja korkeus
huone_leveys = perus_koko * suhde[0]
huone_korkeus = perus_koko * suhde[1]

# Huoneen keskitys
x_offset = (naytto.get_width() - huone_leveys) // 2
y_offset = (naytto.get_height() - huone_korkeus) // 2

# Pelaajan sijainti (keskellä huonetta)
pelaaja_sijainti = pygame.Vector2(
    x_offset + huone_leveys // 2,
    y_offset + huone_korkeus // 2
)

# **Satunnaisten ovien generointi**
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

# **Seinien generointi**
seinät = [
    pygame.Rect(x_offset, y_offset, huone_leveys, seinan_paksuus),
    pygame.Rect(x_offset, y_offset + huone_korkeus, huone_leveys, seinan_paksuus),
    pygame.Rect(x_offset, y_offset, seinan_paksuus, huone_korkeus),
    pygame.Rect(x_offset + huone_leveys, y_offset, seinan_paksuus, huone_korkeus),
]

# **Poista seinän osia ovien kohdalta**
seinät_uudet = []
for seina in seinät:
    osia = [seina]
    for ovi in ovet:
        uudet_osat = []
        for osa in osia:
            if osa.colliderect(ovi):
                if osa.width > osa.height:
                    if osa.x < ovi.x:
                        uudet_osat.append(pygame.Rect(osa.x, osa.y, ovi.x - osa.x, osa.height))
                    if osa.x + osa.width > ovi.x + ovi.width:
                        uudet_osat.append(pygame.Rect(ovi.x + ovi.width, osa.y, (osa.x + osa.width) - (ovi.x + ovi.width), osa.height))
                else:
                    if osa.y < ovi.y:
                        uudet_osat.append(pygame.Rect(osa.x, osa.y, osa.width, ovi.y - osa.y))
                    if osa.y + osa.height > ovi.y + ovi.height:
                        uudet_osat.append(pygame.Rect(osa.x, ovi.y + ovi.height, osa.width, (osa.y + osa.height) - (ovi.y + ovi.height)))
            else:
                uudet_osat.append(osa)
        osia = uudet_osat
    seinät_uudet.extend(osia)
seinät = seinät_uudet

# **Törmäystarkistus**
def tarkista_tormays(x, y):
    pelaaja_rect = pygame.Rect(x - pelaaja_sade, y - pelaaja_sade, pelaaja_sade * 2, pelaaja_sade * 2)
    for seinä in seinät:
        if pelaaja_rect.colliderect(seinä):
            return True
    return False

# **Pelin päälooppi**
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

    if napit[pygame.K_w] and not tarkista_tormays(uusi_x, uusi_y - 200 * dt):
        uusi_y -= 200 * dt
    if napit[pygame.K_s] and not tarkista_tormays(uusi_x, uusi_y + 200 * dt):
        uusi_y += 200 * dt
    if napit[pygame.K_a] and not tarkista_tormays(uusi_x - 200 * dt, uusi_y):
        uusi_x -= 200 * dt
    if napit[pygame.K_d] and not tarkista_tormays(uusi_x + 200 * dt, uusi_y):
        uusi_x += 200 * dt

    pelaaja_sijainti.x, pelaaja_sijainti.y = uusi_x, uusi_y

    pygame.display.flip()
    dt = kello.tick(60) / 1000

pygame.quit()