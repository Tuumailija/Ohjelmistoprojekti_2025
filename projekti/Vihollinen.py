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
        # Tarkistetaan onko vihollinen edelleen stunnissa
        if self.is_stunned:
            if pygame.time.get_ticks() >= self.stun_end_time:
                self.is_stunned = False
            else:
                return  # Ei päivitetä liikettä tai törmäyksiä

        def get_room_id_from_pos(pos):
            x, y = pos
            col = x // (CELL_WIDTH * TILE_SIZE)
            row = y // (CELL_HEIGHT * TILE_SIZE)
            if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
                return matrix[row][col]
            return -1

        enemy_room_id = get_room_id_from_pos(self.rect.center)
        player_room_id = get_room_id_from_pos(player.rect.center)

        if enemy_room_id == player_room_id or any(self.rect.colliderect(door.rect) for door in game_map.doors):
            target = pygame.math.Vector2(player.rect.center)
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
                    target = pygame.math.Vector2(player.rect.center)
            else:
                target = pygame.math.Vector2(player.rect.center)

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
        walls.append(player.rect)

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
                
                #jos törmätty kohde on pelaaja
                if wall == player.rect:
                    #satuta pelaajaa jos iframet sallii
                    if not player.ishurting:
                        player.hurt(35)

                        if self.vihujenaani is not None:
                            self.vihujenaani.play()

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
        print(f"Vihollinen otti osuman! health_state = {self.health_state}")
        self.is_stunned = True
        self.stun_end_time = pygame.time.get_ticks() + 1000  # 1 sekunti

        if self.health_state <= 0:
            print("Vihollinen kuoli!")
            self.health_state = 0  # Varmistetaan ettei mene negatiiviseksi
