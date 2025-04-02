import pygame
import os
import random

class Vihollinen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.leveys = 40
        self.pituus = 40
        
        base_dir = os.path.dirname(__file__)
        sprite_path = os.path.join(base_dir, "projekti", "media", "Img", "Vihollinen_testi.png")
        
        if os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            # Skaalataan sprite vastaamaan vihollisen kokoa
            self.sprite = pygame.transform.scale(self.sprite, (self.leveys, self.pituus))
        else:
            print(f"Spriteä ei löytynyt polusta: {sprite_path}. Käytetään varaväriä.")
            self.sprite = None
            self.vari = (255, 255, 255)  # Vihollinen on valkoinen varavärinä jos spriteä ei löydy

        self.rect = pygame.Rect(self.x, self.y, self.leveys, self.pituus)
        
        # Aseta viholliselle liikkumisnopeus ja satunnainen alkuperäinen liikesuunta
        self.speed = 2  # Vihollisen vauhti
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
        self.frame_counter = 0
        self.change_direction_time = random.randint(30, 120)  # satunnaisia ruudun päivityksiä ennen suunnan vaihtoa

    def update(self, walls, enemies, player):
        """Päivittää vihollisen sijainnin ja tarkistaa törmäykset.
           Jos vihollinen törmää seinään, toiseen viholliseen tai pelaajaan, liike peruutetaan
           ja suunnaksi asetetaan uusi satunnainen vektori."""
        self.frame_counter += 1
        if self.frame_counter >= self.change_direction_time:
            # Vaihdetaan satunnainen suunta
            self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
            self.frame_counter = 0
            self.change_direction_time = random.randint(30, 120)
        
        # Tallennetaan vanha sijainti törmäyksen varalta
        old_rect = self.rect.copy()
        # Liikutetaan vihollista nykyisen suunnan mukaisesti
        self.rect.x += int(self.direction.x * self.speed)
        self.rect.y += int(self.direction.y * self.speed)
        
        # Tarkistetaan törmäykset seinien kanssa
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = old_rect  # Palautetaan edellinen sijainti
                self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
                return

        # Tarkistetaan törmäykset muiden vihollisten kanssa
        for enemy in enemies:
            if enemy is not self and self.rect.colliderect(enemy.rect):
                self.rect = old_rect
                self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
                return

        # Tarkistetaan törmäys pelaajaan
        if self.rect.colliderect(player.rect):
            self.rect = old_rect
            self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
            # Tässä voidaan lisätä logiikkaa, esim. pelaajan vahingoittaminen
            return

    def piirra(self, screen, cam_x, cam_y):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x - cam_x, self.rect.y - cam_y))
        else:
            # Jos spriteä ei ole, piirretään pelkkä suorakulmio
            pygame.draw.rect(screen, self.vari, pygame.Rect(self.rect.x - cam_x, self.rect.y - cam_y, self.leveys, self.pituus))
