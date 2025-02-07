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
                            print("Aloita peli")
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
        

    def run(self):
        #running = True
        self.screen.fill((0, 0, 0))
        self.piirra_valikko()
        #while running:
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            running = False
        #        elif event.type == pygame.KEYDOWN:
        #            if event.key == pygame.K_ESCAPE:
        #                running = False
        #    pygame.display.flip()
        #pygame.quit()