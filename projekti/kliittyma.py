import pygame
import sys
import os

class Kliittyma:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fontti = pygame.font.SysFont("Arial", 60)
        self.pieni_fontti = pygame.font.SysFont("Arial", 40)
        pygame.display.set_caption("Peli")

    def run(self):
        #running = True
        self.screen.fill((0, 0, 0))
        self.piirra_valikko()

    def piirra_valikko(self):
        optio_lista = ["Aloita peli", "Ohjeet", "Lopeta"]
        while True:
            self.screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            valittu_optio = -1
            for i, optio in enumerate(optio_lista):
                teksti = self.fontti.render(optio, True, (255, 255, 255))
                teksti_rect = teksti.get_rect(center=(self.screen.get_width() // 2, 200 + i * 100))
                if teksti_rect.collidepoint(mouse_pos):
                    teksti = self.fontti.render(optio, True, (255, 0, 0))
                    valittu_optio = i
                self.screen.blit(teksti, teksti_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if valittu_optio != -1:
                        if valittu_optio == 0:
                            self.luo_tyhja_huone();
                        elif valittu_optio == 1:
                            self.piirra_ohjeet()
                        elif valittu_optio == 2:
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def piirra_ohjeet(self):
        self.screen.fill((0, 0, 0))
        ohjeet_teksti = [
            "Ohjeet:",
            "Käytä WASD-näppäimiä liikkuaksesi ympäri karttaa.",
            "Tuhoa vihollisia",
            "Poistu ohjeista painamalla ESC"
            ]
        for i, rivi in enumerate(ohjeet_teksti):
            teksti = self.pieni_fontti.render(rivi, True, (255, 255, 255))
            self.screen.blit(teksti, (self.screen.get_width() // 2 - teksti.get_width() // 2, 150 + i * 60))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

    def luo_tyhja_huone(self):
        """Luo tyhjän huoneen ilman esteitä tai objekteja."""
        self.screen.fill((50, 50, 50))  # Harmaa tausta huoneelle
        
        # Määritellään seinien väri ja paksuus
        seinan_vari = (200, 200, 200)  # Vaaleanharmaa
        seinan_paksuus = 10
        leveys, korkeus = self.screen.get_size()
        
        # Piirretään seinät
        pygame.draw.rect(self.screen, seinan_vari, (0, 0, leveys, seinan_paksuus))  # Yläseinä
        pygame.draw.rect(self.screen, seinan_vari, (0, 0, seinan_paksuus, korkeus))  # Vasenseinä
        pygame.draw.rect(self.screen, seinan_vari, (0, korkeus - seinan_paksuus, leveys, seinan_paksuus))  # Alaseinä
        pygame.draw.rect(self.screen, seinan_vari, (leveys - seinan_paksuus, 0, seinan_paksuus, korkeus))  # Oikea seinä
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Poistutaan huoneesta ESC-näppäimellä

