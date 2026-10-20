import sys
import time
import os

# slownik ruchow
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

# sciezka mapki
if len(sys.argv) > 1:
    plik_mapy = sys.argv[1]
else:
    plik_mapy = input("Podaj nazwę pliku z mapą (np. maze1.txt): ")

# czytanie mapki
try:
    with open(plik_mapy, 'r', encoding='utf-8') as f:
        mapa = [list(linia.strip('\n')) for linia in f]
except FileNotFoundError:
    print("Nie znaleziono pliku.")
    sys.exit(1)

max_szer = max(len(w) for w in mapa)
mapa = [w + [' '] * (max_szer - len(w)) for w in mapa]

# mapka
for wiersz in mapa:
    print("".join(wiersz))
    
max_w = len(mapa) - 1
max_k = max_szer - 1
print(f"Maksymalny dozwolony wiersz: {max_w}")
print(f"Maksymalna dozwolona kolumna: {max_k}")
print(f"--------------------------")

# input
print("\nPodaj współrzędne w formacie: wiersz, kolumna (liczone od 0)")
start_in = input("Współrzędne startowe: ").split(',')
koniec_in = input("Współrzędne końcowe: ").split(',')

start = (int(start_in[0].strip()), int(start_in[1].strip()))
koniec = (int(koniec_in[0].strip()), int(koniec_in[1].strip()))

algorytm = input("Rodzaj algorytmu (BFS / DFS): ").strip().upper()

# Zmienne do przeszukiwania
struktura = [start]
odwiedzone = set()
# slownik krokow
kroki = {start: 0} 

# glowna
while struktura:
    y, x = struktura.pop() if algorytm == "DFS" else struktura.pop(0)
    
    if (y, x) in odwiedzone:
        continue
        
    odwiedzone.add((y, x))

    #mapa i kolorowanie
    os.system('cls' if os.name == 'nt' else 'clear')
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

    # koniec
    if (y, x) == koniec:
        #dystans out
        print(f"\nZnaleziono ścieżkę! Ilość kroków: {kroki[(y, x)]}")
        break

    # sąsiedzi do sprawdzeniaa
    for dy, dx in RUCHY.get(mapa[y][x], []):
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(mapa) and 0 <= nx < len(mapa[0]):
            if (ny, nx) not in odwiedzone and (ny, nx) not in struktura:
                struktura.append((ny, nx))
                kroki[(ny, nx)] = kroki[(y, x)] + 1
else:
    print(f"\nBrak ścieżki!")
