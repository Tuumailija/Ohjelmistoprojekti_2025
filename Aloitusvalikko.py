import pygame
import sys

class Aloitusvalikko:
    def __init__(self, naytto):
        self.naytto = naytto
        self.fontti = pygame.font.SysFont("Arial", 60)
        self.pieni_fontti = pygame.font.SysFont("Arial", 40)
        self.optio_lista = ["Aloita peli", "Ohjeet", "Lopeta"]
        self.valittu_optio = 0
        self.ohjeet_nakymassa = False  # Uusi tila ohjenäkymälle

    def piirra_valikko(self):
        # Piirretään valikko näytölle
        self.naytto.fill((0, 0, 0))  # Täytetään näyttö mustalla
        for i, optio in enumerate(self.optio_lista):
            vari = (255, 0, 0) if i == self.valittu_optio else (255, 255, 255)
            teksti = self.fontti.render(optio, True, vari)
            self.naytto.blit(teksti, (self.naytto.get_width() // 2 - teksti.get_width() // 2, 200 + i * 100))

    def piirra_ohjeet(self):
        # Piirretään peliohjeet näytölle
        self.naytto.fill((0, 0, 0))  # Täytetään näyttö mustalla
        ohjeet_teksti = [
            "Ohjeet:",
            "Käytä WASD-näppäimiä liikkuaksesi ympäri karttaa.",
            "Tuhoa vihollisia",        ]

        for i, rivi in enumerate(ohjeet_teksti):
            teksti = self.pieni_fontti.render(rivi, True, (255, 255, 255))
            self.naytto.blit(teksti, (self.naytto.get_width() // 2 - teksti.get_width() // 2, 150 + i * 60))

    def paivita_valikko(self, tapahtuma):
        # Päivitetään valikon tila käyttäjän syötteiden mukaan
        if self.ohjeet_nakymassa:
            if tapahtuma.type == pygame.KEYDOWN and tapahtuma.key == pygame.K_ESCAPE:
                self.ohjeet_nakymassa = False  # Palaa takaisin valikkoon
            return True
        else:
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_UP:
                    self.valittu_optio = (self.valittu_optio - 1) % len(self.optio_lista)
                elif tapahtuma.key == pygame.K_DOWN:
                    self.valittu_optio = (self.valittu_optio + 1) % len(self.optio_lista)
                elif tapahtuma.key == pygame.K_RETURN:
                    if self.valittu_optio == 0:  # Aloita peli
                        return False  # Poistu valikosta ja aloita peli
                    elif self.valittu_optio == 1:  # Ohjeet
                        self.ohjeet_nakymassa = True  # Siirry ohjenäkymään
                    elif self.valittu_optio == 2:  # Lopeta peli
                        pygame.quit()
                        sys.exit()
            return True
