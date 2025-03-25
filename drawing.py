import config
import tkinter as tk

def draw_map(canvas):
    """
    Desenha o mapa no canvas.
    
    Para cada célula do mapa, desenha um retângulo com a cor definida no dicionário
    de terrenos. Se a célula contém um personagem ou saída ('E', 'D', 'L', 'M', 'W', 'S'),
    desenha também o nome no centro da célula.
    
    Parâmetro:
      canvas - widget do Tkinter onde o mapa será desenhado.
    """
    canvas.delete("all")
    for i in range(config.ROWS):
        line = config.map_lines[i]
        for j in range(config.COLS):
            cell_char = line[j]
            terrain_info = config.char_to_terrain.get(cell_char, config.char_to_terrain['#'])
            color = terrain_info["color"]
            x1 = j * config.CELL_SIZE
            y1 = i * config.CELL_SIZE
            x2 = x1 + config.CELL_SIZE
            y2 = y1 + config.CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if cell_char in ['E', 'D', 'L', 'M', 'W', 'S']:
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                canvas.create_text(cx, cy, text=terrain_info["name"],
                                   fill="black", font=("Arial", 8, "bold"), tags="label")
    canvas.tag_raise("label")
    
# Deve existir uma maneira de visualizar os movimentos do agente, 
# mesmo que a interface seja bem simples. 
# Podendo até mesmo ser uma matriz desenhada e atualizada no console.

def draw_path(canvas, path):
    """
    Desenha o caminho encontrado no canvas.
    
    Cada célula presente na lista 'path' é desenhada com um retângulo de cor magenta.
    
    Parâmetros:
      canvas - widget do Tkinter onde o caminho será desenhado.
      path   - lista de posições (tuplas) que formam o caminho.
    """
    if not path:
        print("Caminho nao encontrado!")
        return
    for pos in path:
        i, j = pos
        x1 = j * config.CELL_SIZE
        y1 = i * config.CELL_SIZE
        x2 = x1 + config.CELL_SIZE
        y2 = y1 + config.CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill="magenta", outline="black")
    canvas.update_idletasks()
    canvas.tag_raise("label")
