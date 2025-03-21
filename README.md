# Busca Heurística - Fuga do Laboratório

Este projeto implementa uma aplicação gráfica em Python que utiliza o algoritmo A* para encontrar e animar o caminho de um agente em um labirinto. O objetivo é simular a "fuga" de um laboratório, onde o agente (representado pela personagem "E") precisa coletar amigos (representados por "D", "L", "M", "W") e chegar à saída ("S").

![image](https://github.com/user-attachments/assets/ea129d04-d251-4094-82dc-81392d4458d2)

---

## Funcionalidades

- **Busca Heurística com A\*:** Calcula o caminho de menor custo usando o algoritmo A*.
- **Interface Gráfica:** Utiliza o Tkinter para desenhar o mapa e animar o movimento do agente.
- **Animação:** Mostra o agente se movendo pelo caminho calculado, destacando cada célula enquanto o custo acumulado é atualizado.
- **Reset e Ajuste de Velocidade:** Permite reiniciar o mapa e ajustar a velocidade da animação.

---

## Estrutura do Projeto

O projeto está organizado em módulos para facilitar a manutenção e a compreensão do código:

- **config.py:** Define as configurações do grid, variáveis globais, os tipos de terreno e os mapas (atual e original).
- **algorithms.py:** Contém funções auxiliares e o algoritmo A* para o cálculo do caminho.
- **drawing.py:** Responsável por desenhar o mapa e o caminho no canvas do Tkinter.
- **animation.py:** Gerencia a animação do agente, iniciando a busca completa, mostrando o caminho e resetando o mapa.
- **main.py:** Cria a interface gráfica e integra todas as funcionalidades para a execução da aplicação.

---

## Requisitos

- **Python 3.x:** A aplicação foi desenvolvida em Python 3.
- **Tkinter:** Geralmente incluído na instalação padrão do Python. Caso não esteja instalado, consulte a documentação do Python para instalá-lo.

---

## Como Executar

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/MateusDG/Busca-Heuristica.git
   cd Busca-Heuristica
   ```

2. **Verifique os Arquivos:**

   Certifique-se de que os seguintes arquivos estão na mesma pasta:
   
   - `config.py`
   - `algorithms.py`
   - `drawing.py`
   - `animation.py`
   - `main.py`
   - `eleven.png` (imagem do agente; se necessário, ajuste o caminho para a imagem)

3. **Execute o Projeto:**

   Execute o arquivo principal:
   
   ```bash
   python main.py
   ```

4. **Interaja com a Aplicação:**

   - Use os botões disponíveis para iniciar a animação com ou sem a exibição do caminho completo.
   - Utilize o slider para ajustar a velocidade da animação.
   - O botão de reset retorna o mapa ao estado original.
