import random

#dane(sily zawodnikow)
values = [12, 7, 9, 5, 11, 4, 8, 14,12] 
N = len(values)

total_sum = sum(values)
target_diff = total_sum % 2 

POP_SIZE = 50
MAX_ITER = 1000

def fitness(genome):
    sum_0 = sum(values[i] for i in range(N) if genome[i] == 0) #listy druzyn
    sum_1 = sum(values[i] for i in range(N) if genome[i] == 1)
    return abs(sum_0 - sum_1)

#losowanie
population = [[random.choice([0, 1]) for _ in range(N)] for _ in range(POP_SIZE)]

print(f"N = {N}")
print(f"Totalna suma: {total_sum} | Różnica docelowa: {target_diff}\n")

#petla
for gen in range(1, MAX_ITER + 1):
    
    #selekcja
    population.sort(key=fitness) 
    best_genome = population[0]
    min_diff = fitness(best_genome)
    
    print(f"Iteracja: {gen} | Minimalna różnica: {min_diff}")
    
    #kryteria
    if min_diff == target_diff:
        print(f"Iteracja: {gen} - Odnaleziono rozwiązanie!")
        print(f"Lista: {', '.join(map(str, best_genome))}\n")
        
        subset_0 = [values[i] for i in range(N) if best_genome[i] == 0]
        subset_1 = [values[i] for i in range(N) if best_genome[i] == 1]
        print(f"Drużyna 0: {subset_0} -> Sum: {sum(subset_0)}")
        print(f"Drużyna 1: {subset_1} -> Sum: {sum(subset_1)}")
        break
        
    next_gen = []
    
    #krzyzowanie i mutacje
    for _ in range(POP_SIZE // 2):
        #rodzice
        p1 = random.choice(population[:POP_SIZE//2])
        p2 = random.choice(population[:POP_SIZE//2])
        
        #dzieci
        split_pt = random.randint(1, N - 1)
        c1 = p1[:split_pt] + p2[split_pt:]
        c2 = p2[:split_pt] + p1[split_pt:]
        
        #mutacje
        if random.random() < 0.2:
            idx = random.randint(0, N-1)
            c1[idx] = 1 - c1[idx]
        if random.random() < 0.2:
            idx = random.randint(0, N-1)
            c2[idx] = 1 - c2[idx]
            
        next_gen.extend([c1, c2])
        
    #wybor najlepszych
    population.extend(next_gen)
    population.sort(key=fitness)
    population = population[:POP_SIZE]

else:
    print(f"Max iteracji. Najlepsza różnica: {min_diff}")
