import tkinter as tk
import heapq
import math

# Configurações do grid
ROWS, COLS = 42, 42
CELL_SIZE = 20  # Tamanho de cada célula em pixels

# Variáveis globais para controle da animação
speed_delay = 100       # Delay inicial em milissegundos
agent_shape = None      # Referência ao desenho do agente (imagem)
highlight_shape = None  # Referência ao destaque da célula atual
animation_job = None    # Identificador do callback agendado pelo after()
agent_image = None      # Imagem do agente (após ajuste)
computed_path = None    # Armazena o caminho completo computado

# Dicionário de terrenos com seus custos, cores e nomes
char_to_terrain = {
    '.': {"name": "Piso seco",       "cost": 1,    "color": "#D3D3D3"},
    '~': {"name": "Piso molhado",    "cost": 3,    "color": "#70b2ff"},
    'R': {"name": "Fiação exposta",  "cost": 6,    "color": "#8B0000"},
    'P': {"name": "Porta",           "cost": 4,    "color": "brown"},
    '#': {"name": "Parede",          "cost": None, "color": "#696969"},
    'E': {"name": "E",               "cost": 1,    "color": "pink"},
    'D': {"name": "D",               "cost": 1,    "color": "pink"},
    'L': {"name": "L",               "cost": 1,    "color": "pink"},
    'M': {"name": "M",               "cost": 1,    "color": "pink"},
    'W': {"name": "W",               "cost": 1,    "color": "pink"},
    'S': {"name": "Saída",           "cost": 1,    "color": "brown"}
}

# Mapa original (imóvel) para podermos resetar o mapa
original_map_lines = [
    "##########################################",
    "#..............#............#..~~........#",
    "#..RRR~.~RRRRR.P............#..~~..#RRR..#",
    "#..RRR..~RRRRR~#............#..~~..#RRR..#",
    "#..RRR.~~RRRRR~#....RRR.....#..~~..#RRR..#",
    "#..RRR.D......~#~~~.RRR.....#..~~..#RRR..#",
    "#..RRR...RR....#~~~.RRR.....#~.....#....E#",
    "#........RR....#~~~.RRR.....#~.....#######",
    "#..............#~~~.RRR.....#RRRRR.......#",
    "################~~~.RRR.....#RRRRR.......#",
    "#...............~~~.RRR.....#RRRRR.......#",
    "#...........................#............#",
    "#..................~~~~~~...###P##########",
    "#.....................~~~~...............#",
    "###P################.....~~~~~~~.........#",
    "#....~~~...........#.....................#",
    "#.........~~~~~....#RRRR################P#",
    "#...RRRRRRRRRRRRR..#RRRR#~...........M#..#",
    "#...~~~~.....~~....#....#.~..........#R..#",
    "#...~~~~.....~~....#....#..~~~......#RR..#",
    "#########.L..~~....#....#..~~~.....#RRR..#",
    "#.......#....~~....#....#..~~~....#RRR...#",
    "#.......#..........#....#..~~~...#RRR....#",
    "#.......#..........#....P..~~~..#RRRR....#",
    "#.......############....#..~...#RRRR.....#",
    "#...........RRRRR.......#..~..#RRRRR.....#",
    "#.~~~~~.....RRRRR.......#..~..#RRR.......#",
    "#.~~~~~RRRRRRRR.........#..~..#RR........#",
    "#.~~~~~RRR#####.........#.....#RR.~~~~...#",
    "#.....RR.#....#....~..R.#.....#RR.~~~~...#",
    "#~~~~...#..W..#....~..R.#.....#RR.~~~~...#",
    "#~~~..##......#.RRR~RRR.#.....#RR.~~~~...#",
    "#....#..RRR...#.......R.#######RR....RR#P#",
    "#...#...RRR...#RRRRR..RRRRRRRRRRR...RR#..#",
    "##P#....RRR...#.......R............RR#...#",
    "#....~~~RRR...#~~~.RRRR..........RRR#....#",
    "#....~~~......#~~~....R~~~~.....RRR#..~~~#",
    "###############~~~....R..~..RRRRRR#...~~~#",
    "#..............~~~....R..~..RRRRR#....~~~#",
    "#..............~~~.......~..RRRR#........#",
    "#...........................RRRRP........#",
    "#######################################S##"
]

# Inicialmente, o mapa ativo é uma cópia do original
map_lines = original_map_lines[:]

#------------------------------------------------------------------------------
#                      FUNÇÃO PARA REMOVER PERSONAGENS
#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------
#                      FUNÇÕES DE APOIO
#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------
#                      FUNÇÕES PARA DESENHO E ANIMAÇÃO
#------------------------------------------------------------------------------

def draw_map(canvas):
    canvas.delete("all")
    for i in range(ROWS):
        line = map_lines[i]
        for j in range(COLS):
            cell_char = line[j]
            terrain_info = char_to_terrain.get(cell_char, {"name": "", "color": "white"})
            color = terrain_info["color"]
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if cell_char in ['E','D','L','M','W','S']:
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                canvas.create_text(cx, cy, text=terrain_info["name"],
                                   fill="black", font=("Arial", 8, "bold"), tags="label")
    canvas.tag_raise("label")

def draw_path(canvas, path):
    if not path:
        print("Caminho não encontrado!")
        return
    for pos in path:
        i, j = pos
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill="magenta", outline="black")
    canvas.update_idletasks()
    canvas.tag_raise("label")

def find_cell(character):
    for i in range(ROWS):
        line = map_lines[i]
        if character in line:
            return (i, line.index(character))
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

def animate_agent(canvas, path, index=0):
    global agent_shape, highlight_shape, speed_delay, animation_job, agent_image, computed_path
    if index < len(path):
        pos = path[index]
        i, j = pos
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        
        # Se a célula atual contém um personagem, remove-o e atualiza o mapa
        if map_lines[i][j] in ['E','D','L','M','W']:
            remove_friend_at(pos)
            draw_map(canvas)
            if computed_path is not None:
                draw_path(canvas, computed_path)
        
        if agent_shape is not None:
            canvas.delete(agent_shape)
        agent_shape = canvas.create_image((x1+x2)/2, (y1+y2)/2, image=agent_image)
        
        if highlight_shape is not None:
            canvas.delete(highlight_shape)
        highlight_shape = canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
        
        canvas.update_idletasks()
        canvas.tag_raise("label")
        animation_job = canvas.after(speed_delay, lambda: animate_agent(canvas, path, index+1))
    else:
        if highlight_shape is not None:
            canvas.delete(highlight_shape)
        animation_job = None
        print("Animação concluída.")

def start_full_search(canvas):
    global animation_job, computed_path
    if animation_job is not None:
        canvas.after_cancel(animation_job)
        animation_job = None
    computed_path = compute_full_path()
    if computed_path:
        total_cost = sum(get_cost(i, j) for i, j in computed_path)
        print("Caminho completo encontrado com custo:", total_cost)
        draw_path(canvas, computed_path)
        animate_agent(canvas, computed_path)
    else:
        print("Não foi possível computar o caminho completo.")

def reset_map(canvas):
    global agent_shape, highlight_shape, animation_job, computed_path, map_lines
    if animation_job is not None:
        canvas.after_cancel(animation_job)
        animation_job = None
    map_lines = original_map_lines[:]  # Cria uma cópia do mapa original
    computed_path = None
    canvas.delete("all")
    draw_map(canvas)

def update_speed(val):
    global speed_delay
    speed_delay = int(val)

def main():
    global agent_image
    root = tk.Tk()
    root.title("Busca Heurística Interativa - Fuga do Laboratório")
    
    canvas_width = COLS * CELL_SIZE
    canvas_height = ROWS * CELL_SIZE
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    
    # Carrega a imagem do agente e ajusta seu tamanho para aproximar CELL_SIZE (20 pixels)
    img = tk.PhotoImage(file="eleven.png")
    w_original = img.width()
    h_original = img.height()
    desired_size = CELL_SIZE  # Tamanho desejado: 20 pixels
    if w_original > desired_size or h_original > desired_size:
        factor_w = max(1, round(w_original / desired_size))
        factor_h = max(1, round(h_original / desired_size))
        agent_image = img.subsample(factor_w, factor_h)
    elif w_original < desired_size or h_original < desired_size:
        factor_w = max(1, round(desired_size / w_original))
        factor_h = max(1, round(desired_size / h_original))
        agent_image = img.zoom(factor_w, factor_h)
    else:
        agent_image = img
    
    draw_map(canvas)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    start_button = tk.Button(button_frame, text="Start", command=lambda: start_full_search(canvas))
    start_button.pack(side=tk.LEFT, padx=5)
    
    reset_button = tk.Button(button_frame, text="Restart", command=lambda: reset_map(canvas))
    reset_button.pack(side=tk.LEFT, padx=5)
    
    speed_slider = tk.Scale(button_frame, from_=1, to=500, orient=tk.HORIZONTAL,
                            label="Speed (ms)", command=update_speed)
    speed_slider.set(speed_delay)
    speed_slider.pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
