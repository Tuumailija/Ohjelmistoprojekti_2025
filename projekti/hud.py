import pygame
import random

class gamehud:
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.screen = screen
        #veriläiskä taso
        self.player_splatter_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.pyyhipois = 0
        #punaisen reunustan taso
        self.player_hp_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    def hud_splatter(self, SCREEN_WIDTH, SCREEN_HEIGHT, current_time):
        self.pyyhipois = current_time+2000
        borderwidth = 0

        for _ in range(5):
            #satunnainen x,y ruudulla
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)

            #luo 50x50 punainen loota
            pygame.draw.rect(self.player_splatter_layer, (255, 0, 0), (x, y, 50, 50), borderwidth)

    def hud_redden(self):
        # piirrä hudiin punainen reunusta
        # reunustan läpinäkyvyys riippuu pelaajan hp määrästä

        self.screen.blit(self.player_hp_layer, (0, 0))
    
    def draw_hud(self, SCREEN_WIDTH, SCREEN_HEIGHT, current_time):
        #laske 2 sekuntia, sitten laita self.show_verilaiska = False
        if current_time > self.pyyhipois:
            self.player_splatter_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        else:
            self.screen.blit(self.player_splatter_layer, (0, 0))

        self.hud_redden()