# ---------- GRID LAYOUT ----------

def create_grid():
    grid = [
        ['.', 'S1', 'S2', 'S3', '.'],  # row 0 
        ['.', '.',  '.',  '.',  '.'],  # row 1
        ['L', '.',  'R',  '.',  '.'],  # row 2  
        ['.', '.',  '.',  '.',  '.'],  # row 3
        ['.', 'S4', 'S5', 'S6', '.']   # row 4
    ]
    return grid


def print_grid(grid):
    print()
    print(" --- GRID LAYOUT ---")
    print()
    
    # top numbers
    print("   ", end="")
    for j in range(len(grid)):
        print(f"{j:<3}", end="")
    print()

    # grid
    for i in range(len(grid)):
        print(f"{i:<3}", end="")
        for j in range(len(grid)):
            print(f"{grid[i][j]:<3}", end="")
        print()
    
    print()


# ---------- LOCATE IMPORTANT LOCATIONS ----------

def get_robot_position(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 'R':      # robot srtat postion is marked with 'R' in the grid
                return (x, y)
    return None


def get_load_position(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 'L':      # loading dock position is marked with 'L' in the grid
                return (x, y)
    return None


# ---------- TAKE USER DEFINED TASKS ----------

def get_tasks():
    valid_locations = [(0, 1), (0, 2), (0, 3), (4, 1), (4, 2), (4, 3)]
    shelf_names = {
        (0, 1): 'S1', (0, 2): 'S2', (0, 3): 'S3',
        (4, 1): 'S4', (4, 2): 'S5', (4, 3): 'S6'
    }

    tasks = []

    while True:
        try:
            num_tasks = int(input("Enter the number of tasks (1-3): "))
            if 1 <= num_tasks <= 3:
                break
            print("Please enter a number between 1 and 3.")
        except ValueError:                                                      # ValueError -> wrong value // TypeError -> wrong type // IndexError -> out of bounds // except would catch all errors
            print("Invalid input. Enter a number.")

    for i in range(num_tasks):
        print(f"\n--- Task {i + 1} ---")

        task_id = input(f"Enter ID for item {i + 1}: ")
        name = input(f"Enter name for item {i + 1}: ")

        print("Valid shelf locations:")
        for pos, label in shelf_names.items():                    # we want both keys and the values accocaited with it else we would just do .values() or .keys() 
            print(f"  {label}: row {pos[0]}, col {pos[1]}")

        while True:
            try:
                x = int(input(f"Enter row for item {i + 1}: "))
                y = int(input(f"Enter column for item {i + 1}: "))
                if (x, y) in valid_locations:
                    break
                print(f"Invalid location. Choose from: {list(shelf_names.values())}")
            except ValueError:
                print("Invalid input. Enter numbers only.")

        tasks.append({
            "id": task_id,
            "name": name,        
            "location": (x, y)   # tuple (x, y) to represent the location of the shelf for this task
       })

    return tasks


# ---------- PERMUTATIONS ----------

def generate_permutations(tasks):
    if len(tasks) == 1:
        return [tasks]

    result = []
    for i in range(len(tasks)):
        current = tasks[i]
        remaining = tasks[:i] + tasks[i + 1:]
        for order in generate_permutations(remaining):
            result.append([current] + order)
    return result


# ---------- DISTANCE & COST & BEST ORDER ----------

def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def calculate_cost(orders, start, load_pos):
    cost = 0
    current = start    # start postion of the robot

    for task in orders:
        shelf = task["location"]
        cost += manhattan_distance(current, load_pos)  # robot -> loading dock
        cost += manhattan_distance(load_pos, shelf)    # loading dock -> shelf
        current = shelf  # update start position for next iteration to be the current shelf

    return cost 


def find_best_order(tasks, robot_pos, load_pos):
    
    perms = generate_permutations(tasks)
    best_order = None
    best_cost = float("inf")  # large number to start with so that any real cost will be smaller than it

    for order in perms:
        cost = calculate_cost(order, robot_pos, load_pos)
        if cost < best_cost:
            best_cost = cost
            best_order = order
    
    print(f"\nBest order: {[t['id'] for t in best_order]} -> cost: {best_cost}") 

    return best_order, best_cost


# ---------- SIMULATE ----------

def simulate_route(best_order, robot_pos, load_pos):
    print("\n--- Route Simulation ---")
    current = robot_pos
    total = 0

    for task in best_order:
        shelf = task["location"]
        d1 = manhattan_distance(current, load_pos)
        d2 = manhattan_distance(load_pos, shelf)

        print(f"\n----- Task: {task['id']} - Name: {task['name']} -----") # task info
        print(f"Robot position: {current} -> Loading dock: {load_pos} | Distance:({d1})") # robot to loading dock
        print(f"Loading dock: {load_pos} -> Shelf position: {shelf} | Distance:({d2})") # loading dock to shelf

        total += d1 + d2
        current = shelf  # update current position for next iteration
    
    print()    
    print(f"Total Distance Traveled: {total}")

    

# ---------- MAIN ----------

def main():
    # create and display the grid
    grid = create_grid()
    print_grid(grid)

    # ensure robot and loading dock are present in the grid
    robot_pos = get_robot_position(grid)
    if robot_pos is None:
        print("Error: Robot (R) not found in grid.")
        return

    load_pos = get_load_position(grid)
    if load_pos is None:
        print("Error: Loading dock (L) not found in grid.")
        return

    # give user info on robot and loading dock positions
    print(f"Robot starting position: {robot_pos}")
    #print(f"Loading dock (L): {load_pos}") # for testing 

    # get user defined tasks
    tasks = get_tasks()

    # task permutations
    perms = generate_permutations(tasks)

    #calculate and display cost for each permutation
    print("\n--- All Permutations & Costs ---")
    for p in perms:
        ids = [t["id"] for t in p]
        cost = calculate_cost(p, robot_pos, load_pos)
        print(f"  {ids}  ->  cost: {cost}")

    best_order, best_cost = find_best_order(tasks, robot_pos, load_pos)

    simulate_route(best_order, robot_pos, load_pos)


if __name__ == "__main__":
    main()