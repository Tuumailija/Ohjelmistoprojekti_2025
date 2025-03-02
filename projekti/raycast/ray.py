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
            if not isinstance(rect, pygame.Rect):
                continue

            hit_point = self.raycast_rect(ray_start, ray_end, rect)
            if hit_point:
                dist = ray_start.distance_to(hit_point)
                if dist < min_dist:
                    min_dist = dist
                    closest = hit_point

        return closest if closest else ray_end

    def raycast_rect(self, start, end, rect):
        """Laskee törmäyksen säteen ja suorakulmion välillä"""
        edges = [
            ((rect.left, rect.top), (rect.right, rect.top)),  # Yläreuna
            ((rect.right, rect.top), (rect.right, rect.bottom)),  # Oikea reuna
            ((rect.right, rect.bottom), (rect.left, rect.bottom)),  # Alareuna
            ((rect.left, rect.bottom), (rect.left, rect.top)),  # Vasen reuna
        ]

        closest_hit = None
        min_dist = float("inf")

        for edge in edges:
            hit = self.raycast_line(start, end, edge[0], edge[1])
            if hit:
                dist = start.distance_to(hit)
                if dist < min_dist:
                    min_dist = dist
                    closest_hit = hit

        return closest_hit

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
