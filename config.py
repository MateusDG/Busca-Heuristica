# config.py
import math

# Configurações do grid
ROWS = 42
COLS = 42
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
