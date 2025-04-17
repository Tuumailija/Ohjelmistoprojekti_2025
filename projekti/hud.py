import pygame
import os
import random

project_dir = os.path.dirname(os.path.abspath(__file__)) # Lisätty tämä niin saadaan kuvat toimii millä tahansa koneella T. Markus

class gamehud:
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT):

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

        #perus hud-elementtäejä taso
        #tähän piirretään pelaajan hp sun muita mitä nyt hudiin tahdotaan.
        #self.general_hud = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)

        #veriläiskä taso
        self.player_splatter_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        #veriläiskän kuva
        self.splatterimg = pygame.image.load(self.path_splatter).convert_alpha()
        self.splatterimg = pygame.transform.scale(self.splatterimg, (self.splatterimg.get_width()/2, self.splatterimg.get_height()/2))
        #aika jolloin splatteri poistetaan (current_time+2000)
        self.pyyhipois = 0

        #punaisen reunustan taso
        self.player_hp_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        self.redborder = pygame.image.load(self.path_redden).convert_alpha()
        self.redborder.set_alpha(0)
        self.redborder_rect = self.redborder.get_rect()
        self.lastdrawnhp = 40693

    def splatter(self, current_time):
        self.pyyhipois = current_time+2000

        for _ in range(20):
            #satunnainen x,y ruudulla
            x = random.randint(0, self.sw - 1)
            y = random.randint(0, self.sh - 1)

            self.player_splatter_layer.blit(self.splatterimg, (x, y))

    def redden(self, hp):
        # piirrä hudiin punainen reunusta
        # reunustan läpinäkyvyys riippuu pelaajan hp määrästä

        # toteutus vielä vituillaan
        # tässä ehkä tarvitsee vain säätää sen kuvan läpinäkyvyys, sen voi periaatteessa aina piirtää.
        newalpha = (100-hp) * 3
        if newalpha < 0:
            newalpha = 0

        print(newalpha)

        self.redborder.set_alpha(newalpha)
        self.redborder_rect = self.redborder.get_rect()
        self.player_hp_layer.blit(self.redborder, (0, 0), self.redborder_rect)
        self.lastdrawnhp = hp
    
    def draw(self, current_time, hp):
        #punaiset reunat jos hahmo on kipeä
        if self.lastdrawnhp is not hp:
            self.player_hp_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
            self.redden(hp)
        
        self.screen.blit(self.player_hp_layer, (0, 0))
        
        #piirrä veriläiskätaso
        if current_time > self.pyyhipois:
            self.player_splatter_layer = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        else:
            self.screen.blit(self.player_splatter_layer, (0, 0))

        text_surface = pygame.font.SysFont('Forte', 72).render('HP: ' + str(hp), False, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))