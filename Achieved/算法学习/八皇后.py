def is_safe(map, row, col: int, number_of_queens) -> bool:
    # 检查同一列是否有皇后
    for i in range(row):
        if map[i][col] == 'Q':
            return False

    # 检查左上对角线是否有皇后
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if map[i][j] == 'Q':
            return False
        i -= 1
        j -= 1

    # 检查右上对角线是否有皇后
    i, j = row - 1, col + 1
    while i >= 0 and j < number_of_queens:
        if map[i][j] == 'Q':
            return False
        i -= 1
        j += 1

    return True

def backtrack(map, row, number_of_queens):
    if row == number_of_queens:
        # 找到一个有效解，将其添加到结果中
        solutions.append([''.join(row) for row in map])
        return

    for col in range(number_of_queens):
        if is_safe(map, row, col, number_of_queens):
            map[row][col] = 'Q'
            backtrack(map, row + 1, number_of_queens)
            map[row][col] = '.'

# 递推方式求解八皇后问题
def solve_n_queens_iterator(number_of_queens):
    board = [['.' for _ in range(number_of_queens)] for _ in range(number_of_queens)]
    stack = [(0, 0)]
    while stack:
        row, col = stack.pop()
        if row == number_of_queens:
            solutions.append([''.join(row) for row in board])
            continue
        for c in range(col, number_of_queens):
            if is_safe(board, row, c, number_of_queens):
                board[row][c] = 'Q'
                stack.append((row + 1, 0))
                break
        else:
            if row == 0:
                break
            row -= 1
            col = number_of_queens
        if row < number_of_queens:
            continue
        for i in range(number_of_queens):
            board[row][i] = '.'
        row -= 1
        col += 1
    return solutions

def solve_n_queens(number_of_queens):
    board = [['.' for _ in range(number_of_queens)] for _ in range(number_of_queens)]
    backtrack(board, 0, number_of_queens)
    return solutions

# 调用函数并打印结果
solutions = []
#solutions = solve_n_queens(8)
solutions = solve_n_queens_iterator(8)
print(f"找到了 {len(solutions)} 个解:")
for i, solution in enumerate(solutions):
    print(f"解{i+1}:")
    for row in solution:
        print(row)
    print()