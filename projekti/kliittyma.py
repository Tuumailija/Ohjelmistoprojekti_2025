import math
import pygame
import random
import sys
import os
from tile_kartta import Kartta  
from MapGen import Map, FLOOR, TILE_SIZE
from player import Player
from raycast import RayCaster
from Vihollinen import Vihollinen

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
CELL_WIDTH, CELL_HEIGHT, TILE_SIZE = 11, 9, 64
MATRIX_ROWS, MATRIX_COLS = Kartta.korkeus, Kartta.pituus

class Kliittyma:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Peli")
        self.clock = pygame.time.Clock()
        self.ray_caster = RayCaster(self.screen, ray_length=1000)
        self.game_running = False
        self.musiikki_soi = False

        self.viholliset = []

    def valikko_musiikki(self):
        musiikki_polku = os.path.join(os.getcwd(), "Ohjelmistoprojekti_2025", "projekti", "media", "Aloitusmusiikki.mp3")
        if os.path.exists(musiikki_polku): # Tarkistaa onko musiikki tiedosto olemassa, niin ei kräshää 
            print(f"Ladataan musiikkia: {musiikki_polku}")
            pygame.mixer.init()
            pygame.mixer.music.load(musiikki_polku)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            self.musiikki_soi = True
        else :
            print(f"Aloitusmusiikkia ei löytynyt polusta: {musiikki_polku}")
            # pygame.mixer.quit()

    def lopeta_valikko_musiikki(self):
        if self.musiikki_soi:
            pygame.mixer.music.stop()
            self.musiikki_soi = False


    def peli_musiikki(self):
        musiikin_polku = [
            os.path.join(os.getcwd(), "Ohjelmistoprojekti_2025", "projekti", "media", "Taustamusiikki.mp3"),
            os.path.join(os.getcwd(), "Ohjelmistoprojekti_2025", "projekti", "media", "Taustamusiikki2.mp3"),
            os.path.join(os.getcwd(), "Ohjelmistoprojekti_2025", "projekti", "media", "Taustamusiikki3.mp3"),
            os.path.join(os.getcwd(), "Ohjelmistoprojekti_2025", "projekti", "media", "Taustamusiikki4.mp3"),
        ]
        musiikki = random.choice(musiikin_polku)
        if os.path.exists(musiikki): # Tarkistaa onko musiikki tiedosto olemassa, niin ei kräshää
            print(f"Ladataan musiikkia: {musiikki}")
            pygame.mixer.init()
            pygame.mixer.music.load(musiikki)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
        else:
            print(f"Taustamusiikkia ei löytynyt polusta: {musiikki}")
            # pygame.mixer.quit()


    """  def Kuolema_aani(self):
        kuolema_aani_polku = os.path.join(os.getcwd(), "Ohjelmistoprojekti_2025", "projekti", "media", "Kuolema_aani.mp3")
        if os.path.exists(kuolema_aani_polku): # Tarkistaa onko musiikki tiedosto olemassa, niin ei kräshää
            pygame.mixer.init()
            pygame.mixer.music.load(kuolema_aani_polku)
            pygame.mixer.music.play()

        else:
            print("Kuolema ääntä ei löytynyt")
            # pygame.mixer.quit()
            
            """  # Tämä muokataan vielä myöhemmin kun pelaajan hitscan on valmis ja liitetään eri metodiin T. Markus



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

            for i, optio in enumerate(optio_lista):
                teksti = iso_fontti.render(optio, True, (255, 255, 255))
                teksti_rect = teksti.get_rect(center=(self.screen.get_width() // 2, 200 + i * 100))
                if teksti_rect.collidepoint(mouse_pos):
                    teksti = iso_fontti.render(optio, True, (255, 0, 0))
                    valittu_optio = i
                self.screen.blit(teksti, teksti_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if valittu_optio == 0:
                        self.kaynnista_peli()
                        # pygame.mixer.quit() #Lopettaa aloitus musiikin soiton
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

    # Ei tällä hetkellä vaikuta muuttavan mitään kun peliä runnataan        
    """
    def generoi_esteet(self, määrä=5):
        # Luo satunnaisia esteitä ja tallentaa ne listaan.
        self.esteet = []
        for _ in range(määrä):
            x1 = random.randint(50, 750)
            y1 = random.randint(50, 550)
            x2 = x1 + random.randint(20, 100)
            y2 = y1 + random.randint(20, 100)
            self.esteet.append((x1, y1, x2, y2))
        self.ray_caster.set_obstacles(self.esteet)  # Lähetetään esteet RayCasterille
    """

    def luo_viholliset(self, game_map, maara=40): #maara kertoo kuinka monta vihollista luodaan
        viholliset = []
        vapaat_ruudut = [(x, y) for y in range(len(game_map.tilemap)) for x in range(len(game_map.tilemap[y])) if game_map.tilemap[y][x] == FLOOR]

        for _ in range(maara):
            x, y = random.choice(vapaat_ruudut)
            viholliset.append(Vihollinen(x * TILE_SIZE, y * TILE_SIZE))
        return viholliset


    def kaynnista_peli(self):
        #pygame.display.set_mode((1200, 1000))
        # Käynnistää pelin main menu ruutuun
        self.game_running = True
        matrix = Kartta.generoi_tile_matriisi()
        game_map = Map(matrix)
    
        # Luodaan pelaaja ja asetetaan aloituspaikka
        start_r, start_c = MATRIX_ROWS // 2, 0
        start_x = (start_c * CELL_WIDTH + 1 + 10 // 2) * TILE_SIZE
        start_y = (start_r * CELL_HEIGHT + 1 + 8 // 2) * TILE_SIZE
        player = Player(start_x, start_y)

        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_running = False
                    return

            player.move(pygame.key.get_pressed(), game_map.wall_rects)

            # Kamera seuraa pelaajaa
            cam_x = max(0, min(player.rect.centerx - SCREEN_WIDTH // 2, game_map.map_width_px - SCREEN_WIDTH))
            cam_y = max(0, min(player.rect.centery - SCREEN_HEIGHT // 2, game_map.map_height_px - SCREEN_HEIGHT))
            self.ray_caster.set_cam(cam_x, cam_y)

            # Piirretään kartta
            self.screen.fill((0, 0, 0))
            game_map.draw(self.screen, cam_x, cam_y)

            walls = game_map.get_walls_in_radius(player.rect.centerx, player.rect.centery, 1000)
            self.ray_caster.set_obstacles(walls)
            # Piirretään seinät ja lisätään kameran offset
            for wall in walls:
                pygame.draw.rect(self.screen, (255, 0, 0), 
                                 pygame.Rect(wall.x - cam_x, wall.y - cam_y, wall.width, wall.height))
            

            lights = game_map.get_lights_in_radius(player.rect.centerx, player.rect.centery, 200)

            # Piirretään pallo pelaajan aloituspaikkaan
            pygame.draw.circle(self.screen, (0, 255, 0), (start_x - cam_x, start_y - cam_y), 10)
            self.ray_caster.set_valot(pygame.Vector2(start_x - cam_x, start_y - cam_y))

            # Laske kulma pelaajan ja hiiren välillä
            angle = self.kulma_pelaajan_ja_hiiren_valilla(player, cam_x, cam_y)
            
            # Päivitetään raycasterin säteet ja piirretään ne
            self.ray_caster.update_rays((player.rect.centerx - cam_x, player.rect.centery - cam_y), angle)
            self.ray_caster.draw((player.rect.centerx - cam_x, player.rect.centery - cam_y))

            # Piirretään pelaaja
            player.draw(self.screen, cam_x, cam_y)

            # Piirretään vihollinen
            for vihollinen in self.viholliset:
                vihollinen.piirrä(self.screen, cam_x, cam_y)
            
            pygame.display.flip()

    def kulma_pelaajan_ja_hiiren_valilla(self, player, cam_x, cam_y):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = player.rect.centerx, player.rect.centery

        # Adjust for camera position
        mouse_x += cam_x
        mouse_y += cam_y

        # Calculate the difference in x and y coordinates
        dx = mouse_x - player_x
        dy = mouse_y - player_y

        # Calculate the angle in radians and then convert to degrees
        angle = math.degrees(math.atan2(dy, dx))

        return angle