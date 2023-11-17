from Cache import Cache

class text_colors:
    HEADER =    '\033[95m'
    BLUE =      '\033[94m'
    CYAN =      '\33[96m'
    GREEN =     '\33[92m'
    YELLOW =    '\33[93m'
    RED =       '\033[91m'
    END_C =     '\033[0m'
    BOLD =      '\033[1m'
    UNDERLINE = '\033[4m'

workload = ""
total_access = 0

cache_size = 0
cache_block_size = 0
cache_associativity = 0
cache = 0

if __name__ == "__main__":
    cache_size = int(input("Cache Size (KB):")) * 1024
    cache_block_size = int(input("Cache block Size (B):"))
    cache_associativity = int(input("Cache associativity:"))
    cache_replacement_policy = input("Replacement policy ([LRU], NMRU, Random):")
    cache = Cache(cache_size, cache_block_size, cache_associativity, cache_replacement_policy)

    workload = input("workload:")
    total = 0

    with open(workload, "rb") as f:
        total = sum(1 for _ in f)
    
    print(f"\nstart simulation    ")
    index = 1
    data = []
    old_percent = -1
    f = open(workload, "r")
    line = f.readline()
    while line:
        addr = int(line.split(' ')[1], 16)
        cache.access(addr)
        line = f.readline()
        percent = int((index*50)/total)
        if percent != old_percent:
            print(" [", end="")
            if percent < 16:
                print(text_colors.RED, end="")
            elif percent < 40:
                print(text_colors.YELLOW, end="")
            else:
                print(text_colors.GREEN, end="")
            print(f"{'='*percent}{text_colors.END_C}{' '*(50 - percent)}] {percent*2}%", end='\r')
            old_percent = percent
        index += 1
    print()
    cache.printFinallyState()