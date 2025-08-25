def decode_chromosome(chromosome, bits_per_project=4, num_projects=4):
    allocations = []
    for i in range(num_projects):
        start = i * bits_per_project
        end = start + bits_per_project
        part = chromosome[start:end]
        allocations.append(int(part, 2))
    return allocations

def fitness(chromosome, project_values, resource_limit):
    allocations = decode_chromosome(chromosome)
    total_resources = sum(allocations)
    if total_resources > resource_limit:
        return 0  # Invalid solution if resource limit exceeded
    value = sum(a * v for a, v in zip(allocations, project_values))
    return value

def print_table(population, fitness_values, prob_values, expected_output, actual_count, project_values):
    print(f"{'Chrom No':<8} | {'Chromosome (bin)':<18} | {'Allocations':<25} | {'Fitness (Value)':<15} | {'% Prob':<7} | {'Expected Count':<15} | {'Actual Count':<12}")
    print("-" * 110)
    for i, (chrom, fit, prob, exp, act) in enumerate(zip(population, fitness_values, prob_values, expected_output, actual_count)):
        allocations = decode_chromosome(chrom, bits_per_project=4, num_projects=len(project_values))
        alloc_str = ", ".join([f"P{idx+1}:{val}" for idx, val in enumerate(allocations)])
        print(f"{i:<8} | {chrom:<18} | {alloc_str:<25} | {fit:<15} | {prob*100:<7.2f} | {exp:<15.2f} | {act:<12}")

def selection(population, project_values, resource_limit):
    fitness_values = [fitness(ch, project_values, resource_limit) for ch in population]
    total_fitness = sum(fitness_values)
    max_fitness = max(fitness_values)
    avg_fitness = total_fitness / len(fitness_values) if fitness_values else 0

    if total_fitness == 0:
        # Avoid division by zero if all fitness are zero
        prob_values = [0 for _ in fitness_values]
        expected_output = [0 for _ in fitness_values]
    else:
        prob_values = [f / total_fitness for f in fitness_values]
        expected_output = [(f * len(population)) / total_fitness for f in fitness_values]

    actual_count = [round(val) for val in expected_output]

    print("\nResource Allocation Fitness Table:")
    print_table(population, fitness_values, prob_values, expected_output, actual_count, project_values)
    print(f"\nSum of Fitness (Total Value): {total_fitness}, Max Fitness: {max_fitness}, Avg Fitness: {avg_fitness:.2f}")

    return prob_values, expected_output, actual_count, max_fitness

def print_mating_pool(pool, title):
    print(f"\n{title}:")
    print(f"{'Chrom No':<8} | {'Chromosome (bin)':<18}")
    print("-" * 30)
    for i, chrom in enumerate(pool):
        print(f"{i:<8} | {chrom:<18}")

def mating_pool_selection(population, pool_size, bit_pos):
    mating_pool = population[:pool_size]

    print_mating_pool(mating_pool, f"Mating Pool before crossover at bit {bit_pos}")
    
    for i in range(0, pool_size - 1, 2):
        chrom1 = list(mating_pool[i])
        chrom2 = list(mating_pool[i + 1])                                         
        
        # Swap bit at bit_pos
        chrom1[bit_pos], chrom2[bit_pos] = chrom2[bit_pos], chrom1[bit_pos]
        
        mating_pool[i] = "".join(chrom1)
        mating_pool[i + 1] = "".join(chrom2)
    
    print_mating_pool(mating_pool, f"Mating Pool after crossover at bit {bit_pos}")

    new_population = population.copy()
    new_population[:pool_size] = mating_pool
    return new_population

def mutation(population, mutation_masks):
    print(f"\nMutation masks applied to chromosomes:")
    for i, mask in enumerate(mutation_masks):
        print(f"Chromosome {i}: {mask}")

    new_population = []
    for chrom, mask in zip(population, mutation_masks):
        chrom_list = list(chrom)
        for i, m in enumerate(mask):
            if m == '1':
                # Flip the bit
                chrom_list[i] = '1' if chrom_list[i] == '0' else '0'
        new_population.append("".join(chrom_list))

    print(f"Population after mutation: {new_population}")
    return new_population

def main():
    num_generations = 5                                                        
    num_chromosomes = 4
    bits_per_project = 4
    num_projects = 4
    chromosome_length = bits_per_project * num_projects
    resource_limit = 30
    project_values = [3, 5, 2, 7]

    population = [
        "0011001100110011",  # P1=3, P2=3, P3=3, P4=3
        "1111000000001111",  # P1=15, P2=0, P3=0, P4=15
        "0000111100001111",  # P1=0, P2=15, P3=0, P4=15
        "0000000011110111",  # P1=0, P2=0, P3=15, P4=7
    ]

    for gen in range(1, num_generations + 1):
        print(f"\n\n=== Generation {gen} ===")
        
        # 1. Selection and fitness calculation
        prob_values, expected_output, actual_count, max_fitness = selection(population, project_values, resource_limit)

        # 2. Crossover parameters
        pool_size = 4  # Using full population for mating
        bit_pos = gen % chromosome_length  # vary bit position each generation to mix more bits

        population = mating_pool_selection(population, pool_size, bit_pos)

        # 3. Mutation masks for each chromosome (example: flip bits in a pattern based on generation)
        mutation_masks = []
        for i in range(len(population)):
            # Just a sample mutation pattern: flip bit at (gen + i) % chromosome_length
            mask = ['0'] * chromosome_length
            flip_pos = (gen + i) % chromosome_length
            mask[flip_pos] = '1'
            mutation_masks.append("".join(mask))

        population = mutation(population, mutation_masks)

if __name__ == "__main__":
    main()





'''


=== Generation 1 ===

Resource Allocation Fitness Table:
Chrom No | Chromosome (bin)   | Allocations               | Fitness (Value) | % Prob  | Expected Count  | Actual Count
--------------------------------------------------------------------------------------------------------------
0        | 0011001100110011   | P1:3, P2:3, P3:3, P4:3    | 51              | 11.09   | 0.44            | 0           
1        | 1111000000001111   | P1:15, P2:0, P3:0, P4:15  | 150             | 32.61   | 1.30            | 1           
2        | 0000111100001111   | P1:0, P2:15, P3:0, P4:15  | 180             | 39.13   | 1.57            | 2           
3        | 0000000011110111   | P1:0, P2:0, P3:15, P4:7   | 79              | 17.17   | 0.69            | 1           

Sum of Fitness (Total Value): 460, Max Fitness: 180, Avg Fitness: 115.00

Mating Pool before crossover at bit 1:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011001100110011  
1        | 1111000000001111  
2        | 0000111100001111  
3        | 0000000011110111  

Mating Pool after crossover at bit 1:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0111001100110011  
1        | 1011000000001111  
2        | 0000111100001111  
3        | 0000000011110111  

Mutation masks applied to chromosomes:
Chromosome 0: 0100000000000000
Chromosome 1: 0010000000000000
Chromosome 2: 0001000000000000
Chromosome 3: 0000100000000000
Population after mutation: ['0011001100110011', '1001000000001111', '0001111100001111', '0000100011110111']


=== Generation 2 ===

Resource Allocation Fitness Table:
Chrom No | Chromosome (bin)   | Allocations               | Fitness (Value) | % Prob  | Expected Count  | Actual Count
--------------------------------------------------------------------------------------------------------------
0        | 0011001100110011   | P1:3, P2:3, P3:3, P4:3    | 51              | 16.89   | 0.68            | 1           
1        | 1001000000001111   | P1:9, P2:0, P3:0, P4:15   | 132             | 43.71   | 1.75            | 2           
2        | 0001111100001111   | P1:1, P2:15, P3:0, P4:15  | 0               | 0.00    | 0.00            | 0           
3        | 0000100011110111   | P1:0, P2:8, P3:15, P4:7   | 119             | 39.40   | 1.58            | 2           

Sum of Fitness (Total Value): 302, Max Fitness: 132, Avg Fitness: 75.50

Mating Pool before crossover at bit 2:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011001100110011  
1        | 1001000000001111  
2        | 0001111100001111  
3        | 0000100011110111  

Mating Pool after crossover at bit 2:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0001001100110011  
1        | 1011000000001111  
2        | 0001111100001111  
3        | 0000100011110111  

Mutation masks applied to chromosomes:
Chromosome 0: 0010000000000000
Chromosome 1: 0001000000000000
Chromosome 2: 0000100000000000
Chromosome 3: 0000010000000000
Population after mutation: ['0011001100110011', '1010000000001111', '0001011100001111', '0000110011110111']


=== Generation 3 ===

Resource Allocation Fitness Table:
Chrom No | Chromosome (bin)   | Allocations               | Fitness (Value) | % Prob  | Expected Count  | Actual Count
--------------------------------------------------------------------------------------------------------------
0        | 0011001100110011   | P1:3, P2:3, P3:3, P4:3    | 51              | 15.50   | 0.62            | 1           
1        | 1010000000001111   | P1:10, P2:0, P3:0, P4:15  | 135             | 41.03   | 1.64            | 2           
2        | 0001011100001111   | P1:1, P2:7, P3:0, P4:15   | 143             | 43.47   | 1.74            | 2           
3        | 0000110011110111   | P1:0, P2:12, P3:15, P4:7  | 0               | 0.00    | 0.00            | 0           

Sum of Fitness (Total Value): 329, Max Fitness: 143, Avg Fitness: 82.25

Mating Pool before crossover at bit 3:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011001100110011  
1        | 1010000000001111  
2        | 0001011100001111  
3        | 0000110011110111  

Mating Pool after crossover at bit 3:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0010001100110011  
1        | 1011000000001111  
2        | 0000011100001111  
3        | 0001110011110111  

Mutation masks applied to chromosomes:
Chromosome 0: 0001000000000000
Chromosome 1: 0000100000000000
Chromosome 2: 0000010000000000
Chromosome 3: 0000001000000000
Population after mutation: ['0011001100110011', '1011100000001111', '0000001100001111', '0001111011110111']


=== Generation 4 ===

Resource Allocation Fitness Table:
Chrom No | Chromosome (bin)   | Allocations               | Fitness (Value) | % Prob  | Expected Count  | Actual Count
--------------------------------------------------------------------------------------------------------------
0        | 0011001100110011   | P1:3, P2:3, P3:3, P4:3    | 51              | 29.82   | 1.19            | 1           
1        | 1011100000001111   | P1:11, P2:8, P3:0, P4:15  | 0               | 0.00    | 0.00            | 0           
2        | 0000001100001111   | P1:0, P2:3, P3:0, P4:15   | 120             | 70.18   | 2.81            | 3           
3        | 0001111011110111   | P1:1, P2:14, P3:15, P4:7  | 0               | 0.00    | 0.00            | 0           

Sum of Fitness (Total Value): 171, Max Fitness: 120, Avg Fitness: 42.75

Mating Pool before crossover at bit 4:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011001100110011  
1        | 1011100000001111  
2        | 0000001100001111  
3        | 0001111011110111  

Mating Pool after crossover at bit 4:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011101100110011  
1        | 1011000000001111  
2        | 0000101100001111  
3        | 0001011011110111  

Mutation masks applied to chromosomes:
Chromosome 0: 0000100000000000
Chromosome 1: 0000010000000000
Chromosome 2: 0000001000000000
Chromosome 3: 0000000100000000
Population after mutation: ['0011001100110011', '1011010000001111', '0000100100001111', '0001011111110111']


=== Generation 5 ===

Resource Allocation Fitness Table:
Chrom No | Chromosome (bin)   | Allocations               | Fitness (Value) | % Prob  | Expected Count  | Actual Count
--------------------------------------------------------------------------------------------------------------
0        | 0011001100110011   | P1:3, P2:3, P3:3, P4:3    | 51              | 10.71   | 0.43            | 0           
1        | 1011010000001111   | P1:11, P2:4, P3:0, P4:15  | 158             | 33.19   | 1.33            | 1           
2        | 0000100100001111   | P1:0, P2:9, P3:0, P4:15   | 150             | 31.51   | 1.26            | 1           
3        | 0001011111110111   | P1:1, P2:7, P3:15, P4:7   | 117             | 24.58   | 0.98            | 1           

Sum of Fitness (Total Value): 476, Max Fitness: 158, Avg Fitness: 119.00

Mating Pool before crossover at bit 5:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011001100110011  
1        | 1011010000001111  
2        | 0000100100001111  
3        | 0001011111110111  

Mating Pool after crossover at bit 5:
Chrom No | Chromosome (bin)  
------------------------------
0        | 0011011100110011  
1        | 1011000000001111  
2        | 0000110100001111  
3        | 0001001111110111  

Mutation masks applied to chromosomes:
Chromosome 0: 0000010000000000
Chromosome 1: 0000001000000000
Chromosome 2: 0000000100000000
Chromosome 3: 0000000010000000
Population after mutation: ['0011001100110011', '1011001000001111', '0000110000001111', '0001001101110111']

'''
