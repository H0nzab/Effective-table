import math
import random
import re
import time
import os

def clean_lorem_ipsum(filename="lorem_ipsum.txt"):
    """
    Načte text ze souboru a odstraní z něj značky jako ''.
    """
    if not os.path.exists(filename):
        print(f"POZOR: Soubor {filename} nebyl nalezen. Používám záložní text.")
        return "Lorem ipsum dolor sit amet."
        
    with open(filename, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    # Odstranění prefixů "" pomocí regulárního výrazu
    clean_text = re.sub(r'\\s*', '', raw_text)
    # Odstranění přebytečných mezer a zalomení řádků
    clean_text = clean_text.replace('\n', ' ').strip()
    return clean_text

def generate_variations(num_variations=150, fuzziness=1.0):
    """
    Tvůj původní generátor tabulek rozložený do matice 8x8 (64 znaků).
    """
    chars = (
        [' '] * 5 +
        ['u'] * 3 + ['i'] * 3 + ['e'] * 3 + ['a'] * 3 +
        ['q'] * 2 + ['n'] * 2 + ['s'] * 2 + ['l'] * 2 + ['t'] * 2 +
        ['r'] * 2 + ['o'] * 2 + ['m'] * 2 + ['c'] * 2 + ['d'] * 2 +
        list(".vpgbChjfAPVNMwIQSDEJLUFTOR")
    )

    unique_strings = set()
    attempts = 0
    max_attempts = num_variations * 10

    while len(unique_strings) < num_variations and attempts < max_attempts:
        grid_positions = []
        for row in range(8):
            for col in range(8):
                base_dist = math.sqrt((row - 3.5)**2 + (col - 3.5)**2)
                noise = random.uniform(-fuzziness, fuzziness)
                fuzzed_dist = base_dist + noise
                grid_positions.append((fuzzed_dist, row * 8 + col))
        
        grid_positions.sort()
        sorted_target_indices = [idx for dist, idx in grid_positions]

        result_array = [None] * 64
        for i in range(64):
            result_array[sorted_target_indices[i]] = chars[i]
            
        variation_string = "".join(result_array)
        unique_strings.add(variation_string)
        attempts += 1

    return list(unique_strings)

def calculate_min_presses(grid_string, text, width=8, height=8):
    """
    Dynamické programování pro nalezení minimálního počtu stisků kláves.
    Vrací celkovou "cenu" (počet posunů šipek + stisky Enter) za napsání textu.
    """
    # 1. Zmapování pozic všech znaků v tabulce
    char_positions = {}
    for i, char in enumerate(grid_string):
        r, c = divmod(i, width)
        if char not in char_positions:
            char_positions[char] = []
        char_positions[char].append((r, c))

    # 2. Inicializace stavů: klíč = (řádek, sloupec), hodnota = dosavadní stisky
    # Začínáme v levém horním rohu (0, 0)
    current_states = {(0, 0): 0}

    # 3. Průchod textem
    for char in text:
        if char not in char_positions:
            continue  # Ignorujeme znaky, které nejsou vůbec v tabulce

        next_positions = char_positions[char]
        next_states = {}

        # Pro každou možnou pozici aktuálního znaku najdeme nejlevnější cestu
        for r2, c2 in next_positions:
            min_cost = float('inf')
            
            for (r1, c1), current_cost in current_states.items():
                # Manhattanská vzdálenost + 1 za stisk Enter
                dist = abs(r1 - r2) + abs(c1 - c2)
                cost = current_cost + dist + 1
                
                if cost < min_cost:
                    min_cost = cost
                    
            next_states[(r2, c2)] = min_cost

        current_states = next_states

    # 4. Výběr absolutního minima na konci
    if not current_states:
        return 0
        
    return min(current_states.values())

def main():
    print("Načítám a čistím text z lorem_ipsum.txt...")
    text = clean_lorem_ipsum("lorem_ipsum.txt")
    print(f"Délka psaného textu (po vyčištění): {len(text)} znaků.\n")

    počet_tabulek = 1000
    print(f"Generuji {počet_tabulek} unikátních tabulek...")
    start_time = time.time()
    tabulky = generate_variations(num_variations=počet_tabulek, fuzziness=1.2)
    print(f"Vygenerováno za {time.time() - start_time:.2f} s.\n")

    print("Spouštím vyhodnocování...")
    best_score = float('inf')
    best_grid = ""
    
    start_time = time.time()
    for i, grid in enumerate(tabulky):
        score = calculate_min_presses(grid, text)
        
        if score < best_score:
            best_score = score
            best_grid = grid
            print(f"[{i+1}/{počet_tabulek}] Nové minimum nalezeno: {best_score} stisků")

    print("\n" + "="*50)
    print("HOTOVO!")
    print(f"Vyhodnocení trvalo {time.time() - start_time:.2f} s.")
    print(f"Nejlepší nalezené skóre: {best_score}")
    print("Nejlepší tabulka (64 znaků čtených po řádcích):")
    print(best_grid)
    print("="*50)
    
    # Pro lepší čitelnost si tu nejlepší tabulku vytiskneme jako 8x8 mřížku
    print("\nZobrazení tabulky ve formátu 8x8:")
    for row in range(8):
        print(best_grid[row*8 : (row+1)*8])

if __name__ == "__main__":
    main()