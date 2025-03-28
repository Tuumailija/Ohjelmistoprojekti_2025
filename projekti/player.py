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

        center = pygame.Vector2(self.rect.centerx - cam_x, self.rect.centery - cam_y)

        # Lyöntiliike: liikuta asetta hieman eteenpäin katseen suuntaan
        forward_offset = pygame.Vector2(0, 0)
        if self.is_attacking:
            radians = math.radians(self.angle)
            forward_offset = pygame.Vector2(math.cos(radians), math.sin(radians)) * 25  # 25px eteenpäin

        ase_pos = center + forward_offset

        # Pyöritetään kuvat kulman mukaan
        rotated_ase = pygame.transform.rotate(self.ase_image, -self.angle)
        rotated_hattu = pygame.transform.rotate(self.hattu_image, -self.angle)

        ase_rect = rotated_ase.get_rect(center=ase_pos)
        hattu_rect = rotated_hattu.get_rect(center=center)

        screen.blit(rotated_ase, ase_rect)
        screen.blit(rotated_hattu, hattu_rect)
