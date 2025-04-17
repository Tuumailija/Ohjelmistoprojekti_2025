import os
import math
import pygame
import random
from MapGen import CELL_WIDTH, CELL_HEIGHT, TILE_SIZE
from raycast import raycaster
from raycast.raycaster import fieldOfVisionDegrees
from raycast.ray import Ray  # varmista että import toimii oikein

project_dir = os.path.dirname(os.path.abspath(__file__))

def get_room_id_from_pos(pos, matrix):
    x, y = pos
    col = x // (CELL_WIDTH * TILE_SIZE)
    row = y // (CELL_HEIGHT * TILE_SIZE)
    return matrix[row][col]

class Vihollinen:
    def __init__(self, x, y, size=64):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 100
        self.angle = 0

        self.health_state = 2
        self.is_stunned = False
        self.stun_end_time = 0

        self.light_intensity = 1.0  # 🔧 Alustetaan oletusarvo valaistukselle

        kuva_polku = os.path.join(project_dir, "media", "Img", "zombie.PNG")
        self.original_sprite = pygame.image.load(kuva_polku).convert_alpha()
        self.original_sprite = pygame.transform.scale(self.original_sprite, (size, size))
        self.sprite = self.original_sprite  # Alustetaan sprite

        # Vihollisten ääni
        vihujenaani_polku = os.path.join(project_dir, "media", "Vihollisten_aani.wav")
        if os.path.exists(vihujenaani_polku):
            self.vihujenaani = pygame.mixer.Sound(vihujenaani_polku)
            self.vihujenaani.set_volume(0.5)  # Säädetään äänenvoimakkuus
        else:
            print(f"Äänitiedostoa ei löydy: {vihujenaani_polku}")
            self.vihujenaani = None


    def update(self, dt, player, matrix, game_map):
        # Jos vielä stunnissa, odota
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

        enemy_room_id = get_room_id_from_pos(self.rect.center)
        player_room_id = get_room_id_from_pos(player.rect.center)

        # Määritä tavoite: suoraan pelaajaan, jos samassa huoneessa tai ovella
        if (enemy_room_id == player_room_id
                or any(self.rect.colliderect(door.rect) for door in game_map.doors)):
            target = pygame.math.Vector2(player.rect.center)
        else:
            path = game_map.find_path_between_rooms(enemy_room_id, player_room_id)
            if len(path) >= 2:
                next_room = path[1]

                def door_connects(door, a, b):
                    door_room = get_room_id_from_pos(door.rect.center)
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        neigh = (door.rect.centerx + dx * TILE_SIZE,
                                 door.rect.centery + dy * TILE_SIZE)
                        if {door_room, get_room_id_from_pos(neigh)} == {a, b}:
                            return True
                    return False

                doors_between = [
                    d for d in game_map.doors
                    if door_connects(d, enemy_room_id, next_room)
                ]
                if doors_between:
                    best = min(doors_between,
                               key=lambda d: pygame.Vector2(d.rect.center).distance_to(self.rect.center))
                    target = pygame.math.Vector2(best.rect.center)
                else:
                    target = pygame.math.Vector2(player.rect.center)
            else:
                target = pygame.math.Vector2(player.rect.center)

        # Laske liike ja kulma
        center = pygame.math.Vector2(self.rect.center)
        direction = target - center
        if direction.length() != 0:
            self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
            direction = direction.normalize()
        movement = direction * self.speed * (dt / 1000.0)

        # Kerää törmäysesteet (seinät + pelaaja)
        walls = game_map.get_walls_in_radius(self.rect.centerx, self.rect.centery, 200)
        walls.append(player.rect)

        # Siirry
        self.rect.x += movement.x
        self.rect.y += movement.y

        # Ratkaise törmäykset
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

        # Avaa ovet, jos niihin törmätään
        for door in game_map.doors:
            if not door.is_open and self.rect.colliderect(door.rect):
                door.toggle(self.angle)
                
    def draw(self, surface, cam_x, cam_y, player_pos, player_angle, obstacles=None):
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

        # Raycast: tarkistetaan esteet pelaajan ja vihollisen välillä
        if obstacles is not None:
            start = pygame.Vector2(player_pos)
            end = pygame.Vector2(self.rect.center)
            direction = (end - start).normalize()
            ray = Ray(start, math.atan2(direction.y, direction.x), start.distance_to(end))
            hit_points = ray.cast(obstacles)
            if hit_points and (hit_points[-1].distance_to(end) > 10):
                return  # Este välissä, ei piirretä
            
        # Piirretään vihollinen normaalisti kirkkaudella
        rotated_sprite = pygame.transform.rotate(self.original_sprite, self.angle)
        brightness = int(self.light_intensity * 255)

        # Kirkkauden säätö (sama kuin pelaajalla)
        def apply_brightness(surface, brightness):
            temp = surface.copy()
            darken = pygame.Surface(temp.get_size()).convert_alpha()
            darken.fill((brightness, brightness, brightness, 255))
            temp.blit(darken, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            return temp

        rotated_sprite = apply_brightness(rotated_sprite, brightness)
        sprite_rect = rotated_sprite.get_rect(center=(self.rect.centerx - cam_x, self.rect.centery - cam_y))
        surface.blit(rotated_sprite, sprite_rect)

    def set_lighting(self, light_positions, obstacles):
        target = 0.0
        point = pygame.Vector2(self.rect.center)
        for light_pos in light_positions:
            ray = Ray(point, 0, point.distance_to(light_pos))
            light_value = ray.cast_to_light(light_pos, obstacles)
            if light_value is not None:
                target += light_value
        target *= 3
        target = min(target, 1.0)
        target = max(target, 0)

        smoothing_speed = 0.1
        if not hasattr(self, "light_intensity"):
            self.light_intensity = 1.0
        self.light_intensity += (target - self.light_intensity) * smoothing_speed

    def take_damage(self):
        if self.is_stunned:
            return

        self.health_state -= 1
        self.is_stunned = True
        self.stun_end_time = pygame.time.get_ticks() + 1000  # 1 sekunti

        if self.health_state <= 0:
            self.health_state = 0  # Varmistetaan ettei mene negatiiviseksi
