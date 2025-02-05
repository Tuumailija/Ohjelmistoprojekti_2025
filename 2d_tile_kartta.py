import random 

def generoi_tile_matriisi():
    pituus = 30
    korkeus = 9

    matrix = [[0 for _ in range(pituus)] for _ in range(korkeus)]

    matrix[len(matrix) // 2][0] = 1

    current_id = 2

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
        if any(matrix[r][pituus-1] > 0 for r in range(len(matrix))):
            break

        positions = [(r, c) for r in range(len(matrix)) for c in range(len(matrix[0])) if matrix[r][c] > 0]

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

        room_type = random.choice(["1x1", "1x2", "2x1"])

        for nr, nc in neighbors:
            if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] == 0:
                if room_type == "1x1":
                    matrix[nr][nc] = current_id
                elif room_type == "1x2" and nc + 1 < len(matrix[0]) and matrix[nr][nc + 1] == 0:
                    matrix[nr][nc] = current_id
                    matrix[nr][nc + 1] = current_id
                elif room_type == "2x1" and nr + 1 < len(matrix) and matrix[nr + 1][nc] == 0:
                    matrix[nr][nc] = current_id
                    matrix[nr + 1][nc] = current_id
                else:
                    continue

                current_id += 1
                break
    return matrix

def print_matrix(matrix):
    print("   " + " ".join(f"{i:2}" for i in range(len(matrix[0]))))
    for idx, row in enumerate(matrix):
        print(f"{idx:2} " + " ".join(f"{cell:2}" if cell != 0 else "  " for cell in row))

if __name__ == "__main__": 
    matrix=generoi_tile_matriisi()
    print_matrix(matrix)
