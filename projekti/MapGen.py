import pygame
import random
import sys

# --------------------------
# CONFIGURATION & CONSTANTS
# --------------------------

# Room size in tiles
ROOM_WIDTH = 10    # horizontal floor tiles
ROOM_HEIGHT = 8    # vertical floor tiles

# Each grid cell (if it has a room) is drawn as a room box:
# Leave a 1-tile border for walls.
CELL_WIDTH  = ROOM_WIDTH + 1  # in tiles
CELL_HEIGHT = ROOM_HEIGHT + 1  # in tiles

# We now use a larger tile size so that the door openings (one tile wide) are big enough for the player to go through
TILE_SIZE = 64

# Matrix dimensions
MATRIX_COLS = 30  # width
MATRIX_ROWS = 9   # height

# Screen resolution
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Player settings
PLAYER_SIZE = 32
PLAYER_SPEED = 5

# Tile codes for global tilemap:
FLOOR = 0
WALL  = 1
DOOR  = 2

# Colors for rendering
COLOR_FLOOR  = (200, 200, 200)  # light gray
COLOR_WALL   = (50, 50, 50)     # dark gray
COLOR_DOOR   = (150, 75, 0)     # brown
COLOR_PLAYER = (0, 150, 0)      # green


# MATRIX GENERATION
def generoi_tile_matriisi():
    pituus = MATRIX_COLS
    korkeus = MATRIX_ROWS

    # Create an empty matrix (0 means “no room”/wall)
    matrix = [[0 for _ in range(pituus)] for _ in range(korkeus)]
    
    # Place the starting room at the middle row of the leftmost column.
    matrix[len(matrix) // 2][0] = 1
    
    current_id = 2
    
    # Probabilities for growth
    row_probabilities = {
        0: 0.005,
        1: 0.01,
        2: 0.05,
        3: 1,
        4: 1,
        5: 1,
        6: 0.05,
        7: 0.01,
        8: 0.005
    }
    
    col_probabilities = {
        0: 0.001,
        1: 0.01,
        2: 0.05,
        3: 0.1,
        4: 0.5
    }
    
    while True:
        # Stop if any room reaches the rightmost column.
        if any(matrix[r][pituus - 1] > 0 for r in range(korkeus)):
            break
        
        positions = [(r, c) for r in range(korkeus) for c in range(pituus) if matrix[r][c] > 0]
        if not positions:
            break
        
        weighted_positions = []
        for r, c in positions:
            col_prob = col_probabilities.get(c, 1)
            if random.random() < row_probabilities[r] and random.random() < col_prob:
                weighted_positions.append((r, c))
        
        if not weighted_positions:
            continue
        
        r, c = random.choice(weighted_positions)
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        random.shuffle(neighbors)
        
        # Randomly choose a room type: a normal 1x1 room, or a big 1x2/2x1 room.
        room_type = random.choice(["1x1", "1x2", "2x1"])
        for nr, nc in neighbors:
            if 0 <= nr < korkeus and 0 <= nc < pituus and matrix[nr][nc] == 0:
                if room_type == "1x1":
                    matrix[nr][nc] = current_id
                elif room_type == "1x2" and nc + 1 < pituus and matrix[nr][nc + 1] == 0:
                    matrix[nr][nc] = current_id
                    matrix[nr][nc + 1] = current_id
                elif room_type == "2x1" and nr + 1 < korkeus and matrix[nr + 1][nc] == 0:
                    matrix[nr][nc] = current_id
                    matrix[nr + 1][nc] = current_id
                else:
                    continue
                current_id += 1
                break
    return matrix


# BUILD GLOBAL TILEMAP FROM MATRIX
def build_global_tilemap(matrix):

    rows = len(matrix)
    cols = len(matrix[0])
    # Global tilemap dimensions
    map_width  = cols * CELL_WIDTH + 1  # each cell contributes CELL_WIDTH tiles, plus one extra wall column
    map_height = rows * CELL_HEIGHT + 1
    # Start with all WALL tiles.
    tilemap = [[WALL for _ in range(map_width)] for _ in range(map_height)]
    
    # Carve out each room cell’s interior (leaving a 1-tile wall border)
    for r in range(rows):
        for c in range(cols):
            origin_x = c * CELL_WIDTH
            origin_y = r * CELL_HEIGHT
            if matrix[r][c] != 0:
                for y in range(origin_y + 1, origin_y + 1 + ROOM_HEIGHT):
                    for x in range(origin_x + 1, origin_x + 1 + ROOM_WIDTH):
                        tilemap[y][x] = FLOOR
                        
    # Limit the number of doors per room
    room_sizes = {}
    for r in range(rows):
        for c in range(cols):
            room_id = matrix[r][c]
            if room_id:
                room_sizes[room_id] = room_sizes.get(room_id, 0) + 1
    # For a 1x1 room (size==1) allow max 3 doors, for merged rooms (size>1) allow max 5
    room_max_doors = {room_id: (3 if size == 1 else 5) for room_id, size in room_sizes.items()}
    room_door_count = {room_id: 0 for room_id in room_sizes}
    
    # Create door openings between adjacent cells—only if they belong to different rooms and if neither room has exceeded its door limit
    for r in range(rows):
        for c in range(cols):
            origin_x = c * CELL_WIDTH
            origin_y = r * CELL_HEIGHT
            if matrix[r][c] != 0:
                room_a = matrix[r][c]
                # East door: check right neighbor exists, is a room, and is a different room
                if c < cols - 1 and matrix[r][c + 1] != 0:
                    room_b = matrix[r][c + 1]
                    if room_b != room_a:
                        if (room_door_count[room_a] < room_max_doors[room_a] and
                            room_door_count[room_b] < room_max_doors[room_b]):
                            door_x = origin_x + ROOM_WIDTH + 1
                            door_y = origin_y + 1 + ROOM_HEIGHT // 2
                            tilemap[door_y][door_x] = DOOR
                            room_door_count[room_a] += 1
                            room_door_count[room_b] += 1
                # South door: check bottom neighbor exists, is a room, and is a different room
                if r < rows - 1 and matrix[r + 1][c] != 0:
                    room_b = matrix[r + 1][c]
                    if room_b != room_a:
                        if (room_door_count[room_a] < room_max_doors[room_a] and
                            room_door_count[room_b] < room_max_doors[room_b]):
                            door_x = origin_x + 1 + ROOM_WIDTH // 2
                            door_y = origin_y + ROOM_HEIGHT + 1
                            tilemap[door_y][door_x] = DOOR
                            room_door_count[room_a] += 1
                            room_door_count[room_b] += 1

    # Remove walls between cells that were merged into one room
    # For horizontal merging, remove the vertical wall.
    for r in range(rows):
        for c in range(cols - 1):
            if matrix[r][c] != 0 and matrix[r][c + 1] == matrix[r][c]:
                wall_x = (c + 1) * CELL_WIDTH
                for y in range(r * CELL_HEIGHT + 1, r * CELL_HEIGHT + 1 + ROOM_HEIGHT):
                    tilemap[y][wall_x] = FLOOR
    # For vertical merging, remove the horizontal wall.
    for r in range(rows - 1):
        for c in range(cols):
            if matrix[r][c] != 0 and matrix[r + 1][c] == matrix[r][c]:
                wall_y = (r + 1) * CELL_HEIGHT
                for x in range(c * CELL_WIDTH + 1, c * CELL_WIDTH + 1 + ROOM_WIDTH):
                    tilemap[wall_y][x] = FLOOR
                    
    return tilemap


# BUILD COLLISION RECTANGLES FROM TILEMAP
def get_wall_rects(tilemap):
    rects = []
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == WALL:
                rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return rects


# MAIN GAME LOOP
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scaled Rooms with Door Limitations")
    clock = pygame.time.Clock()
    
    # Generate the Matrix and build the global tilemap.
    matrix = generoi_tile_matriisi()
    global_tilemap = build_global_tilemap(matrix)
    
    # Full map size in pixels
    map_width_px = len(global_tilemap[0]) * TILE_SIZE
    map_height_px = len(global_tilemap) * TILE_SIZE
    
    # Build walls
    wall_rects = get_wall_rects(global_tilemap)
    
    # Place the player in the starting room
    start_r = MATRIX_ROWS // 2
    start_c = 0
    origin_x = start_c * CELL_WIDTH
    origin_y = start_r * CELL_HEIGHT
    # Position the player in the center of the room’s floor
    player_px = (origin_x + 1 + ROOM_WIDTH // 2) * TILE_SIZE
    player_py = (origin_y + 1 + ROOM_HEIGHT // 2) * TILE_SIZE
    player_rect = pygame.Rect(player_px, player_py, PLAYER_SIZE, PLAYER_SIZE)
    
    running = True
    while running:
        dt = clock.tick(60)  # Limit to 60 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED
        
        # Move player (horizontal then vertical) and check collision with walls
        old_rect = player_rect.copy()
        player_rect.x += dx
        for wall in wall_rects:
            if player_rect.colliderect(wall):
                player_rect.x = old_rect.x
                break
        player_rect.y += dy
        for wall in wall_rects:
            if player_rect.colliderect(wall):
                player_rect.y = old_rect.y
                break
        
        # Center the camera on the player
        cam_x = player_rect.centerx - SCREEN_WIDTH // 2
        cam_y = player_rect.centery - SCREEN_HEIGHT // 2
        # Clamp the camera so it never goes beyond the full map
        cam_x = max(0, min(cam_x, map_width_px - SCREEN_WIDTH))
        cam_y = max(0, min(cam_y, map_height_px - SCREEN_HEIGHT))
        

        screen.fill((0, 0, 0))  # Black background
        
        # Only draw the visible portion of the tilemap
        start_col = cam_x // TILE_SIZE
        end_col   = (cam_x + SCREEN_WIDTH) // TILE_SIZE + 1
        start_row = cam_y // TILE_SIZE
        end_row   = (cam_y + SCREEN_HEIGHT) // TILE_SIZE + 1
        
        for y in range(start_row, min(len(global_tilemap), end_row)):
            for x in range(start_col, min(len(global_tilemap[0]), end_col)):
                tile = global_tilemap[y][x]
                rect = pygame.Rect(x * TILE_SIZE - cam_x, y * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
                if tile == FLOOR:
                    color = COLOR_FLOOR
                elif tile == WALL:
                    color = COLOR_WALL
                elif tile == DOOR:
                    color = COLOR_DOOR
                else:
                    color = (255, 0, 255)  # Pink for unknown tiles
                pygame.draw.rect(screen, color, rect)
        
        # Draw the player (adjust for camera offset)
        draw_player = player_rect.copy()
        draw_player.x -= cam_x
        draw_player.y -= cam_y
        pygame.draw.rect(screen, COLOR_PLAYER, draw_player)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()