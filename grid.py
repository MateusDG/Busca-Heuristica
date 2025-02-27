# grid.py
from config import map_lines, ROWS, COLS, char_to_terrain

def remove_friend_at(pos):
    """
    Atualiza o mapa removendo o personagem (E, D, L, M ou W) na posição 'pos'
    (substituindo-o por '.').
    """
    i, j = pos
    row = list(map_lines[i])
    if row[j] in ['E', 'D', 'L', 'M', 'W']:
        row[j] = '.'
        map_lines[i] = "".join(row)

def get_cost(i, j):
    cell_char = map_lines[i][j]
    return char_to_terrain.get(cell_char, char_to_terrain['#'])["cost"]

def get_neighbors(pos):
    i, j = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < ROWS and 0 <= nj < COLS and get_cost(ni, nj) is not None:
            neighbors.append((ni, nj))
    return neighbors

def find_cell(character):
    for i in range(ROWS):
        line = map_lines[i]
        if character in line:
            return (i, line.index(character))
    return None
