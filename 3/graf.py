import tkinter as tk
import math, heapq

# zmienne
FILE_NAME = "graf2.txt" 
n = 0
pos, coords, adj = {}, {}, {}

def load():
    global n, pos, coords, adj
    try:
        D = list(map(int, open(FILE_NAME).read().split()))
    except FileNotFoundError:
        info.config(text=f"Nie znaleziono pliku {FILE_NAME} w folderze z programem!")
        return

    n = D[0]
    pos, coords, adj, idx = {}, {}, {}, 1
    
    for i in range(1, n + 1):
        x, y = D[idx], D[idx+1]
        coords[i] = (x, y)
        pos[i] = (x * 40 + 20, y * 40 + 20)
        idx += 2
        
    for i in range(1, n + 1):
        adj[i] = D[idx+1 : idx+1+D[idx]]
        idx += D[idx] + 1
        
    s_var.set(f"{coords[1][0]},{coords[1][1]}")
    e_var.set(f"{coords[n][0]},{coords[n][1]}")
    draw()
    info.config(text=f"Wczytano {n} wierzchołków z pliku {FILE_NAME}.")

def get_node(text):
    try:
        x, y = map(int, text.replace(" ", "").split(','))
        for node_id, (cx, cy) in coords.items():
            if cx == x and cy == y: return node_id
    except: pass
    return None

def dist(a, b):
    return math.hypot(coords[a][0] - coords[b][0], coords[a][1] - coords[b][1])

def draw():
    if not pos: return
    c.delete("all")
    s, e = get_node(s_var.get()), get_node(e_var.get())
    
    for u, nxt_list in adj.items():
        for v in nxt_list:
            c.create_line(*pos[u], *pos[v], fill="gray")
            
    for u, (px, py) in pos.items():
        col = "green" if u == s else "red" if u == e else "blue"
        c.create_oval(px-6, py-6, px+6, py+6, fill=col)

def run(algo):
    s, e = get_node(s_var.get()), get_node(e_var.get())
    if not s or not e:
        info.config(text="Błędne współrzędne w polach Start/Cel!")
        return
        
    draw() 
    frontier, came_from, cost = [(0, s)], {s: None}, {s: 0}
    
    def step():
        if not frontier: 
            info.config(text="Brak ścieżki!")
            return
        _, curr = heapq.heappop(frontier)
        
        if curr == e:
            p = curr
            while came_from[p]:
                nxt = came_from[p]
                c.create_line(*pos[p], *pos[nxt], fill="red", width=3)
                p = nxt
            info.config(text=f"Znaleziono! Koszt: {cost[e]:.2f}")
            return
            
        if curr not in (s, e):
            px, py = pos[curr]
            c.create_oval(px-6, py-6, px+6, py+6, fill="orange")

        for nxt in adj[curr]:
            new_cost = cost[curr] + dist(curr, nxt)
            if nxt not in cost or new_cost < cost[nxt]:
                cost[nxt], came_from[nxt] = new_cost, curr
                h = dist(nxt, e)
                prio = h if algo == 'bfs' else new_cost if algo == 'dij' else new_cost + h
                heapq.heappush(frontier, (prio, nxt))
        c.after(50, step)
        
    step()

#interfejs
root = tk.Tk()
root.title("Pathfinder")

c = tk.Canvas(root, width=600, height=600, bg="white")
c.pack()
info = tk.Label(root, text="Kliknij 'Wczytaj', aby załadować wybrany graf")
info.pack()

f = tk.Frame(root)
f.pack()
tk.Button(f, text="Wczytaj", command=load).pack(side="left")

tk.Label(f, text="Start (x,y):").pack(side="left")
s_var = tk.StringVar()
tk.Entry(f, textvariable=s_var, width=5).pack(side="left")

tk.Label(f, text="Cel (x,y):").pack(side="left")
e_var = tk.StringVar()
tk.Entry(f, textvariable=e_var, width=5).pack(side="left")

tk.Button(f, text="Best First", command=lambda: run('bfs')).pack(side="left")
tk.Button(f, text="Dijkstra", command=lambda: run('dij')).pack(side="left")
tk.Button(f, text="A*", command=lambda: run('astar')).pack(side="left")

root.mainloop()
