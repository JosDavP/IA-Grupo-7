import matplotlib.pyplot as plt
import numpy as np
import random

class Environment3x3:
    def __init__(self):
        # Cuadrícula y posición inicial totalmente aleatorias
        self.grid = np.random.choice([0, 1], size=(3, 3))
        self.agent_pos = [random.randint(0, 2), random.randint(0, 2)]
        
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.im = self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)
        self.dot, = self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', ms=20)
        
        self.texts = {(r, c): self.ax.text(c, r, '', ha='center', va='center', weight='bold', fontsize=9) 
                      for r in range(3) for c in range(3)}
        
        self.ax.set_xticks(range(3))
        self.ax.set_yticks(range(3))
        self.ax.set_xlim(-0.5, 2.5)
        self.ax.set_ylim(2.5, -0.5)

    def render(self, step, action):
        self.im.set_data(self.grid)
        self.dot.set_data([self.agent_pos[1]], [self.agent_pos[0]])
        for (r, c), txt in self.texts.items():
            txt.set_text("SUCIO" if self.grid[r, c] == 1 else "LIMPIO")
        self.ax.set_title(f"Paso {step}: {action}")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.5)

    def execute(self, action):
        r, c = self.agent_pos
        if action == 'Suck':
            self.grid[r, c] = 0
        elif action == 'Up' and r > 0:
            self.agent_pos[0] -= 1
        elif action == 'Down' and r < 2:
            self.agent_pos[0] += 1
        elif action == 'Left' and c > 0:
            self.agent_pos[1] -= 1
        elif action == 'Right' and c < 2:
            self.agent_pos[1] += 1

class OptimalRandomStartAgent:
    def act(self, pos, grid):
        r, c = pos
        # 1. Si la casilla actual está sucia, limpia obligatoriamente
        if grid[r, c] == 1:
            return 'Suck'
        
        # 2. Buscar todas las casillas que siguen sucias en el entorno
        dirty_cells = [(i, j) for i in range(3) for j in range(3) if grid[i, j] == 1]
        
        if not dirty_cells:
            return 'Suck'
        
        # 3. Encontrar la casilla sucia más cercana usando distancia Manhattan
        closest_dirty = min(dirty_cells, key=lambda target: abs(r - target[0]) + abs(c - target[1]))
        target_r, target_c = closest_dirty
        
        # 4. Elegir el movimiento que reduzca la distancia al objetivo (camino más corto)
        possible_moves = []
        if target_r < r and r > 0: possible_moves.append(('Up', abs((r-1) - target_r) + abs(c - target_c)))
        if target_r > r and r < 2: possible_moves.append(('Down', abs((r+1) - target_r) + abs(c - target_c)))
        if target_c < c and c > 0: possible_moves.append(('Left', abs(r - target_r) + abs((c-1) - target_c)))
        if target_c > c and c < 2: possible_moves.append(('Right', abs(r - target_r) + abs((c+1) - target_c)))
        
        if possible_moves:
            # Ordenar por el menor costo resultante y retornar la mejor acción
            possible_moves.sort(key=lambda x: x[1])
            return possible_moves[0][0]
        
        return 'Suck'

# --- EJECUCIÓN ---
env = Environment3x3()
agent = OptimalRandomStartAgent()

env.render(0, "Inicio")

for paso in range(1, 20):
    action = agent.act(env.agent_pos, env.grid)
    env.execute(action)
    env.render(paso, action)
    
    if np.sum(env.grid) == 0:
        print(f"¡Entorno limpiado óptimamente desde posición aleatoria en {paso} pasos!")
        break

plt.ioff()
plt.show()