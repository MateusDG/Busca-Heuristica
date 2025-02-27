# drawing.py
import tkinter as tk
import config
from config import map_lines, CELL_SIZE
from grid import remove_friend_at, get_cost
from pathfinding import compute_full_path

def draw_map(canvas):
    canvas.delete("all")
    for i in range(config.ROWS):
        line = map_lines[i]
        for j in range(config.COLS):
            cell_char = line[j]
            terrain_info = config.char_to_terrain.get(cell_char, {"name": "", "color": "white"})
            color = terrain_info["color"]
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if cell_char in ['E', 'D', 'L', 'M', 'W', 'S']:
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

def animate_agent(canvas, path, index=0):
    if index < len(path):
        pos = path[index]
        i, j = pos
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        
        if map_lines[i][j] in ['E', 'D', 'L', 'M', 'W']:
            remove_friend_at(pos)
            draw_map(canvas)
            if config.computed_path is not None:
                draw_path(canvas, config.computed_path)
        
        if config.agent_shape is not None:
            canvas.delete(config.agent_shape)
        config.agent_shape = canvas.create_image((x1+x2)/2, (y1+y2)/2, image=config.agent_image)
        
        if config.highlight_shape is not None:
            canvas.delete(config.highlight_shape)
        config.highlight_shape = canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
        
        canvas.update_idletasks()
        canvas.tag_raise("label")
        config.animation_job = canvas.after(config.speed_delay, lambda: animate_agent(canvas, path, index+1))
    else:
        if config.highlight_shape is not None:
            canvas.delete(config.highlight_shape)
        config.animation_job = None
        print("Animação concluída.")

def start_full_search(canvas, cost_label):
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    config.computed_path = compute_full_path()
    if config.computed_path:
        total_cost = sum(get_cost(i, j) for i, j in config.computed_path)
        print("Caminho completo encontrado com custo:", total_cost)
        cost_label.config(text=f"Custo: {total_cost}")
        draw_path(canvas, config.computed_path)
        animate_agent(canvas, config.computed_path)
    else:
        print("Não foi possível computar o caminho completo.")
        cost_label.config(text="Caminho não encontrado.")

def reset_map(canvas):
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    # Reinicia o mapa para o estado original
    config.map_lines = config.original_map_lines[:]  # Cria uma cópia do mapa original
    config.computed_path = None
    canvas.delete("all")
    draw_map(canvas)

def update_speed(val):
    config.speed_delay = int(val)
