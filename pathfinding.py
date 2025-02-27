# pathfinding.py
import heapq
import math
from grid import get_cost, get_neighbors, find_cell

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
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

def compute_full_path():
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
