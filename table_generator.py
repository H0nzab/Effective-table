import math

def generate_optimized_table_string():
    chars = (
        [' '] * 5 +                                # mezery
        ['u'] * 3 + ['i'] * 3 +                    # 'u' a 'i' pro 'quis' a 'nulla'
        ['e'] * 3 + ['a'] * 3 +                    # Hlavní samohlásky
        ['q'] * 2 + ['n'] * 2 +                    # 'q' k 'u' a 'n' k 'u'
        ['s'] * 2 + ['l'] * 2 + ['t'] * 2 +        # Častí sousedé
        ['r'] * 2 + ['o'] * 2 + ['m'] * 2 +        
        ['c'] * 2 + ['d'] * 2 +
        list(".vpgbChjfAPVNMwIQSDEJLUFTOR")         # Ostatní 
    )

    grid_positions = []
    for row in range(8):
        for col in range(8):
            dist = math.sqrt((row - 3.5)**2 + (col - 3.5)**2)
            grid_positions.append((dist, row * 8 + col))
    
    grid_positions.sort()
    sorted_target_indices = [idx for dist, idx in grid_positions]

    result_array = [None] * 64
    for i in range(64):
        target_idx = sorted_target_indices[i]
        result_array[target_idx] = chars[i]
        
    return "".join(result_array)

if __name__ == "__main__":
    final_string = generate_optimized_table_string()
    print(final_string)
    print(f"\nKontrola délky: {len(final_string)} znaků")