import os
import math
import pygame
import random
from MapGen import CELL_WIDTH, CELL_HEIGHT, TILE_SIZE
from raycast.raycaster import fieldOfVisionDegrees
from raycast.ray import Ray

class Vihollinen:
    def __init__(self, x, y, size=64, pixel_size=4):
        # Lataa ja skaalaa alkuperäinen sprite
        kuva_polku = os.path.join(os.path.dirname(__file__), "media", "Img", "zombie.PNG")
        original = pygame.image.load(kuva_polku).convert_alpha()
        original = pygame.transform.scale(original, (size, size))
        # Pixelöi sprite
        self.original_sprite = self.pixelate(original, pixel_size)
        self.rect = self.original_sprite.get_rect(center=(x, y))

        self.speed = 100
        self.angle = 0
        self.health_state = 2
        self.is_stunned = False
        self.stun_end_time = 0

        # Vihollisen ääni
        aanipolku = os.path.join(os.path.dirname(__file__), "media", "Vihollisten_aani.wav")
        if os.path.exists(aanipolku):
            self.vihujenaani = pygame.mixer.Sound(aanipolku)
            self.vihujenaani.set_volume(0.5)
        else:
            self.vihujenaani = None

    def pixelate(self, surface, pixel_size, blend_ratio=0.5):
        """Lievempi pixelöinti blend_ratio-arvolla (0-1)."""
        w, h = surface.get_size()
        small = pygame.transform.scale(surface, (max(1, w // pixel_size), max(1, h // pixel_size)))
        pixelated = pygame.transform.scale(small, (w, h))

        if 0 < blend_ratio < 1:
            result = surface.copy()
            pixelated.set_alpha(int(255 * blend_ratio))
            result.blit(pixelated, (0, 0))
            return result
        else:
            return pixelated

    def update(self, dt, player, matrix, game_map):
        # Stun-tila
        if self.is_stunned:
            if pygame.time.get_ticks() >= self.stun_end_time:
                self.is_stunned = False
            else:
                return

        # Apufunktio huone-ID:n hakemiseen
        def get_room_id_from_pos(pos):
            x, y = pos
            col = x // (CELL_WIDTH * TILE_SIZE)
            row = y // (CELL_HEIGHT * TILE_SIZE)
            if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
                return matrix[row][col]
            return -1

        enemy_room = get_room_id_from_pos(self.rect.center)
        player_room = get_room_id_from_pos(player.rect.center)

        # Tavoitteen valinta
        if (enemy_room == player_room
                or any(self.rect.colliderect(d.rect) for d in game_map.doors)):
            target = pygame.math.Vector2(player.rect.center)
        else:
            path = game_map.find_path_between_rooms(enemy_room, player_room)
            if len(path) >= 2:
                next_room = path[1]
                def door_connects(d, a, b):
                    room_d = get_room_id_from_pos(d.rect.center)
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        neigh = (d.rect.centerx + dx * TILE_SIZE,
                                 d.rect.centery + dy * TILE_SIZE)
                        if {room_d, get_room_id_from_pos(neigh)} == {a, b}:
                            return True
                    return False
                candidates = [d for d in game_map.doors if door_connects(d, enemy_room, next_room)]
                if candidates:
                    best = min(candidates, key=lambda d: pygame.Vector2(d.rect.center).distance_to(self.rect.center))
                    target = pygame.math.Vector2(best.rect.center)
                else:
                    target = pygame.math.Vector2(player.rect.center)
            else:
                target = pygame.math.Vector2(player.rect.center)

        # Liike ja kulma
        center = pygame.math.Vector2(self.rect.center)
        direction = target - center
        if direction.length() != 0:
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
            direction = direction.normalize()
        movement = direction * self.speed * (dt / 1000.0)

        # Esteet (seinät + pelaaja)
        walls = game_map.get_walls_in_radius(self.rect.centerx, self.rect.centery, 200)
        walls.append(player.rect)

        # Siirry
        self.rect.x += movement.x
        self.rect.y += movement.y

        # Törmäysten korjaus
        for wall in walls:
            if self.rect.colliderect(wall):
                overlap = self.rect.clip(wall)
                if overlap.width and overlap.height:
                    if overlap.width < overlap.height:
                        self.rect.x += -overlap.width if self.rect.centerx < wall.centerx else overlap.width
                    else:
                        self.rect.y += -overlap.height if self.rect.centery < wall.centery else overlap.height
                if wall is player.rect and not player.ishurting:
                    player.hurt(35)
                    if self.vihujenaani:
                        self.vihujenaani.play()

        # Avaa ovet, jos törmäät niihin
        for door in game_map.doors:
            if not door.is_open and self.rect.colliderect(door.rect):
                door.toggle(self.angle)

    def draw(self, surface, cam_x, cam_y, player_pos, player_angle, obstacles=None):
        player_angle = -player_angle
        vision = fieldOfVisionDegrees - 35

        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        angle_to = math.degrees(math.atan2(-dy, dx))
        if abs((angle_to - player_angle + 180) % 360 - 180) > vision:
            return
        if obstacles:
            start = pygame.Vector2(player_pos)
            end = pygame.Vector2(self.rect.center)
            dir_vec = (end - start).normalize()
            ray = Ray(start, math.atan2(dir_vec.y, dir_vec.x), start.distance_to(end))
            hits = ray.cast(obstacles)
            if hits and hits[-1].distance_to(end) > 10:
                return

        sprite = pygame.transform.rotate(self.original_sprite, self.angle)
        rect = sprite.get_rect(center=(self.rect.centerx - cam_x,
                                       self.rect.centery - cam_y))
        surface.blit(sprite, rect)

    def set_lighting(self, light_positions, obstacles):
        target = 0.0
        point = pygame.Vector2(self.rect.center)
        for lp in light_positions:
            ray = Ray(point, 0, point.distance_to(lp))
            val = ray.cast_to_light(lp, obstacles)
            if val is not None:
                target += val
        target = min(max(target * 3, 0), 1.0)
        if not hasattr(self, "light_intensity"):
            self.light_intensity = 1.0
        self.light_intensity += (target - self.light_intensity) * 0.1

    def take_damage(self):
        if self.is_stunned:
            return
        self.health_state -= 1
        self.is_stunned = True
        self.stun_end_time = pygame.time.get_ticks() + 1000
        if self.health_state <= 0:
            self.health_state = 0
