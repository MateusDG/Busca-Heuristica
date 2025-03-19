import tkinter as tk
import config
from algorithms import compute_full_path, remove_friend_at, get_cost, find_cell, a_star
from drawing import draw_map, draw_path

def animate_agent(canvas, path, index=0, cost_label=None):
    """
    Anima o movimento do agente ao longo do caminho.

    Parâmetros:
      canvas     - widget Tkinter onde a animação é desenhada.
      path       - lista de posições (tuplas) que formam o caminho.
      index      - índice atual no caminho (padrão: 0).
      cost_label - Label para exibir o custo acumulado (opcional).
    """
    if index < len(path):
        pos = path[index]
        i, j = pos
        x1 = j * config.CELL_SIZE
        y1 = i * config.CELL_SIZE
        x2 = x1 + config.CELL_SIZE
        y2 = y1 + config.CELL_SIZE

        # Atualiza o custo acumulado
        if index == 0:
            config.cumulative_cost = get_cost(i, j)
        else:
            config.cumulative_cost += get_cost(i, j)

        if cost_label is not None:
            cost_label.config(text=f"Custo: {config.cumulative_cost}")

        # Se a célula atual contém um personagem, remove-o e redesenha o mapa e o caminho
        if config.map_lines[i][j] in ['E', 'D', 'L', 'M', 'W']:
            remove_friend_at(pos)
            draw_map(canvas)
            if config.computed_path is not None:
                draw_path(canvas, config.computed_path)

        # Atualiza a posição do agente
        if config.agent_shape is not None:
            canvas.delete(config.agent_shape)
        config.agent_shape = canvas.create_image((x1+x2)/2, (y1+y2)/2, image=config.agent_image)

        # Destaca a célula atual
        if config.highlight_shape is not None:
            canvas.delete(config.highlight_shape)
        config.highlight_shape = canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

        canvas.update_idletasks()
        canvas.tag_raise("label")
        config.animation_job = canvas.after(config.speed_delay, lambda: animate_agent(canvas, path, index+1, cost_label))
    else:
        if config.highlight_shape is not None:
            canvas.delete(config.highlight_shape)
        config.animation_job = None
        print("Animacao concluida.")

def start_full_search(canvas, cost_label):
    """
    Inicia a busca completa e anima o agente seguindo o caminho encontrado.

    Parâmetros:
      canvas     - widget Tkinter onde o mapa e a animação são exibidos.
      cost_label - Label para exibir o custo acumulado.
    """
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    config.cumulative_cost = 0
    config.computed_path = compute_full_path()
    if config.computed_path:
        total_cost = sum(get_cost(i, j) for i, j in config.computed_path)
        print("Caminho completo encontrado com custo:", total_cost)
        draw_path(canvas, config.computed_path)
        animate_agent(canvas, config.computed_path, cost_label=cost_label)
    else:
        print("Nao foi possivel computar o caminho completo.")

def show_full_path(canvas, cost_label):
    """
    Mostra o caminho completo sem animação, apenas desenhando o caminho no mapa.

    Parâmetros:
      canvas     - widget Tkinter onde o mapa e o caminho são exibidos.
      cost_label - Label para exibir o custo acumulado.
    """
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    config.cumulative_cost = 0
    config.computed_path = compute_full_path()
    if config.computed_path:
        total_cost = sum(get_cost(i, j) for i, j in config.computed_path)
        print("Caminho completo encontrado com custo:", total_cost)
        draw_path(canvas, config.computed_path)
        config.cumulative_cost = total_cost
        if cost_label is not None:
            cost_label.config(text=f"Custo: {config.cumulative_cost}")
    else:
        print("Nao foi possivel computar o caminho completo.")

def reset_map(canvas):
    """
    Reseta o mapa para o estado original e cancela qualquer animação em andamento.

    Parâmetro:
      canvas - widget Tkinter onde o mapa é exibido.
    """
    if config.animation_job is not None:
        canvas.after_cancel(config.animation_job)
        config.animation_job = None
    config.map_lines = config.original_map_lines.copy()
    draw_map(canvas)
    config.agent_shape = None
    config.highlight_shape = None

def update_speed(val):
    """
    Atualiza a velocidade (delay) da animação.

    Parâmetro:
      val - novo valor de delay (em milissegundos) como string.
    """
    config.speed_delay = int(val)
