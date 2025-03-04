import pygame
import math

class Ray:
    def __init__(self, pos, angle, ray_length):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.ray_length = ray_length  # Maksimipituus säteelle

    def cast(self, obstacles):
        closest = None
        min_dist = self.ray_length
        ray_start = self.pos
        ray_end = ray_start + self.dir * self.ray_length

        for rect in obstacles:
            hit_point = self.raycast_rect(ray_start, ray_end, rect)
            if hit_point:
                dist = ray_start.distance_to(hit_point)
                if dist < min_dist:
                    min_dist = dist
                    closest = hit_point

        return closest if closest else ray_end  # Pysäyttää säteen seinän kohdalle



    def raycast_rect(self, start, end, rect):
        """Laskee säteen ja suorakulmion osumat tarkasti"""
        clipped = rect.clipline(start, end)  # Pygame sisäänrakennettu törmäyksen tarkistus
    
        if clipped:
            hit_start = pygame.Vector2(clipped[0])
            hit_end = pygame.Vector2(clipped[1])
    
            if start.distance_to(hit_start) < start.distance_to(hit_end):
                return hit_start
            else:
                return hit_end
    
        return None



    def raycast_line(self, start, end, line_start, line_end):
        """Laskee törmäyspisteen viivan ja säteen välillä"""
        x1, y1 = line_start
        x2, y2 = line_end
        x3, y3 = start
        x4, y4 = end

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None  # Ei törmäystä (viivat ovat yhdensuuntaiset)

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if 0 <= t <= 1 and 0 <= u:
            return pygame.Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))

        return None  # Ei törmäystä
