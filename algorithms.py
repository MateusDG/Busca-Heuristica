import heapq
import math
import config

def remove_friend_at(pos):
    """
    Remove o personagem ('E', 'D', 'L', 'M' ou 'W') da posição 'pos', substituindo-o por '.'.
    
    Parâmetro:
      pos - (linha, coluna)
    """
    i, j = pos
    row = list(config.map_lines[i])
    if row[j] in ['E', 'D', 'L', 'M', 'W']:
        row[j] = '.'
        config.map_lines[i] = "".join(row)

def get_cost(i, j):
    """
    Retorna o custo para atravessar a célula na posição (i, j).
    
    Parâmetros:
      i - número da linha
      j - número da coluna
    """
    cell_char = config.map_lines[i][j]
    return config.char_to_terrain.get(cell_char, config.char_to_terrain['#'])["cost"]

def get_neighbors(pos):
    """
    Retorna as células vizinhas válidas (acima, abaixo, esquerda e direita) da posição 'pos'.
    
    Parâmetro:
      pos - (linha, coluna)
    """
    i, j = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < config.ROWS and 0 <= nj < config.COLS and get_cost(ni, nj) is not None:
            neighbors.append((ni, nj))
    return neighbors

def heuristic(a, b):
    """
    Calcula a distância Manhattan entre as posições a e b.
    
    Parâmetros:
      a - (linha, coluna)
      b - (linha, coluna)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    """
    Encontra um caminho entre 'start' e 'goal' usando o algoritmo A*.
    
    Parâmetros:
      start - posição inicial (linha, coluna)
      goal  - posição final (linha, coluna)
      
    Retorna:
      Lista de posições que formam o caminho ou None se não encontrar.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
        
        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + get_cost(neighbor[0], neighbor[1])
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

def find_cell(character):
    """
    Procura a primeira ocorrência do caractere no mapa.
    
    Parâmetro:
      character - caractere a ser procurado (ex.: 'E', 'S')
      
    Retorna:
      (linha, coluna) ou None se não encontrar.
    """
    for i in range(config.ROWS):
        line = config.map_lines[i]
        if character in line:
            return (i, line.index(character))
    return None

def compute_full_path():
    """
    Calcula o caminho completo passando por 'E', pelos amigos ('M', 'D', 'L', 'W')
    e terminando na saída ('S').
    
    Retorna:
      Lista de posições que formam o caminho completo ou None se não for possível.
    """
    start = find_cell('E')
    if start is None:
        print("Posição de Eleven não encontrada!")
        return None

    friends = ['M', 'D', 'L', 'W']
    friend_positions = {}
    for f in friends:
        pos = find_cell(f)
        if pos:
            friend_positions[f] = pos
        else:
            print(f"Amigo {f} não encontrado!")
    
    current = start
    full_path = []
    
    while friend_positions:
        best_friend = None
        best_cost = math.inf
        best_path = None
        for f, pos in friend_positions.items():
            path = a_star(current, pos)
            if path:
                cost = sum(get_cost(i, j) for i, j in path)
                if cost < best_cost:
                    best_cost = cost
                    best_friend = f
                    best_path = path
        if best_path is None:
            print("Não foi possível encontrar caminho para algum amigo!")
            return None
        if full_path and best_path[0] == full_path[-1]:
            full_path.extend(best_path[1:])
        else:
            full_path.extend(best_path)
        current = friend_positions.pop(best_friend)
    
    exit_cell = find_cell('S')
    if exit_cell is None:
        print("Saída não encontrada!")
        return None
    path_exit = a_star(current, exit_cell)
    if path_exit is None:
        print("Não foi possível encontrar caminho para a saída!")
        return None
    if full_path and path_exit[0] == full_path[-1]:
        full_path.extend(path_exit[1:])
    else:
        full_path.extend(path_exit)
    
    return full_path
