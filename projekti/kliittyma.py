import math
import pygame
import random
import sys
import os
import time
from tile_kartta import Kartta
from MapGen import Map, FLOOR, TILE_SIZE, WALL, CELL_WIDTH, CELL_HEIGHT
from player import Player
from raycast import RayCaster
from Vihollinen import Vihollinen
from ovi import Door

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
CELL_WIDTH, CELL_HEIGHT, TILE_SIZE = 11, 9, 64
MATRIX_ROWS, MATRIX_COLS = Kartta.korkeus, Kartta.pituus
PHYSICS_RENDER_DIST = 1000

class Kliittyma:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Peli")
        self.ray_caster = RayCaster(self.screen, PHYSICS_RENDER_DIST)
        self.game_running = False
        self.musiikki_soi = False

        self.clock = pygame.time.Clock()

        self.viholliset = []

        taustakuva = os.path.join(os.getcwd(),"projekti", "media", "Img", "StoneFloorTexture.png")
        if os.path.exists(taustakuva):
            self.background = pygame.image.load(taustakuva).convert()
            self.tile_width = self.background.get_width()
            self.tile_height = self.background.get_height()
        else:
            print(f"Taustakuvaa ei löytynyt polusta: {taustakuva}")
            self.tile_width = TILE_SIZE
            self.tile_height = TILE_SIZE
            self.background = pygame.Surface((self.tile_width, self.tile_height))
            self.background.fill((100, 100, 100))  # Lataa harmaan lattian

    def valikko_musiikki(self):
        base_dir = os.path.dirname(__file__)
        musiikki_polku = os.path.join(base_dir,"projekti", "media", "Aloitusmusiikki.mp3")
        if os.path.exists(musiikki_polku):
            print(f"Ladataan musiikkia: {musiikki_polku}")
            pygame.mixer.init()
            pygame.mixer.music.load(musiikki_polku)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            self.musiikki_soi = True
        else:
            print(f"Aloitusmusiikkia ei löytynyt polusta: {musiikki_polku}")

    def lopeta_valikko_musiikki(self):
        if self.musiikki_soi:
            pygame.mixer.music.stop()
            self.musiikki_soi = False

    def peli_musiikki(self):
        musiikin_polku = [
            os.path.join(os.getcwd(),"projekti", "media", "Taustamusiikki.mp3"),
            os.path.join(os.getcwd(),"projekti", "media", "Taustamusiikki2.mp3"),
            os.path.join(os.getcwd(),"projekti", "media", "Taustamusiikki3.mp3"),
            os.path.join(os.getcwd(),"projekti", "media", "Taustamusiikki4.mp3"),
        ]
        musiikki = random.choice(musiikin_polku)
        if os.path.exists(musiikki):
            print(f"Ladataan musiikkia: {musiikki}")
            pygame.mixer.init()
            pygame.mixer.music.load(musiikki)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
        else:
            print(f"Taustamusiikkia ei löytynyt polusta: {musiikki}")

    def run(self):
        self.screen.fill((0, 0, 0))
        self.piirra_valikko()

    def piirra_valikko(self):
        optio_lista = ["Aloita peli", "Ohjeet", "Lopeta"]
        iso_fontti = pygame.font.SysFont("Arial", 60)
        while True:
            self.screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            valittu_optio = -1
            keski_x = self.screen.get_width() // 2
            keski_y = self.screen.get_height() // 2 - (len(optio_lista) * 50 // 2)
            for i, optio in enumerate(optio_lista):
                teksti = iso_fontti.render(optio, True, (255, 255, 255))
                teksti_rect = teksti.get_rect(center=(keski_x, keski_y + i * 100))
                if teksti_rect.collidepoint(mouse_pos):
                    teksti = iso_fontti.render(optio, True, (255, 0, 0))
                    valittu_optio = i
                self.screen.blit(teksti, teksti_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if valittu_optio == 0:
                        self.kaynnista_peli()
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
            "Paina E-näppäintä avataksesi ovia.",
            "Käytä hiirtä kääntääksesi pelaajan katsetta.",
            "Poistu ohjeista painamalla ESC",
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

    def luo_viholliset(self, game_map, maara=500):
        viholliset = []
        vapaat_ruudut = []
        rows = len(game_map.tilemap)
        cols = len(game_map.tilemap[0])
        for y in range(1, rows - 1):
            for x in range(1, cols - 1):
                if game_map.tilemap[y][x] == FLOOR:
                    if (game_map.tilemap[y-1][x] == FLOOR and 
                        game_map.tilemap[y+1][x] == FLOOR and 
                        game_map.tilemap[y][x-1] == FLOOR and 
                        game_map.tilemap[y][x+1] == FLOOR):
                        vapaat_ruudut.append((x, y))
        print("Löydetty vapaita ruutuja:", len(vapaat_ruudut))
    
        if not vapaat_ruudut:
            print("Ei vapaita ruutuja, käytetään kaikkia lattiaruutuja")
            vapaat_ruudut = [(x, y) for y in range(rows) for x in range(cols) if game_map.tilemap[y][x] == FLOOR]

        for _ in range(maara):
            x, y = random.choice(vapaat_ruudut)
            enemy_x = x * TILE_SIZE + TILE_SIZE // 2 - 20
            enemy_y = y * TILE_SIZE + TILE_SIZE // 2 - 20
            viholliset.append(Vihollinen(enemy_x, enemy_y))
        print("Luodaan vihollisia:", len(viholliset))
        return viholliset

    def kaynnista_peli(self):
        self.game_running = True
        matrix = Kartta.generoi_tile_matriisi()
        game_map = Map(matrix)
        self.viholliset = self.luo_viholliset(game_map, 500)
        #veriläiskä taso
        self.player_splatter_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.show_verilaiska = False
        self.pyyhipois = 0
        start_r, start_c = MATRIX_ROWS // 2, 0
        start_x = (start_c * CELL_WIDTH + 1 + 10 // 2) * TILE_SIZE
        start_y = (start_r * CELL_HEIGHT + 1 + 8 // 2) * TILE_SIZE
        player = Player(start_x, start_y)

        while self.game_running:
            self.current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_running = False
                        return
                    
                    elif event.key == pygame.K_e:
                        for door in game_map.doors:
                            if pygame.Vector2(player.rect.center).distance_to(pygame.Vector2(door.rect.center)) < 64:
                                door.toggle(self.kulma_pelaajan_ja_hiiren_valilla(player, 0, 0))
                    #debug veri
                    elif event.key == pygame.K_q:
                        self.hud_splatter()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    player.attack()

            doors_in_radius = [door.rect for door in game_map.doors if not door.is_open and pygame.Vector2(door.rect.center).distance_to(pygame.Vector2(player.rect.center)) < PHYSICS_RENDER_DIST]
            walls = game_map.get_walls_in_radius(player.rect.centerx, player.rect.centery, PHYSICS_RENDER_DIST) + doors_in_radius
            dt = self.clock.tick(60)
            player.update(dt)
            player.move(pygame.key.get_pressed(), walls)
            cam_x = max(0, min(player.rect.centerx - SCREEN_WIDTH // 2, game_map.map_width_px - SCREEN_WIDTH))
            cam_y = max(0, min(player.rect.centery - SCREEN_HEIGHT // 2, game_map.map_height_px - SCREEN_HEIGHT))
            self.ray_caster.set_cam(cam_x, cam_y)
            start_x_tile = - (cam_x % self.tile_width)
            start_y_tile = - (cam_y % self.tile_height)

            for x in range(start_x_tile, SCREEN_WIDTH, self.tile_width):
                for y in range(start_y_tile, SCREEN_HEIGHT, self.tile_height):
                    self.screen.blit(self.background, (x, y))

            light_mask = self.ray_caster.get_light_mask()
            self.screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.ray_caster.set_obstacles(walls)

            for wall in walls:
                pygame.draw.rect(self.screen, (0, 0, 0), 
                                 pygame.Rect(wall.x - cam_x, wall.y - cam_y, wall.width, wall.height))
                
            lights = game_map.get_lights_in_radius(player.rect.centerx, player.rect.centery, PHYSICS_RENDER_DIST * 1.5)
            self.ray_caster.set_valot(lights)
            angle = self.kulma_pelaajan_ja_hiiren_valilla(player, cam_x, cam_y)
            self.ray_caster.update_rays((player.rect.centerx - cam_x, player.rect.centery - cam_y), angle)
            player.draw(self.screen, cam_x, cam_y, angle)

            # Päivitetään viholliset, huomioiden törmäykset sekä pelaajaan
            for vihollinen in self.viholliset:
                vihollinen.update(walls, self.viholliset, player)
            for vihollinen in self.viholliset:
                vihollinen.piirra(self.screen, cam_x, cam_y)

            #piirrä ui elementit
            self.draw_ui() 

            pygame.display.flip()

    def kulma_pelaajan_ja_hiiren_valilla(self, player, cam_x, cam_y):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = player.rect.centerx, player.rect.centery
        mouse_x += cam_x
        mouse_y += cam_y
        dx = mouse_x - player_x
        dy = mouse_y - player_y
        angle = math.degrees(math.atan2(dy, dx))
        return angle

    def hud_splatter(self):
        self.show_verilaiska = True
        self.pyyhipois = self.current_time+2000
        borderwidth = 0

        for _ in range(5):
            #satunnainen x,y ruudulla
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)

            #luo 50x50 punainen loota
            pygame.draw.rect(self.player_splatter_layer, (255, 0, 0), (x, y, 50, 50), borderwidth)
    
    def draw_ui(self):


        #laske 2 sekuntia, sitten laita self.show_verilaiska = False
        if self.current_time > self.pyyhipois:
            self.show_verilaiska = False
            self.player_splatter_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        if self.show_verilaiska:
            self.screen.blit(self.player_splatter_layer, (0, 0))