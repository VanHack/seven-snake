import re
import time
import sys

#matrixA = ((5,1,5,7,3,8,5), (8,5,4,5,2,8,9), (1,8,7,4,2,5,9),
#           (4,7,5,2,1,4,8), (9,6,5,2,3,5,4), (7,8,5,4,1,2,6),
#           (3,2,1,4,5,8,7))
#matrixA = ((116, 122, 72, 24, 179, 121, 214, 246, 158, 211, 108, 182, 212, 198, 80),
#           (184, 171, 95, 45, 44, 55, 61, 148, 82, 129, 75, 105, 39, 120, 8),
#           (70, 145, 119, 22, 253, 202, 2, 245, 74, 18, 237, 234, 51, 47, 254),
#           (252, 69, 17, 78, 188, 216, 89, 7, 222, 251, 31, 144, 137, 132, 32),
#           (153, 29, 230, 25, 92, 103, 203, 225, 166, 200, 62, 176, 6, 9, 126),
#           (149, 238, 151, 109, 123, 239, 76, 218, 107, 199, 133, 157, 227, 84, 250),
#           (124, 205, 191, 13, 43, 141, 247, 106, 140, 41, 136, 220, 71, 231, 102),
#           (178, 49, 208, 143, 232, 94, 23, 167, 248, 192, 168, 66, 37, 27, 210),
#           (165, 159, 97, 86, 152, 213, 34, 160, 193, 12, 52, 169, 11, 127, 83),
#           (243, 134, 206, 183, 139, 40, 235, 104, 118, 187, 63, 100, 28, 57, 131),
#           (128, 164, 33, 93, 19, 4, 194, 59, 77, 35, 154, 201, 186, 229, 10),
#           (130, 174, 233, 99, 87, 241, 50, 81, 135, 177, 21, 189, 150, 255, 224),
#           (42, 221, 15, 172, 58, 16, 170, 190, 1, 180, 101, 112, 226, 14, 114),
#           (20, 215, 85, 185, 3, 209, 142, 161, 113, 5, 88, 56, 196, 98, 38),
#           (125, 91, 228, 207, 79, 181, 60, 217, 236, 65, 147, 117, 219, 163, 73))

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
        find_snakes((posX,posY), snake_size, acc, path)

    ## Check Bottom
    posX = start[0]+1
    posY = start[1]
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes((posX,posY), snake_size, acc, path)

    ## Check Top
    posX = start[0]-1
    posY = start[1]
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes((posX,posY), snake_size, acc, path)

    ## Check Left
    posX = start[0]
    posY = start[1]-1
    aux_pos = (posX,posY)
    if aux_pos not in path and check_inside((posX, posY)):
        find_snakes((posX,posY), snake_size, acc, path)

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
