import pygame
import math

sadeSteps = 25 * 2

class Ray:
    def __init__(self, pos, angle, ray_length, index=0):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.ray_length = ray_length
        self.index = index  # säteen indeksi (käytetään vaiheensiirtoon)

    def cast(self, obstacles):
        esteet = obstacles.copy()
        esteet.append(pygame.Rect(0, 0, 1920, 108))
        esteet.append(pygame.Rect(0, 970, 1920, 100))

        closest = None
        min_dist = self.ray_length
        ray_start = self.pos
        ray_end = ray_start + self.dir * self.ray_length

        # Lasketaan mahdollinen vaiheensiirto
        offset = sadeSteps // 2 if self.index % 2 == 1 else 0

        hit_points = []

        for rect in esteet:
            hit_point = self.raycast_rect(ray_start, ray_end, rect)
            if hit_point:
                dist = ray_start.distance_to(hit_point)
                if dist < min_dist:
                    min_dist = dist
                    dist -= 5
                    closest = ray_start + self.dir * dist
                    hit_points = self.jaa_sade_osiin_absoluuttisesti(ray_start, closest, sadeSteps, offset)
                    hit_points.append(closest)

        if closest:
            return hit_points
        else:
            hit_points = self.jaa_sade_osiin_absoluuttisesti(ray_start, ray_end, sadeSteps, offset)
            hit_points.append(ray_end)
            return hit_points

    def jaa_sade_osiin_absoluuttisesti(self, start, end, vali, offset=0):
        """Jakaa säteen osiin absoluuttisilla väleillä, aloitusvaiheella."""
        pisteet = []
        kokonais_matka = start.distance_to(end)
        kuljettu_matka = vali + offset

        while kuljettu_matka < kokonais_matka:
            suunta = (end - start).normalize()
            nykyinen_piste = start + suunta * kuljettu_matka
            pisteet.append(nykyinen_piste)
            kuljettu_matka += vali

        return pisteet

    def raycast_rect(self, start, end, rect):
        clipped = rect.clipline(start, end)
        if clipped:
            hit_start = pygame.Vector2(clipped[0])
            hit_end = pygame.Vector2(clipped[1])
            return hit_start if start.distance_to(hit_start) < start.distance_to(hit_end) else hit_end
        return None

    def cast_to_light(self, light_pos, obstacles):
        ray_start = self.pos
        ray_end = pygame.Vector2(light_pos)
        vali = ray_start.distance_to(ray_end)

        for rect in obstacles:
            if self.raycast_rect(ray_start, ray_end, rect):
                return None

        return 1 / (vali / 200)**2 if vali != 0 else 1.0
