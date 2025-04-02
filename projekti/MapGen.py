import pygame
import os
import random
from ovi import Door

# Konfigurointikonstantit
ROOM_WIDTH = 20   
ROOM_HEIGHT = 16   
CELL_WIDTH = ROOM_WIDTH + 1  
CELL_HEIGHT = ROOM_HEIGHT + 1  
TILE_SIZE = 32
FLOOR, WALL, DOOR = 0, 1, 2
COLOR_FLOOR, COLOR_WALL, COLOR_DOOR = (105, 105, 105), (25, 25, 25), (100, 50, 0)

class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.doors = []
        self.tilemap = self.build_global_tilemap()
        self.wall_rects = self.get_wall_rects()
        self.map_width_px = len(self.tilemap[0]) * TILE_SIZE
        self.map_height_px = len(self.tilemap) * TILE_SIZE
        self.room_balls = self.generate_room_balls()
        self.win_tile = self.get_win_tile()
        self.debug_tile = self.get_debug_tile()

    def build_global_tilemap(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        map_width = cols * CELL_WIDTH + 1  
        map_height = rows * CELL_HEIGHT + 1
        tilemap = [[WALL for _ in range(map_width)] for _ in range(map_height)]

        for r in range(rows):
            for c in range(cols):
                origin_x, origin_y = c * CELL_WIDTH, r * CELL_HEIGHT
                if self.matrix[r][c] != 0:
                    for y in range(origin_y + 1, origin_y + 1 + ROOM_HEIGHT):
                        for x in range(origin_x + 1, origin_x + 1 + ROOM_WIDTH):
                            tilemap[y][x] = FLOOR

        # Lisätään vasen reuna seinä kaikille vasemman laidan huoneille
        for r in range(rows):
            if self.matrix[r][0] != 0:  # vasemman laidan huone
                origin_x, origin_y = 0, r * CELL_HEIGHT
                for y in range(origin_y + 1, origin_y + 1 + ROOM_HEIGHT):
                    tilemap[y][origin_x] = WALL  # vasen reunaseinä

        self.create_doors(tilemap, rows, cols)
        self.merge_rooms(tilemap, rows, cols)
        return tilemap

    def create_doors(self, tilemap, rows, cols):
        room_sizes = {}
        for r in range(rows):
            for c in range(cols):
                room_id = self.matrix[r][c]
                if room_id:
                    room_sizes[room_id] = room_sizes.get(room_id, 0) + 1

        room_max_doors = {room_id: (3 if size == 1 else 5) for room_id, size in room_sizes.items()}
        room_door_count = {room_id: 0 for room_id in room_sizes}

        for r in range(rows):
            for c in range(cols):
                origin_x, origin_y = c * CELL_WIDTH, r * CELL_HEIGHT
                if self.matrix[r][c] != 0:
                    room_a = self.matrix[r][c]

                    if c < cols - 1 and self.matrix[r][c + 1] != 0:
                        room_b = self.matrix[r][c + 1]
                        if room_b != room_a and room_door_count[room_a] < room_max_doors[room_a] and \
                        room_door_count[room_b] < room_max_doors[room_b]:
                            door_x = origin_x + ROOM_WIDTH + 1
                            door_y = origin_y + 1 + ROOM_HEIGHT // 2
                            tilemap[door_y - 1][door_x] = DOOR
                            tilemap[door_y][door_x] = DOOR
                            tilemap[door_y + 1][door_x] = DOOR
                            room_door_count[room_a] += 1
                            room_door_count[room_b] += 1
                            self.doors.append(Door(door_x * TILE_SIZE, door_y * TILE_SIZE, "vertical"))

                    if r < rows - 1 and self.matrix[r + 1][c] != 0:
                        room_b = self.matrix[r + 1][c]
                        if room_b != room_a and room_door_count[room_a] < room_max_doors[room_a] and \
                        room_door_count[room_b] < room_max_doors[room_b]:
                            door_x = origin_x + 1 + ROOM_WIDTH // 2
                            door_y = origin_y + ROOM_HEIGHT + 1
                            tilemap[door_y][door_x - 1] = DOOR
                            tilemap[door_y][door_x] = DOOR
                            tilemap[door_y][door_x + 1] = DOOR
                            room_door_count[room_a] += 1
                            room_door_count[room_b] += 1
                            self.doors.append(Door(door_x * TILE_SIZE, door_y * TILE_SIZE, "horizontal"))

    def merge_rooms(self, tilemap, rows, cols):
        for r in range(rows):
            for c in range(cols - 1):
                if self.matrix[r][c] != 0 and self.matrix[r][c + 1] == self.matrix[r][c]:
                    wall_x = (c + 1) * CELL_WIDTH
                    for y in range(r * CELL_HEIGHT + 1, r * CELL_HEIGHT + 1 + ROOM_HEIGHT):
                        tilemap[y][wall_x] = FLOOR

        for r in range(rows - 1):
            for c in range(cols):
                if self.matrix[r][c] != 0 and self.matrix[r + 1][c] == self.matrix[r][c]:
                    wall_y = (r + 1) * CELL_HEIGHT
                    for x in range(c * CELL_WIDTH + 1, c * CELL_WIDTH + 1 + ROOM_WIDTH):
                        tilemap[wall_y][x] = FLOOR

    def get_wall_rects(self):
        visited = set()
        wall_rects = []

        # Manuaalinen vasen seinä lisäys testiksi
        wall_rects.append(pygame.Rect(0, TILE_SIZE, TILE_SIZE, ROOM_HEIGHT * TILE_SIZE))

        for y in range(len(self.tilemap)):
            for x in range(len(self.tilemap[y])):
                if self.tilemap[y][x] == WALL and (x, y) not in visited:
                    width, height = 1, 1
                    while x + width < len(self.tilemap[y]) and self.tilemap[y][x + width] == WALL:
                        visited.add((x + width, y))
                        width += 1
                    while y + height < len(self.tilemap) and all(self.tilemap[y + height][x + i] == WALL for i in range(width)):
                        for i in range(width):
                            visited.add((x + i, y + height))
                        height += 1
                    wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, width * TILE_SIZE, height * TILE_SIZE))
                    visited.update((x + i, y + j) for i in range(width) for j in range(height))
        return wall_rects

    def generate_room_balls(self):
        room_cells = {}
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[r])):
                room_id = self.matrix[r][c]
                if room_id != 0:
                    room_cells.setdefault(room_id, []).append((r, c))

        balls = []
        ball_offset = 10
        for room_id, cells in room_cells.items():
            min_r = min(r for r, c in cells)
            max_r = max(r for r, c in cells)
            min_c = min(c for r, c in cells)
            max_c = max(c for r, c in cells)

            room_left_tile = min_c * CELL_WIDTH + 1
            room_right_tile = max_c * CELL_WIDTH + 1 + ROOM_WIDTH
            room_top_tile = min_r * CELL_HEIGHT + 1
            room_bottom_tile = max_r * CELL_HEIGHT + 1 + ROOM_HEIGHT

            room_left = room_left_tile * TILE_SIZE
            room_right = room_right_tile * TILE_SIZE
            room_top = room_top_tile * TILE_SIZE
            room_bottom = room_bottom_tile * TILE_SIZE

            wall = random.choice(['left', 'right', 'top', 'bottom'])
            if wall == 'left':
                x = room_left + ball_offset
                y = random.randint(room_top, room_bottom)
            elif wall == 'right':
                x = room_right - ball_offset
                y = random.randint(room_top, room_bottom)
            elif wall == 'top':
                x = random.randint(room_left, room_right)
                y = room_top + ball_offset
            elif wall == 'bottom':
                x = random.randint(room_left, room_right)
                y = room_bottom - ball_offset
            balls.append((x, y))
        return balls
    
    def get_win_tile(self):
        last_room_id = max(r for row in self.matrix for r in row)
        cells = [(r, c) for r in range(len(self.matrix)) for c in range(len(self.matrix[0])) if self.matrix[r][c] == last_room_id]
        min_r = min(r for r, c in cells)
        max_r = max(r for r, c in cells)
        min_c = min(c for r, c in cells)
        max_c = max(c for r, c in cells)
        center_x = ((min_c + max_c + 1) / 2) * CELL_WIDTH * TILE_SIZE
        center_y = ((min_r + max_r + 1) / 2) * CELL_HEIGHT * TILE_SIZE
        size = TILE_SIZE
        return pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)
    
    def get_debug_tile(self):  # DEBUG (voi poistaa myöhemmin)
        room_ids = sorted(set(r for row in self.matrix for r in row if r != 0))  # DEBUG
        if len(room_ids) < 2:  # DEBUG
            return pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)  # DEBUG
        debug_id = room_ids[1]  # DEBUG
        cells = [(r, c) for r in range(len(self.matrix)) for c in range(len(self.matrix[0])) if self.matrix[r][c] == debug_id]  # DEBUG
        min_r = min(r for r, c in cells)  # DEBUG
        max_r = max(r for r, c in cells)  # DEBUG
        min_c = min(c for r, c in cells)  # DEBUG
        max_c = max(c for r, c in cells)  # DEBUG
        center_x = ((min_c + max_c + 1) / 2) * CELL_WIDTH * TILE_SIZE  # DEBUG
        center_y = ((min_r + max_r + 1) / 2) * CELL_HEIGHT * TILE_SIZE  # DEBUG
        size = TILE_SIZE  # DEBUG
        return pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)  # DEBUG

    def draw(self, screen, cam_x, cam_y):
        for wall in self.wall_rects:
            pygame.draw.rect(screen, COLOR_WALL, 
                             pygame.Rect(wall.x - cam_x, wall.y - cam_y, wall.width, wall.height))

        for ball_pos in self.room_balls:
            pygame.draw.circle(screen, (255, 255, 0),
                               (int(ball_pos[0] - cam_x), int(ball_pos[1] - cam_y)), 8)

        for door in self.doors:
            door.draw(screen, cam_x, cam_y)

    def get_walls_in_radius(self, x, y, radius):
        walls = []
        center = pygame.Vector2(x, y)
        for wall in self.wall_rects:
            wall_rect = pygame.Rect(wall.x, wall.y, wall.width, wall.height)
            if wall_rect.collidepoint(center) or wall_rect.inflate(radius * 2, radius * 2).collidepoint(center):
                walls.append(wall)
        return walls

    def get_lights_in_radius(self, x, y, radius):
        balls = []
        center = pygame.Vector2(x, y)
        for ball_pos in self.room_balls:
            ball_center = pygame.Vector2(ball_pos[0], ball_pos[1])
            if center.distance_to(ball_center) <= radius:
                balls.append(ball_pos)
        return balls
