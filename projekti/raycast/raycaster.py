from numpy import linspace
import pygame
import math
from .ray import Ray

rayNumber = (360//16)
fieldOfVisionDegrees = 360/4
fieldOfVision = linspace(0, fieldOfVisionDegrees, rayNumber)

class RayCaster:
    def __init__(self, screen, ray_length):
        self.screen = screen
        self.rays = []
        self.ray_length = ray_length  # Maksimipituus säteille
        self.obstacles = []  # Lista esteille
        self.valot = []
        self.cam_x = 0
        self.cam_y = 0

    def set_obstacles(self, obstacles):
        self.obstacles = [pygame.Rect(wall.x - self.cam_x, wall.y - self.cam_y, wall.width, wall.height) for wall in obstacles]

    def set_valot(self, valo_pos):
        self.valot = [(x - self.cam_x, y - self.cam_y) for x, y in valo_pos]

    def set_cam(self, x, y):
        self.cam_x = x
        self.cam_y = y

    def update_rays(self, pos, angle):
        """Luo säteet pelaajan sijainnista. Jokaisella säteellä on oma vaihe."""
        self.rays = [
            Ray(pos, math.radians(a + angle - 45), self.ray_length, i)
            for i, a in enumerate(fieldOfVision)
        ]


    def cast_rays(self):
        """Laskee säteiden loppupisteet ottaen huomioon suorakulmioesteet."""
        return [ray.cast(self.obstacles) for ray in self.rays]

    def draw(self, pos):
        """Piirtää säteet alkaen pelaajan sijainnista."""
        ray_points = self.cast_rays()
        for points in ray_points:
            pygame.draw.circle(self.screen, (255, 0, 255), points[-1], 10)
            for point in points:
                arvo = 0.0
                if self.valot:
                    for light_pos in self.valot:
                        light_hit = Ray(point, 0, point.distance_to(light_pos)).cast_to_light(light_pos, self.obstacles)
                        if light_hit is not None:
                            arvo += light_hit
                            if arvo >= 1:
                                arvo = 1
                        #if light_hit == light_pos:
                        #    pygame.draw.line(self.screen, (255, 255, 255), point, light_hit, 1)
                        #if light_hit is not None:
                        #    pygame.draw.line(self.screen, (255, 255, 255), point, light_hit, 1)
                #print(arvo)
                

                keys = pygame.key.get_pressed()
                if keys[pygame.K_TAB]:
                        font = pygame.font.SysFont(None, 12)
                        text = font.render(f'{arvo:.4f}', True, (255, 255, 0))
                        self.screen.blit(text, (point[0], point[1]))
                else:
                    color = (255, 255, 0, int(arvo * 128))  # Reduce alpha value for more transparency
                    s = pygame.Surface((arvo*100, arvo*100), pygame.SRCALPHA)  # Create a surface with alpha channel
                    pygame.draw.circle(s, color, (arvo*50, arvo*50), arvo*50)
                    self.screen.blit(s, (point[0] - arvo*50, point[1] - arvo*50))

                #pygame.draw.line(self.screen, (255, 255, 255), pos, point, 1)

    def draw_falloff_circle(surface, center, max_radius, brightness):
        for r in range(max_radius, 0, -1):
            falloff = r / max_radius  # 1.0 (reuna) → 0.0 (keskusta)
            alpha = int((1 - falloff**2) * brightness)
            if alpha <= 0:
                continue  # Ei piirretä näkymätöntä kerrosta
            color = (brightness, brightness, brightness, alpha)
            pygame.draw.circle(surface, color, center, r)

    def get_light_mask(self):
        width, height = self.screen.get_size()
        mask = pygame.Surface((width, height), pygame.SRCALPHA)

        for points in self.cast_rays():
            for point in points:
                arvo = 0.0
                for light_pos in self.valot:
                    light_hit = Ray(point, 0, point.distance_to(light_pos)).cast_to_light(light_pos, self.obstacles)
                    if light_hit is not None:
                        arvo += light_hit
                arvo = min(arvo, 1.0)

                if arvo > 0:
                    radius = 35
                    brightness = int(arvo * 255)
                    if brightness < 8:
                        continue  # jätetään hyvin himmeät pois
                    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    RayCaster.draw_falloff_circle(s, (radius, radius), radius, brightness)
                    mask.blit(s, (point[0] - radius, point[1] - radius))  # ilman blend-moodia

        return mask
