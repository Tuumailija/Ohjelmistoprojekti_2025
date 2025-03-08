import pygame
import math

sadeSteps = 25*2

class Ray:
    def __init__(self, pos, angle, ray_length):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.ray_length = ray_length  # Maksimipituus säteelle

    def cast(self, obstacles):
        #omat Rect arvot ei käy, jos muuttaa resoluutiota !!!!!!!
        #self.screen.get_width() | self.screen.get_height()
        esteet = obstacles.copy()
        esteet.append(pygame.Rect(0, 0, 1920, 108))
        esteet.append(pygame.Rect(0, 970, 1920, 100))
        closest = None
        min_dist = self.ray_length
        ray_start = self.pos
        ray_end = ray_start + self.dir * self.ray_length

        hit_points = []  # Lista osumapisteille

        for rect in esteet:
            hit_point = self.raycast_rect(ray_start, ray_end, rect)
            if hit_point:
                dist = ray_start.distance_to(hit_point)
                if dist < min_dist:
                    min_dist = dist
                    closest = hit_point
                    hit_points = self.jaa_sade_osiin_absoluuttisesti(ray_start, closest, sadeSteps)
                    hit_points.append(closest)  # Lisätään törmäyspiste

        if closest:
            return hit_points  # Palautetaan osumapisteet
        else:
            hit_points = self.jaa_sade_osiin_absoluuttisesti(ray_start, ray_end, sadeSteps)
            hit_points.append(ray_end)  # Lisätään lopetuspiste
            return hit_points

    def jaa_sade_osiin_absoluuttisesti(self, start, end, vali):
        """Jakaa säteen osiin absoluuttisilla väleillä."""
        pisteet = []
        nykyinen_piste = start
        kokonais_matka = start.distance_to(end)
        kuljettu_matka = 0

        while kuljettu_matka < kokonais_matka:
            pisteet.append(nykyinen_piste)
            kuljettu_matka += vali
            if kuljettu_matka > kokonais_matka:
                nykyinen_piste = end
            else:
                suunta = (end - start).normalize()
                nykyinen_piste = start + suunta * kuljettu_matka

        return pisteet

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
    
    def cast_to_light(self, light_pos, obstacles):
        """Lähettää säteen valopisteeseen ja palauttaa törmäyspisteen tai valopisteen."""
        ray_start = self.pos
        ray_end = pygame.Vector2(light_pos)

        vali = ray_start.distance_to(ray_end)

        for rect in obstacles:
            hit_point = self.raycast_rect(ray_start, ray_end, rect)
            if hit_point:
                return None
            
        arvo = 1 / (vali/200)**2
        return arvo
    
    
    #def cast_to_light(self, light_pos, obstacles):
    #    """Lähettää säteen valopisteeseen ja palauttaa törmäyspisteen tai valopisteen."""
    #    ray_start = self.pos
    #    ray_end = pygame.Vector2(light_pos)
#
    #    vali = ray_start.distance_to(ray_end)
#
    #    for rect in obstacles:
    #        hit_point = self.raycast_rect(ray_start, ray_end, rect)
    #        if hit_point:
    #            return None
    #        
    #    return ray_end