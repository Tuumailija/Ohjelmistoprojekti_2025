import pygame

# Constants
ROOM_WIDTH = 10    
ROOM_HEIGHT = 8    
CELL_WIDTH = ROOM_WIDTH + 1  
CELL_HEIGHT = ROOM_HEIGHT + 1  
TILE_SIZE = 64
FLOOR, WALL, DOOR = 0, 1, 2
COLOR_FLOOR, COLOR_WALL, COLOR_DOOR = (105, 105, 105), (25, 25, 25), (100, 50, 0)

class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.tilemap = self.build_global_tilemap()
        self.wall_rects = self.get_wall_rects()
        self.map_width_px = len(self.tilemap[0]) * TILE_SIZE
        self.map_height_px = len(self.tilemap) * TILE_SIZE

    def build_global_tilemap(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        map_width = cols * CELL_WIDTH + 1  
        map_height = rows * CELL_HEIGHT + 1
        tilemap = [[WALL for _ in range(map_width)] for _ in range(map_height)]
        
        # Carve out room interiors
        for r in range(rows):
            for c in range(cols):
                origin_x, origin_y = c * CELL_WIDTH, r * CELL_HEIGHT
                if self.matrix[r][c] != 0:
                    for y in range(origin_y + 1, origin_y + 1 + ROOM_HEIGHT):
                        for x in range(origin_x + 1, origin_x + 1 + ROOM_WIDTH):
                            tilemap[y][x] = FLOOR
        
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
                        if room_b != room_a and room_door_count[room_a] < room_max_doors[room_a] and room_door_count[room_b] < room_max_doors[room_b]:
                            door_x, door_y = origin_x + ROOM_WIDTH + 1, origin_y + 1 + ROOM_HEIGHT // 2
                            tilemap[door_y][door_x] = DOOR
                            room_door_count[room_a] += 1
                            room_door_count[room_b] += 1

                    if r < rows - 1 and self.matrix[r + 1][c] != 0:
                        room_b = self.matrix[r + 1][c]
                        if room_b != room_a and room_door_count[room_a] < room_max_doors[room_a] and room_door_count[room_b] < room_max_doors[room_b]:
                            door_x, door_y = origin_x + 1 + ROOM_WIDTH // 2, origin_y + ROOM_HEIGHT + 1
                            tilemap[door_y][door_x] = DOOR
                            room_door_count[room_a] += 1
                            room_door_count[room_b] += 1

    def merge_rooms(self, tilemap, rows, cols):
        # Remove walls between horizontally merged rooms (1x2, 1x3, etc.)
        for r in range(rows):
            for c in range(cols - 1):
                if self.matrix[r][c] != 0 and self.matrix[r][c + 1] == self.matrix[r][c]:
                    wall_x = (c + 1) * CELL_WIDTH
                    for y in range(r * CELL_HEIGHT + 1, r * CELL_HEIGHT + 1 + ROOM_HEIGHT):
                        tilemap[y][wall_x] = FLOOR

        # Remove walls between vertically merged rooms (2x1, 3x1, etc.)
        for r in range(rows - 1):
            for c in range(cols):
                if self.matrix[r][c] != 0 and self.matrix[r + 1][c] == self.matrix[r][c]:
                    wall_y = (r + 1) * CELL_HEIGHT
                    for x in range(c * CELL_WIDTH + 1, c * CELL_WIDTH + 1 + ROOM_WIDTH):
                        tilemap[wall_y][x] = FLOOR

    def get_wall_rects(self):
        visited = set()
        wall_rects = []

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

    def draw(self, screen, cam_x, cam_y):
        for wall in self.wall_rects:
            pygame.draw.rect(screen, COLOR_WALL, pygame.Rect(wall.x - cam_x, wall.y - cam_y, wall.width, wall.height))

    def get_walls_in_radius(self, x, y, radius):
        walls = []
        center = pygame.Vector2(x, y)
    
        for wall in self.wall_rects:
            wall_center = pygame.Vector2(wall.centerx, wall.centery)
            if center.distance_to(wall_center) <= radius:
                walls.append(wall)
    
        return walls
