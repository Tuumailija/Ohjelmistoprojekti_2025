import pygame
import os
import math

PLAYER_SIZE = 32
PLAYER_SPEED = 5

class Player:
    def __init__(self, start_x, start_y):
        self.rect = pygame.Rect(start_x, start_y, PLAYER_SIZE, PLAYER_SIZE)

        # Ladataan pelaajahahmon kuva (hattu)
        image_path = os.path.join("projekti", "media", "Img", "pelaaja.png")
        if os.path.exists(image_path):
            self.original_image = pygame.image.load(image_path).convert_alpha()
            
            # Skaalataan hattu isommaksi
            self.image = pygame.transform.scale(
                self.original_image,
                (int(PLAYER_SIZE * 2), int(PLAYER_SIZE * 2))
            )
        else:
            print(f"Virhe: Pelaajakuvaa ei löytynyt polusta: {image_path}")
            self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.image.fill((0, 150, 0))
        

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

    def draw(self, screen, cam_x, cam_y, angle):
        rotated_image = pygame.transform.rotate(self.image, -angle)  # negatiivinen koska pygame kiertää vastapäivään
        rotated_rect = rotated_image.get_rect(center=(self.rect.centerx - cam_x, self.rect.centery - cam_y))
        screen.blit(rotated_image, rotated_rect)
