import pygame
import math

class Player():
    #initti
    def __init__(self):
        super().__init__()
        self.position = pygame.Vector2(640, 360)
        self.sade = 20 
        self.speed = 8
    
    #vauhdin asetus
    def input(self, seinat):
        self.velocityX = 0
        self.velocityY = 0

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.velocityY = -self.speed
        if keys[pygame.K_s]:
            self.velocityY = self.speed
    
        if keys[pygame.K_a]:
            self.velocityX = -self.speed
        if keys[pygame.K_d]:
            self.velocityX = self.speed

        #estä sitä liikkumasta nopeampaa viistoon
        if self.velocityX != 0 and self.velocityY != 0:
            self.velocityX /= math.sqrt(2)
            self.velocityY /= math.sqrt(2)
        
        self.collision(self.position.x, self.position.y, seinat)

    #ei toimi kunnolla
    def collision(self, x, y, seinat):
        rect = pygame.Rect(x - self.sade, y - self.sade, self.sade * 2, self.sade * 2)
        for seina in seinat:
            if rect.colliderect(seina):
                self.position.x -= self.velocityX
                self.position.y -= self.velocityY

    #liikuta pelaajaa
    def move(self):
        self.position += pygame.Vector2(self.velocityX, self.velocityY)

    #kutsu tätä pää loopissa
    def update(self, seinat):
        self.input(seinat)
        self.move()