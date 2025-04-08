import pygame
import random
from MapGen import CELL_WIDTH, CELL_HEIGHT, TILE_SIZE

# Globaalit konfiguraatiokertoimet, joita käytetään matriisista laskemiseen
# Oletetaan, että nämä arvot ovat samaa arvoa kuin muissa moduuleissa:
# CELL_WIDTH, CELL_HEIGHT, TILE_SIZE

def get_room_id_from_pos(pos, matrix):
    x, y = pos
    col = x // (CELL_WIDTH * TILE_SIZE)
    row = y // (CELL_HEIGHT * TILE_SIZE)
    return matrix[row][col]

class Vihollinen:
    def __init__(self, x, y, size=24):  # pienempi koko
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 100

    def update(self, dt, player_rect, matrix, game_map):
        def get_room_id_from_pos(pos):
            x, y = pos
            col = x // (CELL_WIDTH * TILE_SIZE)
            row = y // (CELL_HEIGHT * TILE_SIZE)
            if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
                return matrix[row][col]
            return -1

        enemy_room_id = get_room_id_from_pos(self.rect.center)
        player_room_id = get_room_id_from_pos(player_rect.center)

        # Jos ollaan samassa huoneessa tai oviaukolla, seuraa pelaajaa suoraan
        if enemy_room_id == player_room_id or any(self.rect.colliderect(door.rect) for door in game_map.doors):
            target = pygame.math.Vector2(player_rect.center)
        else:
            # Muussa tapauksessa etsi lähin ovi vihollisen huoneesta kohti pelaajaa
            valid_doors = []
            for door in game_map.doors:
                door_room_id = get_room_id_from_pos(door.rect.center)
                if door_room_id == enemy_room_id:
                    valid_doors.append(door)

            if valid_doors:
                room_center_dict = game_map.get_room_center_dict()
                player_room_center = room_center_dict.get(player_room_id, player_rect.center)
                best_door = min(
                    valid_doors,
                    key=lambda d: pygame.math.Vector2(d.rect.center).distance_to(player_room_center)
                )
                target = pygame.math.Vector2(best_door.rect.center)
            else:
                target = pygame.math.Vector2(player_rect.center)

        # Liikkuminen kohti kohdetta
        enemy_center = pygame.math.Vector2(self.rect.center)
        direction = target - enemy_center
        if direction.length() != 0:
            direction = direction.normalize()
        movement = direction * self.speed * (dt / 1000.0)

        # Esteet (ovet eivät ole esteitä)
        all_walls = game_map.get_walls_in_radius(self.rect.centerx, self.rect.centery, 200)
        walls = all_walls  # Ovet ovat jo suodatettu pois build_global_tilemapissa, ei poisteta niitä uudelleen

        self.rect.x += movement.x
        if any(self.rect.colliderect(wall) for wall in walls):
            self.rect.x -= movement.x

        self.rect.y += movement.y
        if any(self.rect.colliderect(wall) for wall in walls):
            self.rect.y -= movement.y

    def draw(self, surface, cam_x, cam_y):
        # Piirretään vihollinen punaisena neliönä
        pygame.draw.rect(surface, (255, 0, 0),
                         pygame.Rect(self.rect.x - cam_x, self.rect.y - cam_y,
                                     self.rect.width, self.rect.height))
