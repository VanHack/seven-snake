import time
import sys

matrixA = list()
result_list = list()

snake_max_size = 7

## Load the csv file into matrixA
def load_csv(path_to_file):
    global matrixA
    with open(path_to_file) as f:
        for line in f:
            matrixA.append(tuple(map(int, line.split(","))))

## See if cell is inside matrix boundaries
def check_inside(cell):
    if cell[0] < len(matrixA) and cell[0] >= 0 and cell[1] < len(matrixA[0]) and cell[1] >= 0:
        return True
    else:
        return False

def check_adjacency(path, cell):
    ## If a "Square" is made in the snake, that snake will be invalid because at least 1 cell will have adjacency > 2
    ## Bottom Right Square
    if (cell[0],cell[1]+1) in path and (cell[0]+1,cell[1]+1) in path and (cell[0]+1,cell[1]) in path:
        return False
    ## Top Right Square
    if (cell[0],cell[1]+1) in path and (cell[0]-1,cell[1]+1) in path and (cell[0]-1,cell[1]) in path:
        return False
    ## Bottom Left Square
    if (cell[0]+1,cell[1]) in path and (cell[0]+1,cell[1]-1) in path and (cell[0],cell[1]-1) in path:
        return False
    ## Top Left Square
    if (cell[0],cell[1]-1) in path and (cell[0]-1,cell[1]-1) in path and (cell[0]-1,cell[1]) in path:
        return False
    return True

## Find all snakes using a recursive algorithm
def find_snakes_recursive(start, snake_size, acc, path):
    acc += matrixA[start[0]][start[1]]
    path = path + [(start[0],start[1])]
    snake_size += 1
    if snake_size >= snake_max_size:
        result_list.append((acc, path))
        return

    ## Check Right
    posX = start[0]
    posY = start[1]+1
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)) and check_adjacency(path, (posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

    ## Check Bottom
    posX = start[0]+1
    posY = start[1]
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)) and check_adjacency(path, (posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

    ## Check Top
    posX = start[0]-1
    posY = start[1]
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)) and check_adjacency(path, (posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

    ## Check Left
    posX = start[0]
    posY = start[1]-1
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)) and check_adjacency(path, (posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

## Find pairs with same value
def look_for_pair(results):
    while results:
        head_value = results[0][0]
        pairs = [result[1] for result in results if result[0] == head_value]
        results = results[len(pairs):]
        snake1, snake2 = check_distinct_pair(pairs)
        if snake1 and snake2:
            print("Snake Value: " + str(head_value))
            print(snake1)
            print(snake2)
            return
    print("FAIL")

## See if snake is different than others with same value
def check_distinct_pair(pairs):
    for i, _ in enumerate(pairs):
        for j in range(i+1, len(pairs)):
            dif_cells = 0
            for cell in pairs[i]:
                if cell not in pairs[j]:
                    dif_cells += 1
                else:
                    break
            if dif_cells == 7:
                return pairs[i], pairs[j]
    return [], []

if __name__ == "__main__":
    #sys.argv = 'SevenSnake.py', 'D:\\matrix100.csv'
    if len(sys.argv) != 2:
        print("Correct usage: 'python SevenSnake.py csv_full_path.csv'")

    else:
        load_csv(sys.argv[1])
        for i in range(len(matrixA)):
            for j in range(len(matrixA[0])):
                find_snakes_recursive((i,j), 0, 0, list())
        result_list.sort(key=lambda x: x[0])
        look_for_pair(result_list)
