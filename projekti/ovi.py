import pygame

TILE_SIZE = 32
DOOR_WIDTH = 16
DOOR_HEIGHT = TILE_SIZE * 4

class Door:
    def __init__(self, x, y, orientation="vertical"):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.is_open = False
        self.angle = 0
        self.rect = self.create_rect()

    def create_rect(self):
        if self.orientation == "vertical":
            return pygame.Rect(self.x + (TILE_SIZE - DOOR_WIDTH) // 2, self.y - DOOR_HEIGHT // 2, DOOR_WIDTH, DOOR_HEIGHT) # y-akselin ovet
        else:
            return pygame.Rect(self.x - DOOR_HEIGHT // 2, self.y + (TILE_SIZE - DOOR_WIDTH) // 2, DOOR_HEIGHT, DOOR_WIDTH) # x-akselin ovet

    def toggle(self, _player_angle=None):
        self.is_open = not self.is_open

    def draw(self, screen, cam_x, cam_y):
        color = (25,25,25) if not self.is_open else (100, 180, 100)
        pygame.draw.rect(screen, color, self.rect.move(-cam_x, -cam_y))