# drawing.py
import tkinter as tk
import config
from config import map_lines, CELL_SIZE, char_to_terrain, ROWS, COLS
from grid import remove_friend_at, get_cost
from pathfinding import compute_segments

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
            if cell_char in ['E', 'D', 'L', 'M', 'W', 'S']:
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                canvas.create_text(cx, cy, text=terrain_info["name"],
                                   fill="black", font=("Arial", 8, "bold"), tags="label")
    canvas.tag_raise("label")

def draw_path(canvas, path, color="magenta"):
    # Desenha o segmento atual sem apagar os anteriores
    for pos in path:
        i, j = pos
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    canvas.update_idletasks()
    canvas.tag_raise("label")

def animate_agent_segment(canvas, path, index=0, on_segment_end=None):
    if index < len(path):
        pos = path[index]
        i, j = pos
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        # Atualiza somente a posição do agente e o destaque da célula
        if config.agent_shape is not None:
            canvas.delete(config.agent_shape)
        config.agent_shape = canvas.create_image((x1+x2)/2, (y1+y2)/2, image=config.agent_image)

        if config.highlight_shape is not None:
            canvas.delete(config.highlight_shape)
        config.highlight_shape = canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

        canvas.update_idletasks()
        canvas.tag_raise("label")
        config.animation_job = canvas.after(config.speed_delay,
            lambda: animate_agent_segment(canvas, path, index+1, on_segment_end))
    else:
        # Ao final do segmento, remove o personagem (se aplicável) na última célula
        pos = path[-1]
        i, j = pos
        if map_lines[i][j] in ['E', 'D', 'L', 'M', 'W']:
            remove_friend_at(pos)
        config.animation_job = None
        print("Segmento concluído.")
        if on_segment_end:
            on_segment_end()

def animate_segments(canvas, segments, cost_label, seg_index=0, cum_cost=0):
    if seg_index == 0:
        # Desenha o mapa apenas uma vez no início
        draw_map(canvas)
    if seg_index < len(segments):
        segment = segments[seg_index]
        # Desenha o segmento atual (acumulando os anteriores)
        draw_path(canvas, segment)
        def on_segment_end():
            # Calcula o custo do segmento atual
            seg_cost = sum(get_cost(i, j) for i, j in segment)
            new_cum_cost = cum_cost + seg_cost
            cost_label.config(text=f"Custo: {new_cum_cost}")
            # Anima o próximo segmento com o custo acumulado atualizado
            animate_segments(canvas, segments, cost_label, seg_index+1, new_cum_cost)
        animate_agent_segment(canvas, segment, 0, on_segment_end)
    else:
        print("Animação completa de todos os segmentos.")

def start_full_search(canvas, cost_label):
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    segments = compute_segments()
    if segments:
        # Reinicia o label de custo antes de iniciar a animação
        cost_label.config(text="Custo: 0")
        animate_segments(canvas, segments, cost_label)
    else:
        print("Não foi possível computar o caminho completo.")
        cost_label.config(text="Caminho não encontrado.")

def reset_map(canvas):
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    # Restaura o mapa original, criando uma nova cópia da lista
    config.map_lines = config.original_map_lines[:]
    # Reinicia as variáveis de controle
    config.computed_path = None
    config.agent_shape = None
    config.highlight_shape = None
    # Limpa o canvas e redesenha o mapa
    canvas.delete("all")
    draw_map(canvas)

def update_speed(val):
    config.speed_delay = int(val)
