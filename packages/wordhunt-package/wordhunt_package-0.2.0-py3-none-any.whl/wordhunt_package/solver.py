from .english import create_english_list, restore_trie

class Solver:


    def __init__(self, matrix_string, length=4, width=4):
        if len(matrix_string) != length * width or not matrix_string.isalnum():
            raise ValueError("Invalid input string")
        self.trie = restore_trie()
        self.matrix = [[None for j in range(width)] for i in range(length)]
        index = 0
        for i in range(length):
            for j in range(width):
                self.matrix[i][j] = matrix_string[index].lower()
                index += 1
        self.output = set()

    def backtracking(self, i, j, word, path, curr_len, children):
        rows = len(self.matrix)
        cols = len(self.matrix[0])

        if '*' in children:
            self.output.add((word, curr_len))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            xx = i + dx
            yy = j + dy

            if xx < 0 or xx >= rows or yy < 0 or yy >= cols or (xx, yy) in path:
                continue

            element = self.matrix[xx][yy]
            if element not in children:
                continue

            self.backtracking(xx, yy, word + self.matrix[xx][yy], path.union([(xx, yy)]), curr_len + 1, children[element])

        return

    def solve(self):
        rows = len(self.matrix)
        cols = len(self.matrix[0])

        for i in range(rows):
            for j in range(cols):
                self.backtracking(i, j, self.matrix[i][j], set([(i, j)]), 1, self.trie[self.matrix[i][j]])

        return [element[0] for element in sorted(list(self.output), key=lambda x: x[1], reverse=True) if element[1] >= 3]

def run(): 
    while True:
        print("Enter wordhunt board:")
        matrix_string = input("> ")
        if matrix_string in ['quit', 'q', 'stop', 'break']:
            break
        try:
            solver = Solver(matrix_string)
            print(solver.solve())
            break
        except ValueError as e:
            print(e)