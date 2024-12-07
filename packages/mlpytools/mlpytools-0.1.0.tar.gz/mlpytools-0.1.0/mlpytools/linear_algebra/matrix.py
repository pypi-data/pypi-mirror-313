class Matrix:
    def __init__(self, rows: int, cols: int):
        self.rows = rows  # Number of rows
        self.cols = cols  # Number of columns
        self.data = [[0 for col in range(cols)] for row in range(rows)]

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions")
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + other.data[i][j]
        return result

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions")
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] - other.data[i][j]
        return result

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError(
                "Number of columns in the first matrix must be equal to the \
            number of rows in the second matrix"
            )
        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data])


if __name__ == "__main__":
    A = Matrix([[2, 3], [2, 3]])
    B = Matrix([[3, 2], [3, 2]])
    print(A + B)
