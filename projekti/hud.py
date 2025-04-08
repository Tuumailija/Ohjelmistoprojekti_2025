import pygame
import os
import random

project_dir = os.path.dirname(os.path.abspath(__file__)) # Lisätty tämä niin saadaan kuvat toimii millä tahansa koneella T. Markus

class gamehud:
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.path_redden = os.path.join(project_dir, "media", "Img", "hud_hurtborder.png")
        self.screen = screen
        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT

        #veriläiskä taso
        self.player_splatter_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        #aika jolloin splatteri poistetaan (current_time+2000)
        self.pyyhipois = 0

        #punaisen reunustan taso
        self.player_hp_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        self.redborder = pygame.image.load(self.path_redden).convert_alpha()
        self.redborder.set_alpha(0)
        self.redborder_rect = self.redborder.get_rect()

    def splatter(self, current_time):
        self.pyyhipois = current_time+2000
        borderwidth = 0

        for _ in range(5):
            #satunnainen x,y ruudulla
            x = random.randint(0, self.sw - 1)
            y = random.randint(0, self.sh - 1)

            #luo 50x50 punainen loota
            pygame.draw.rect(self.player_splatter_layer, (255, 0, 0), (x, y, 50, 50), borderwidth)

    def redden(self, hp):
        # piirrä hudiin punainen reunusta
        # reunustan läpinäkyvyys riippuu pelaajan hp määrästä

        # toteutus vielä vituillaan
        # tässä ehkä tarvitsee vain säätää sen kuvan läpinäkyvyys, sen voi periaatteessa aina piirtää.
        self.redborder.set_alpha(hp)
        self.redborder_rect = self.redborder.get_rect()
    
    def draw(self, current_time):
        #punaiset reunat jos hahmo on kipeä
        self.player_hp_layer.blit(self.player_hp_layer, (0, 0), self.redborder_rect)

        #laske 2 sekuntia, sitten laita self.show_verilaiska = False
        if current_time > self.pyyhipois:
            self.player_splatter_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        else:
            self.screen.blit(self.player_splatter_layer, (0, 0))