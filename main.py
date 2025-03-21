# main.py
import tkinter as tk
from drawing import draw_map
from animation import start_full_search, show_full_path, reset_map, update_speed
import config

def main():
    root = tk.Tk()
    root.title("Busca Heuristica - Fuga do Laboratório")
    
    canvas_width = config.COLS * config.CELL_SIZE
    canvas_height = config.ROWS * config.CELL_SIZE
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    
    # Carrega a imagem do agente e ajusta o tamanho usando subsample ou zoom
    img = tk.PhotoImage(file="img/eleven.png")
    w_original = img.width()
    h_original = img.height()
    desired_size = config.CELL_SIZE 
    if w_original > desired_size or h_original > desired_size:
        factor_w = max(1, round(w_original / desired_size))
        factor_h = max(1, round(h_original / desired_size))
        config.agent_image = img.subsample(factor_w, factor_h)
    elif w_original < desired_size or h_original < desired_size:
        factor_w = max(1, round(desired_size / w_original))
        factor_h = max(1, round(desired_size / h_original))
        config.agent_image = img.zoom(factor_w, factor_h)
    else:
        config.agent_image = img
    
    draw_map(canvas)
    
    cost_label = tk.Label(root, text="Custo: 0")
    cost_label.pack(pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    start_button = tk.Button(button_frame, text="Start(Animacao)", command=lambda: start_full_search(canvas, cost_label))
    start_button.pack(side=tk.LEFT, padx=5)
    
    show_button = tk.Button(button_frame, text="Start(Sem animacao)", command=lambda: show_full_path(canvas, cost_label))
    show_button.pack(side=tk.LEFT, padx=5)
    
    reset_button = tk.Button(button_frame, text="Reset", command=lambda: reset_map(canvas))
    reset_button.pack(side=tk.LEFT, padx=5)
    
    speed_slider = tk.Scale(button_frame, from_=1, to=500, orient=tk.HORIZONTAL,
                            label="Speed (ms)", command=update_speed)
    speed_slider.set(config.speed_delay)
    speed_slider.pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
