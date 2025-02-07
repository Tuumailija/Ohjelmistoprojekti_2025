# Aloitusvalikko.py
import pygame

class Aloitusvalikko:
    def __init__(self, naytto):
        self.naytto = naytto
        self.fontti = pygame.font.SysFont("Arial", 50)
        self.optio_lista = ["Aloita peli", "Lopeta"]
        self.valittu_optio = 0

    def piirra_valikko(self):
        self.naytto.fill((0, 0, 0))  # Täytetään näyttö mustalla
        for i, optio in enumerate(self.optio_lista):
            vari = (255, 0, 0) if i == self.valittu_optio else (255, 255, 255)
            teksti = self.fontti.render(optio, True, vari)
            self.naytto.blit(teksti, (self.naytto.get_width() // 2 - teksti.get_width() // 2, 200 + i * 100))

    def paivita_valikko(self, tapahtuma):
        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_UP:
                self.valittu_optio = (self.valittu_optio - 1) % len(self.optio_lista)
            elif tapahtuma.key == pygame.K_DOWN:
                self.valittu_optio = (self.valittu_optio + 1) % len(self.optio_lista)
            elif tapahtuma.key == pygame.K_RETURN:
                if self.valittu_optio == 0:  # Aloita peli
                    return False  # Poistu valikosta
                elif self.valittu_optio == 1:  # Lopeta peli
                    pygame.quit()
        return True
