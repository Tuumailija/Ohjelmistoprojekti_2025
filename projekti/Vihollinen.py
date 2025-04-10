import os
import math
import pygame
import random
from MapGen import CELL_WIDTH, CELL_HEIGHT, TILE_SIZE
from raycast import raycaster
from raycast.raycaster import fieldOfVisionDegrees

project_dir = os.path.dirname(os.path.abspath(__file__))

def get_room_id_from_pos(pos, matrix):
    x, y = pos
    col = x // (CELL_WIDTH * TILE_SIZE)
    row = y // (CELL_HEIGHT * TILE_SIZE)
    return matrix[row][col]

class Vihollinen:
    def __init__(self, x, y, size=64):  # isompi koko
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 100
        self.angle = 0  # suunta-arvo spriteä varten

        kuva_polku = os.path.join(project_dir, "media", "Img", "zombie.PNG")
        self.original_sprite = pygame.image.load(kuva_polku).convert_alpha()
        self.original_sprite = pygame.transform.scale(self.original_sprite, (size, size))
        self.sprite = self.original_sprite  # Alustetaan sprite

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

        if enemy_room_id == player_room_id or any(self.rect.colliderect(door.rect) for door in game_map.doors):
            target = pygame.math.Vector2(player_rect.center)
        else:
            path = game_map.find_path_between_rooms(enemy_room_id, player_room_id)
            if len(path) >= 2:
                next_room_id = path[1]

                def door_connects(door, room_a, room_b):
                    door_room = get_room_id_from_pos(door.rect.center)
                    for dx in [-1, 1, 0, 0]:
                        for dy in [-1, 1, 0, 0]:
                            neighbor_pos = (door.rect.centerx + dx * TILE_SIZE, door.rect.centery + dy * TILE_SIZE)
                            neighbor_room = get_room_id_from_pos(neighbor_pos)
                            if {door_room, neighbor_room} == {room_a, room_b}:
                                return True
                    return False

                possible_doors = [
                    door for door in game_map.doors
                    if door_connects(door, enemy_room_id, next_room_id)
                ]

                if possible_doors:
                    best_door = min(
                        possible_doors,
                        key=lambda d: pygame.math.Vector2(d.rect.center).distance_to(self.rect.center)
                    )
                    target = pygame.math.Vector2(best_door.rect.center)
                else:
                    target = pygame.math.Vector2(player_rect.center)
            else:
                target = pygame.math.Vector2(player_rect.center)

        # Liikkuminen ja suunta päivittyy samalla
        enemy_center = pygame.math.Vector2(self.rect.center)
        direction = target - enemy_center
        if direction.length() != 0:
            # Korjaa kulmaa: tässä oletetaan, että alkuperäinen sprite katsoo ylös.
            # Jos sprite katsoo eri suuntaan, säädä kulmakorjausta (tässä -90 astetta).
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
            direction = direction.normalize()
        movement = direction * self.speed * (dt / 1000.0)

        # Haetaan törmäysesteet: huoneen seinät ja pelaaja.
        walls = game_map.get_walls_in_radius(self.rect.centerx, self.rect.centery, 200)
        walls.append(player_rect)

        # Liikutetaan vihollista ensin kokonaisliikkeellä
        self.rect.x += movement.x
        self.rect.y += movement.y

        # Tarkistetaan törmäykset ja korjataan ne "nudgeamalla" ulos
        for wall in walls:
            if self.rect.colliderect(wall):
                # Lasketaan päällekkäisyys
                overlap = self.rect.clip(wall)
                if overlap.width == 0 or overlap.height == 0:
                    continue  # Ei päällekkäisyyttä

                # Korjataan pienimmän korjaussuunta-arvon mukaisesti
                if overlap.width < overlap.height:
                    # Pienempi korjaus vaakasuunnassa
                    if self.rect.centerx < wall.centerx:
                        self.rect.x -= overlap.width
                    else:
                        self.rect.x += overlap.width
                else:
                    # Pienempi korjaus pystysuunnassa
                    if self.rect.centery < wall.centery:
                        self.rect.y -= overlap.height
                    else:
                        self.rect.y += overlap.height

    def draw(self, surface, cam_x, cam_y, player_pos, player_angle):
        player_angle *= -1
        visionField = fieldOfVisionDegrees - 35

        # Lasketaan kulma pelaajasta viholliseen
        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        angle_to_enemy = math.degrees(math.atan2(-dy, dx))

        # Kulmaero pelaajan katsesuunnan ja vihollisen suunnan välillä
        angle_diff = abs((angle_to_enemy - player_angle + 180) % 360 - 180)

        # Jos vihollinen on pelaajan näkökentän ulkopuolella, ei piirretä
        if angle_diff > visionField:
            return

        # Piirretään vihollinen normaalisti
        rotated_sprite = pygame.transform.rotate(self.original_sprite, self.angle)
        sprite_rect = rotated_sprite.get_rect(center=(self.rect.centerx - cam_x, self.rect.centery - cam_y))
        surface.blit(rotated_sprite, sprite_rect)

        # DEBUG (viivat näytölle)
        screen_center_x = surface.get_width() // 2
        screen_center_y = surface.get_height() // 2

        ## Viholliseen osoittava viiva (punainen)
        #enemy_line_x = screen_center_x + 100 * math.cos(math.radians(angle_to_enemy))
        #enemy_line_y = screen_center_y - 100 * math.sin(math.radians(angle_to_enemy))
        #pygame.draw.line(surface, (255, 0, 0), (screen_center_x, screen_center_y), (enemy_line_x, enemy_line_y), 2)
#
        ## Pelaajan katsesuunta (vihreä)
        #player_line_x = screen_center_x + 100 * math.cos(math.radians(player_angle))
        #player_line_y = screen_center_y - 100 * math.sin(math.radians(player_angle))
        #pygame.draw.line(surface, (0, 255, 0), (screen_center_x, screen_center_y), (player_line_x, player_line_y), 2)
