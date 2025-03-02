import pygame

PLAYER_SIZE = 32
PLAYER_SPEED = 5
COLOR_PLAYER = (0, 150, 0)

class Player:
    def __init__(self, start_x, start_y):
        self.rect = pygame.Rect(start_x, start_y, PLAYER_SIZE, PLAYER_SIZE)

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

    def draw(self, screen, cam_x, cam_y):
        pygame.draw.rect(screen, COLOR_PLAYER, self.rect.move(-cam_x, -cam_y))
