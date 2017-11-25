import re
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
def check_inside(posXY):
    if posXY[0] < len(matrixA) and posXY[0] >= 0 and posXY[1] < len(matrixA[0]) and posXY[1] >= 0:
        return True
    else:
        return False

## Find all snakes using a recursive algorithm
def find_snakes_recursive(start, snake_size, acc, path):
    acc += matrixA[start[0]][start[1]]
    path = path + [(start[0],start[1])]
    #path += str(start[0]) + "," + str(start[1]) + "; "
    snake_size += 1
    if snake_size >= snake_max_size:
        result_list.append((acc, path))
        return True

    ## Check Right
    posX = start[0]
    posY = start[1]+1
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

    ## Check Bottom
    posX = start[0]+1
    posY = start[1]
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

    ## Check Top
    posX = start[0]-1
    posY = start[1]
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

    ## Check Left
    posX = start[0]
    posY = start[1]-1
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes_recursive((posX,posY), snake_size, acc, path)

## Find pairs with same value
def look_for_pair(results):
    while results:
        head_value = results[0][0]
        pairs = [result[1] for result in results if result[0] == head_value]
        results = results[len(pairs):]
        snake1, snake2 = check_distinct_pair(pairs)
        if snake1 and snake2:
            print(head_value)
            print(snake1)
            print(snake2)
            return
    print("FAIL")
            
## See if snake is different than others with same value
def check_distinct_pair(pairs):
    for i in range(len(pairs)):
        for j in range(i+1, len(pairs)):
            dif_cells = 0
            for cell in pairs[i]:
                if cell not in pairs[j]:
                    dif_cells += 1
            if dif_cells == 7:
                return pairs[i], pairs[j]
    return [], []

if __name__ == "__main__":

    sys.argv = 'SevenSnake.py', 'D:\\matrix20.csv'
    if len(sys.argv) != 2:
        print("Correct usage: 'python SevenSnake.py csv_full_path.csv'")
        
    else:
        start_time = time.time()
        load_csv(sys.argv[1])
        end_time = time.time()
        #print("Time to load file: " + str(end_time-start_time))

        start_time = time.time()
        for i in range(len(matrixA)):
            for j in range(len(matrixA[0])):
                find_snakes_recursive((i,j), 0, 0, list())
        end_time = time.time()
        #print("Snake generation time: " + str(end_time-start_time))

        start_time = time.time()
        result_list.sort(key=lambda x: x[0])
        end_time = time.time()
        #print("Sorting time: " + str(end_time-start_time))

        start_time = time.time()
        look_for_pair(result_list)
        end_time = time.time()
        #print("Looking for a pair time: " + str(end_time-start_time))

        #print(result_list)
        #print("Results Size: " + str(len(result_list)))
