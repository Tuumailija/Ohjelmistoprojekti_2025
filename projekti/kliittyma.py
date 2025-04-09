import math
import pygame
import random
import sys
import os
import time
from tile_kartta import Kartta
from MapGen import Map, FLOOR, TILE_SIZE, WALL, CELL_WIDTH, CELL_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT
from player import Player
from raycast import RayCaster
from ovi import Door
from hud import *
from Vihollinen import Vihollinen

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
CELL_WIDTH, CELL_HEIGHT, TILE_SIZE = 11, 9, 64
MATRIX_ROWS, MATRIX_COLS = Kartta.korkeus, Kartta.pituus
PHYSICS_RENDER_DIST = 1000

# Määritellään projektin peruspolku (kuvia ja musiikkia varten)
project_dir = os.path.dirname(os.path.abspath(__file__))
# Lisäkkää tää kun käytätte jotain media kansiosta niin toimii kaikilla koneilla T. Markus
# katokkaa mallia musiikista ja taustakuvasta miten.


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


        valikko_tausta = os.path.join(project_dir, "media", "Img", "ValikkoTausta.jpg")
        if os.path.exists(valikko_tausta):
            print(f"Ladataan valikkotaustakuvaa: {valikko_tausta}")
            self.menu_background = pygame.image.load(valikko_tausta).convert()
            self.menu_tile_width = self.menu_background.get_width()
            self.menu_tile_height = self.menu_background.get_height()
        else:
            print(f"Valikkotaustakuvaa ei löytynyt polusta: {valikko_tausta}")
            self.menu_tile_width = TILE_SIZE
            self.menu_tile_height = TILE_SIZE
            self.menu_background = pygame.Surface((self.menu_tile_width, self.menu_tile_height))
            self.menu_background.fill((0, 0, 0))

        taustakuva = os.path.join(project_dir, "media", "Img", "WoodFloorTexture.jpg")
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
        musiikki_polku = os.path.join(project_dir, "media", "Aloitusmusiikki.mp3")
        if os.path.exists(musiikki_polku):
            print(f"Ladataan musiikkia: {musiikki_polku}")
            pygame.mixer.music.load(musiikki_polku)
            pygame.mixer.music.set_volume(0.5)
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
            os.path.join(project_dir, "media", "Taustamusiikki.mp3"),
            os.path.join(project_dir, "media", "Taustamusiikki2.mp3"),
            os.path.join(project_dir, "media", "Taustamusiikki3.mp3"),
            os.path.join(project_dir, "media", "Taustamusiikki4.mp3"),
        ]
        musiikki = random.choice(musiikin_polku)
        if os.path.exists(musiikki):
            print(f"Ladataan musiikkia: {musiikki}")
            pygame.mixer.music.load(musiikki)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        else:
            print(f"Taustamusiikkia ei löytynyt polusta: {musiikki}")

    def run(self):
        self.valikko_musiikki()
        #self.screen.fill((0, 0, 0)) piirtää vaan mustan taustan
        self.piirra_valikko()

    def piirra_valikko(self):
        optio_lista = ["Aloita peli", "Ohjeet", "Lopeta"]
        iso_fontti = pygame.font.SysFont("Arial", 60)
        while True:
            # Taustakuva
            valikko_tausta = pygame.transform.scale(self.menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(valikko_tausta, (0, 0))

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

    def kaynnista_peli(self):
        # Lopetetaan valikkos-musiikki ja aloitetaan pelimusiikki
        self.lopeta_valikko_musiikki()
        self.peli_musiikki()

        self.game_running = True
        matrix = Kartta.generoi_tile_matriisi()
        game_map = Map(matrix)
        hud = gamehud(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        start_r, start_c = MATRIX_ROWS // 2, 0
        start_x = (start_c * CELL_WIDTH + 1 + 10 // 2) * TILE_SIZE
        start_y = (start_r * CELL_HEIGHT + 1 + 8 // 2) * TILE_SIZE
        player = Player(start_x, start_y)

        debug_tile = game_map.get_debug_tile()  # DEBUG

        # Lista vihollisille ja parametrit spawnausta ja despawnausta varten
        enemies = []
        MAX_ENEMIES = 10
        SPAWN_INTERVAL = 3000         # Spawnataan uusi vihollinen x ms välein
        DESPAWN_DISTANCE = 1500       # Jos vihollinen on yli x pikselin päässä pelaajasta, se poistetaan
        spawn_timer = pygame.time.get_ticks()

        while self.game_running:
            self.current_time = pygame.time.get_ticks()
            dt = self.clock.tick(60)

            # Tapahtumakäsittely
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
                    # Debug-toimintoja
                    elif event.key == pygame.K_q:
                        hud.splatter(self.current_time)
                    elif event.key == pygame.K_c:
                        hud.redden(player.hp)
                        player.hp -= 10
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    player.attack()

            # Hae esteet (seinät + ovet) pelaajaa ympäriltä
            doors_in_radius = [door.rect for door in game_map.doors 
                                if not door.is_open and pygame.Vector2(door.rect.center).distance_to(pygame.Vector2(player.rect.center)) < PHYSICS_RENDER_DIST]
            walls = game_map.get_walls_in_radius(player.rect.centerx, player.rect.centery, PHYSICS_RENDER_DIST) + doors_in_radius

            # Päivitetään pelaaja ja liikutaan
            player.update(dt)
            player.move(pygame.key.get_pressed(), walls)

            # Kameran asetukset
            cam_x = max(-SCREEN_WIDTH // 2, min(player.rect.centerx - SCREEN_WIDTH // 2, game_map.map_width_px - SCREEN_WIDTH))
            cam_y = max(-SCREEN_HEIGHT // 2, min(player.rect.centery - SCREEN_HEIGHT // 2, game_map.map_height_px - SCREEN_HEIGHT))
            self.ray_caster.set_cam(cam_x, cam_y)

            # Piirretään taustakuva laattoina
            start_x_tile = -(cam_x % self.tile_width)
            start_y_tile = -(cam_y % self.tile_height)
            for x in range(start_x_tile, SCREEN_WIDTH, self.tile_width):
                for y in range(start_y_tile, SCREEN_HEIGHT, self.tile_height):
                    self.screen.blit(self.background, (x, y))

            # Käsitellään valaistuksen togglaus
            keys = pygame.key.get_pressed()
            if not hasattr(self, 'skip_lighting'):
                self.skip_lighting = False
            if keys[pygame.K_1]:
                self.skip_lighting = not self.skip_lighting
                pygame.time.wait(200)
            if not self.skip_lighting:
                light_mask = self.ray_caster.get_light_mask()
                self.screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Päivitetään esteet säteiden laskentaa varten
            self.ray_caster.set_obstacles(walls)
            for wall in walls:
                pygame.draw.rect(self.screen, (0, 0, 0), 
                                pygame.Rect(wall.x - cam_x, wall.y - cam_y, wall.width, wall.height))

            # Päivitetään ja piirretään valot
            lights = game_map.get_lights_in_radius(player.rect.centerx, player.rect.centery, PHYSICS_RENDER_DIST * 1.5)
            angle = self.kulma_pelaajan_ja_hiiren_valilla(player, cam_x, cam_y)
            self.ray_caster.set_valot(lights)
            self.ray_caster.update_rays((player.rect.centerx - cam_x, player.rect.centery - cam_y), angle)
            player.set_lighting(lights, walls)
            player.draw(self.screen, cam_x, cam_y, angle)

            # Piirretään voittoruutu ja debug-ruutu
            pygame.draw.rect(self.screen, (255, 255, 0), 
                            pygame.Rect(game_map.win_tile.x - cam_x, game_map.win_tile.y - cam_y, game_map.win_tile.width, game_map.win_tile.height))
            pygame.draw.rect(self.screen, (255, 165, 0), 
                            pygame.Rect(debug_tile.x - cam_x, debug_tile.y - cam_y, debug_tile.width, debug_tile.height))

            # Tarkistetaan, osuuko pelaaja debug-ruutuun tai voittoruudulle
            if player.rect.colliderect(debug_tile):
                print("DEBUG: osuma toisen huoneen laatikkoon")
                self.game_running = False
                return
            if player.rect.colliderect(game_map.win_tile):
                print("Voitit pelin!")
                self.game_running = False
                return
            
            # Spawnaus tapahtuu aikarajalla
            if self.current_time - spawn_timer > SPAWN_INTERVAL and len(enemies) < MAX_ENEMIES:
                player_row = player.rect.centery // (CELL_HEIGHT * TILE_SIZE)
                player_col = player.rect.centerx // (CELL_WIDTH * TILE_SIZE)
                player_room_id = matrix[player_row][player_col]
                room_center_dict = game_map.get_room_center_dict()

                valid_spawn_points = [
                    center for room_id, center in room_center_dict.items()
                    if room_id != player_room_id and pygame.Vector2(center).distance_to(player.rect.center) < DESPAWN_DISTANCE
                ]

                if valid_spawn_points:
                    spawn_pos = random.choice(valid_spawn_points)
                    enemies.append(Vihollinen(spawn_pos[0], spawn_pos[1]))
                spawn_timer = self.current_time

            # Tämä osa siirretään ulkopuolelle ja suoritetaan JOKA framella
            for enemy in enemies[:]:
                if pygame.math.Vector2(enemy.rect.center).distance_to(player.rect.center) > DESPAWN_DISTANCE:
                    enemies.remove(enemy)
                else:
                    enemy.update(dt, player.rect, matrix, game_map)
                    enemy.draw(self.screen, cam_x, cam_y)

            # Piirretään HUD ja päivitetään näyttö
            hud.draw(self.current_time)
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
    
