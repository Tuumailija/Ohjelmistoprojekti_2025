import random
import pygame
import sys
import os
from raycast import RayCaster

class Kliittyma:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.ray_caster = RayCaster(self.screen, ray_length=2000)
        self.obstacles = []
        pygame.display.set_caption("Peli")

    def run(self):
        self.screen.fill((0, 0, 0))
        self.piirra_valikko()

    def piirra_valikko(self):
        optio_lista = ["Aloita peli", "Ohjeet", "Lopeta"]
        while True:
            self.screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            valittu_optio = -1
            for i, optio in enumerate(optio_lista):
                teksti = pygame.font.SysFont("Arial", 60).render(optio, True, (255, 255, 255))
                teksti_rect = teksti.get_rect(center=(self.screen.get_width() // 2, 200 + i * 100))
                if teksti_rect.collidepoint(mouse_pos):
                    teksti = pygame.font.SysFont("Arial", 60).render(optio, True, (255, 0, 0))
                    valittu_optio = i
                self.screen.blit(teksti, teksti_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if valittu_optio == 0:
                        self.luo_tyhja_huone()
                    elif valittu_optio == 1:
                        self.piirra_ohjeet()
                    elif valittu_optio == 2:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
        pieni_fontti = pygame.font.SysFont("Arial", 40)
        for i, rivi in enumerate(ohjeet_teksti):
            teksti = pieni_fontti.render(rivi, True, (255, 255, 255))
            self.screen.blit(teksti, (self.screen.get_width() // 2 - teksti.get_width() // 2, 150 + i * 60))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

    def generoi_esteet(self, määrä=5):
        """Luo satunnaisia esteitä ja tallentaa ne listaan."""
        self.esteet = []
        for _ in range(määrä):
            x1 = random.randint(50, 750)
            y1 = random.randint(50, 550)
            x2 = x1 + random.randint(20, 100)
            y2 = y1 + random.randint(20, 100)
            self.esteet.append((x1, y1, x2, y2))
        self.ray_caster.set_obstacles(self.esteet)  # Lähetetään esteet RayCasterille
        
    def luo_tyhja_huone(self):
        """Luo huone satunnaisilla esteillä ja näyttää säteet hiiren kohdalta."""
        self.screen.fill((50, 50, 50))
        self.generoi_esteet()  # Luodaan uudet esteet
        running = True
        
        while running:
            self.screen.fill((50, 50, 50))
            mouse_pos = pygame.mouse.get_pos()
            self.ray_caster.update_rays(mouse_pos)  # Säteen lähtökohta on hiiren sijainti
            self.ray_caster.draw(mouse_pos)
            
            # Piirretään esteet
            for wall in self.esteet:
                pygame.draw.line(self.screen, (255, 0, 0), (wall[0], wall[1]), (wall[2], wall[3]), 3)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False