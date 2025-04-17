import pygame
import os
import random

project_dir = os.path.dirname(os.path.abspath(__file__)) # Lisätty tämä niin saadaan kuvat toimii millä tahansa koneella T. Markus

class gamehud:
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.max_hp = 100
        self.path_redden = os.path.join(project_dir, "media", "Img", "hud_hurtborder.png")
        if os.path.exists(self.path_redden):
            print(f"Kuvan polku on oikein {self.path_redden}")
        else:
            print(f"Kuvan polku on väärin: {self.path_redden}")

        self.path_splatter = os.path.join(project_dir, "media", "Img", "hud_splatter.png")
        if os.path.exists(self.path_splatter):
            print(f"Kuvan polku on oikein {self.path_splatter}")
        else:
            print(f"Kuvan polku on väärin: {self.path_splatter}")

        self.screen = screen
        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        
        #veriläiskä taso
        self.player_splatter_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        #veriläiskän kuva
        self.splatterimg = pygame.image.load(self.path_splatter).convert_alpha()
        self.splatterimg = pygame.transform.scale(self.splatterimg, (self.splatterimg.get_width()/2, self.splatterimg.get_height()/2))
        #aika jolloin splatteri poistetaan (current_time+2000)
        self.pyyhipois = 0

        #punaisen reunustan taso
        self.player_hp_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

    def splatter(self, current_time):
        self.pyyhipois = current_time+2000

        for _ in range(20):
            #satunnainen x,y ruudulla
            x = random.randint(0, self.sw - 1)
            y = random.randint(0, self.sh - 1)

            self.player_splatter_layer.blit(self.splatterimg, (x, y))

    def redden(self, hp):
        # Laske pudotetun HP:n osuus (0–1)
        damage_ratio = max(0.0, min(1.0, (self.max_hp - hp) / self.max_hp))
        # Maksimi‑alpha (voimakkuus)
        max_alpha = 180
        red_alpha = int(damage_ratio * max_alpha)

        # Luo punainen semi‑läpinäkyvä pinta
        overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, red_alpha))
        # Blitataan se layerille
        self.player_hp_layer.blit(overlay, (0, 0))



    def draw(self, current_time, hp):
        # Piirretään punainen overlay aina HP:n mukaan
        self.player_hp_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        self.redden(hp)
        self.screen.blit(self.player_hp_layer, (0, 0))

        # Veriläiskät
        if current_time > self.pyyhipois:
            self.player_splatter_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        else:
            self.screen.blit(self.player_splatter_layer, (0, 0))

        # HP‑teksti
        text_surface = pygame.font.SysFont('Forte', 72).render('HP: ' + str(int(hp)), False, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))

