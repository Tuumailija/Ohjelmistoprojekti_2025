import pygame
import os
import math

PLAYER_SIZE = 32
PLAYER_SPEED = 5

class Player:
    def __init__(self, start_x, start_y):
        self.rect = pygame.Rect(start_x, start_y, PLAYER_SIZE, PLAYER_SIZE)

        # Pelaajan hattu
        hattu_path = os.path.join("projekti", "media", "Img", "pelaaja.png")
        if os.path.exists(hattu_path):
            hattu_orig = pygame.image.load(hattu_path).convert_alpha()
            hattu_scaled = pygame.transform.scale(hattu_orig, (int(PLAYER_SIZE * 2), int(PLAYER_SIZE * 2)))
            self.hattu_image = pygame.transform.rotate(hattu_scaled, -90)
        else:
            print(f"Virhe: Pelaajakuvaa ei löytynyt polusta: {hattu_path}")
            self.hattu_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.hattu_image.fill((0, 150, 0))

        # Pelaajan ase
        ase_path = os.path.join("projekti", "media", "Img", "pelaajaAse.png")
        if os.path.exists(ase_path):
            ase_orig = pygame.image.load(ase_path).convert_alpha()
            ase_scaled = pygame.transform.scale(ase_orig, (int(PLAYER_SIZE * 4.5), int(PLAYER_SIZE * 4.5)))
            self.ase_image = pygame.transform.rotate(ase_scaled, -90)
        else:
            print(f"Virhe: Asekuvaa ei löytynyt polusta: {ase_path}")
            self.ase_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.ase_image, (255, 0, 0), self.ase_image.get_rect())  # punainen neliö aseeksi

        # Lyöntitila
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 200  # ms

        # Suunta
        self.angle = 0  # Kulma, johon pelaaja katsoo

        # Aseen oletuspaikka pelaajan oikealla puolella
        self.weapon_offset_local = pygame.Vector2(-7, 15)

    def move(self, keys, walls):
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = PLAYER_SPEED

        old_rect = self.rect.copy()
        self.rect.x += dx
        if any(self.rect.colliderect(wall) for wall in walls): self.rect.x = old_rect.x
        self.rect.y += dy
        if any(self.rect.colliderect(wall) for wall in walls): self.rect.y = old_rect.y

    def update(self, dt):
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False

    def attack(self):
        self.is_attacking = True
        self.attack_timer = self.attack_duration

    def draw(self, screen, cam_x, cam_y, angle):
        self.angle = angle  # Päivitä kulma pelaajan katseeseen

        # Pelaajan keskipiste ruudulla
        center = pygame.Vector2(self.rect.centerx - cam_x, self.rect.centery - cam_y)

        # Aseen paikan laskeminen
        offset_rotated = self.weapon_offset_local.rotate(self.angle)

        attack_offset = pygame.Vector2(0, 0)
        if self.is_attacking:
            radians = math.radians(self.angle)
            attack_offset = pygame.Vector2(math.cos(radians), math.sin(radians)) * 55

        ase_pos = center + offset_rotated + attack_offset

        # Pyöritetään ase ja pelaajan kuva
        rotated_ase = pygame.transform.rotate(self.ase_image, -self.angle)
        rotated_hattu = pygame.transform.rotate(self.hattu_image, -self.angle)

        ase_rect = rotated_ase.get_rect(center=ase_pos)
        hattu_rect = rotated_hattu.get_rect(center=center)

        # --- Luo asepinta maskattavaksi ---
        ase_surface = pygame.Surface(rotated_ase.get_size(), pygame.SRCALPHA)
        ase_surface.blit(rotated_ase, (0, 0))
    
        # Luo maski
        mask = pygame.Surface(rotated_ase.get_size(), pygame.SRCALPHA)
        w, h = mask.get_size()
    
        # Laske maskin keskipiste niin että se vastaa pelaajan sijaintia aseen pinnalla
        # Ero pelaajan ja aseen sijainnin välillä
        ase_center_on_screen = pygame.Vector2(ase_rect.center)
        player_center_on_screen = center
        ase_to_player_offset = player_center_on_screen - ase_center_on_screen
    
        # Uusi maskikeskipiste
        mask_center = pygame.Vector2(w // 2, h // 2) + ase_to_player_offset
    
        # Piirrä maski (pelaajan etupuoli säilytetään näkyvänä)
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))
    
        pygame.draw.polygon(mask, (255, 255, 255, 255), [
            mask_center,
            mask_center + direction.rotate(-90) * 1000,
            mask_center + direction * 1000,
            mask_center + direction.rotate(90) * 1000,
        ])
    
        # Käytä maskia aseeseen
        ase_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
        # Piirrä ase
        screen.blit(ase_surface, ase_rect)
        screen.blit(rotated_hattu, hattu_rect)

        # --- Debug: hyökkäyksen alue näkyviin ---
        if self.is_attacking:
            debug_length = 100  # Kuinka pitkälle eteenpäin
            debug_width = 30   # Suorakulmion leveys

            # Lasketaan suunta ja ortonormaali (leveyssuunta)
            radians = math.radians(self.angle)
            direction = pygame.Vector2(math.cos(radians), math.sin(radians))
            perpendicular = pygame.Vector2(-direction.y, direction.x)  # 90 astetta

            # Suorakulmion kulmat
            p1 = center + direction * (PLAYER_SIZE / 2) + perpendicular * (debug_width / 2)
            p2 = center + direction * (PLAYER_SIZE / 2) - perpendicular * (debug_width / 2)
            p3 = p2 + direction * debug_length
            p4 = p1 + direction * debug_length

            # Piirrä läpinäkyvä punainen suorakulmio
            debug_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.polygon(debug_surface, (255, 0, 0, 100), [p1, p2, p3, p4])
            screen.blit(debug_surface, (0, 0))
