import time

RUCHY = {
    '\u253C': [(-1,0), (1,0), (0,-1), (0,1)], 
    '\u2502': [(-1,0), (1,0)],                
    '\u2500': [(0,-1), (0,1)],                
    '\u2510': [(1,0), (0,-1)],                
    '\u2518': [(-1,0), (0,-1)],               
    '\u2514': [(-1,0), (0,1)],                
    '\u250C': [(1,0), (0,1)],                 
    '\u2524': [(-1,0), (1,0), (0,-1)],        
    '\u2534': [(-1,0), (0,-1), (0,1)],        
    '\u251C': [(-1,0), (1,0), (0,1)],         
    '\u252C': [(1,0), (0,-1), (0,1)],         
    '\u2575': [(-1,0)],                       
    '\u2577': [(1,0)],                        
    '\u2574': [(0,-1)],                       
    '\u2576': [(0,1)],                        
    '\u0020': []                              
}

plik_mapy = "maze1.txt"
start, koniec = (0, 0), (19, 19) 
algorytm = "DFS" 

with open(plik_mapy, 'r', encoding='utf-8') as f:
    mapa = [list(linia.strip('\n')) for linia in f]
max_szer = max(len(w) for w in mapa)
mapa = [w + [' '] * (max_szer - len(w)) for w in mapa]

struktura = [start]
odwiedzone = set()
kroki = 0

while struktura:
    y, x = struktura.pop() if algorytm == "DFS" else struktura.pop(0)
    odwiedzone.add((y, x))
    kroki += 1

    print("\033[H\033[J", end="") 
    for i, wiersz in enumerate(mapa):
        for j, znak in enumerate(wiersz):
            poz = (i, j)
            if poz == start:        kolor = '\033[1;31m' 
            elif poz == koniec:     kolor = '\033[1;34m' 
            elif poz in odwiedzone: kolor = '\033[1;32m' 
            elif poz in struktura:  kolor = '\033[1;33m' 
            else:                   kolor = '\033[0m'    
            
            print(f"{kolor}{znak}\033[0m", end="")
        print()
    
    time.sleep(0.1) 

    if (y, x) == koniec:
        print(f"\nZnaleziono ścieżkę! Ilość kroków: {kroki}")
        break

    for dy, dx in RUCHY.get(mapa[y][x], []):
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(mapa) and 0 <= nx < len(mapa[0]):
            if (ny, nx) not in odwiedzone and (ny, nx) not in struktura:
                struktura.append((ny, nx))
else:
    print(f"\nBrak ścieżki! Ilość kroków: {kroki}")