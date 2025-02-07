import pygame
import math

# Asetukset
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

pygame.init()

# Luo näyttö
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Seinät
walls = [
    ((100, 100), (700, 100)),
    ((700, 100), (700, 500)),
    ((700, 500), (100, 500)),
    ((100, 500), (100, 100)),
]

def cast_ray(start, angle):
    """ Heittää säteen annetusta pisteestä ja kulmasta. """
    x, y = start
    dx = math.cos(angle)
    dy = math.sin(angle)
    
    closest_hit = None
    min_dist = float('inf')
    
    for wall in walls:
        (x1, y1), (x2, y2) = wall
        
        # Ray-line intersection (parametric equations)
        den = (x1 - x2) * (y - (y + dy)) - (y1 - y2) * (x - (x + dx))
        if den == 0:
            continue
        
        t = ((x1 - x) * (y - (y + dy)) - (y1 - y) * (x - (x + dx))) / den
        u = -((x1 - x2) * (y1 - y) - (y1 - y2) * (x1 - x)) / den
        
        
        if 0 <= t <= 1 and u > 0:
            hit_x = x1 + t * (x2 - x1)
            hit_y = y1 + t * (y2 - y1)
            dist = math.sqrt((hit_x - x) ** 2 + (hit_y - y) ** 2)
            
            if dist < min_dist:
                min_dist = dist
                closest_hit = (hit_x, hit_y)
    
    return closest_hit

running = True
while running:
    screen.fill(BLACK)
    
    # Piirrä seinät
    for wall in walls:
        pygame.draw.line(screen, GRAY, wall[0], wall[1], 3)
    
    # Hae hiiren sijainti
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Heitä säteitä
    for angle in range(0, 360, 2):
        rad = math.radians(angle)
        hit = cast_ray((mouse_x, mouse_y), rad)
        if hit:
            pygame.draw.line(screen, WHITE, (mouse_x, mouse_y), hit, 1)
    
    # Tapahtumien käsittely
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
