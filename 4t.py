import copy

with open('input.txt', 'r') as file:
    sudoku = file.readlines()
sudoku = [[int(elem) for elem in x.split()] for x in sudoku]

#Создание класса с функциями решения и вспомогательного решения

class Solver:
    def solve(sudoku):
        solution = copy.deepcopy(sudoku) #Копирование поля
        if Solver.solveHelp(solution): #Если решение есть
            return solution
        return None

    def solveHelp(solution): #Вспомогательное решение
        minPosValCountCell = None
        while True:
            minPosValCountCell = None
            for rowIndex in range(9):
                for columnIndex in range(9):
                    if solution[rowIndex][columnIndex] != 0:
                        continue
                    posVal = Solver.findPosVal(rowIndex, columnIndex, solution)
                    posValCount = len(posVal)
                    if posValCount == 0:
                        return False
                    if posValCount == 1:
                        solution[rowIndex][columnIndex] = posVal.pop()
                    if not minPosValCountCell or \
                       posValCount < len(minPosValCountCell[1]):
                        minPosValCountCell = ((rowIndex, columnIndex), posVal)
            if not minPosValCountCell:
                return True
            elif 1 < len(minPosValCountCell[1]):
                break
        i, j = minPosValCountCell[0]
        for v in minPosValCountCell[1]:
            solutionCopy = copy.deepcopy(solution)
            solutionCopy[i][j] = v
            if Solver.solveHelp(solutionCopy):
                for i in range(9):
                    for j in range(9):
                        solution[i][j] = solutionCopy[i][j]
                return True
        return False

# Функция, возвращающая необходимые цифры, после проверки на уникальность

    def findPosVal(rowIndex, columnIndex, sudoku):
        values = {v for v in range(1, 10)}
        values -= Solver.getRow(rowIndex, sudoku)
        values -= Solver.getColumn(columnIndex, sudoku)
        values -= Solver.getBlock(rowIndex, columnIndex, sudoku)
        return values

#Проверка на уникальность по строке

    def getRow(rowIndex, sudoku):
        return set(sudoku[rowIndex][:])

#Проверка на уникальность по столбцу

    def getColumn(columnIndex, sudoku):
        return {sudoku[i][columnIndex] for i in range(9)}

#Проверка на уникальность по блоку 3x3

    def getBlock(rowIndex, columnIndex, sudoku):
        blockRowStart = 3 * (rowIndex // 3)
        blockColumnStart = 3 * (columnIndex // 3)
        return {
            sudoku[blockRowStart + i][blockColumnStart + j]
                for i in range(3)
                for j in range(3)
        }


#Функция вывода матрицы

def printsudoku(sudoku):
    for row in sudoku:
        print(row)


printsudoku(sudoku)
print()

solution = Solver.solve(sudoku)
if solution: printsudoku(solution)

with open("output.txt", "w") as file:
    file.write('\n'.join(' '.join(str(j) for j in i) for i in solution))


    