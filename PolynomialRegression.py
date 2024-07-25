# Enter your code here. Read input from STDIN. Print output to STDOUT
import pandas as pd
import numpy as np

f, n = map(int, input().strip().split())
data = [input().strip() for _ in range(n)]

data = [list(map(float, row.split())) for row in data]

columns = [f'F{i+1}' for i in range(f)] + ["Target"]

df = pd.DataFrame(data, columns=columns)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

def linear_regression(X, y):
    # (X^T X)^(-1) X^T y
    X_transpose = X.T
    coefficients = np.linalg.inv(X_transpose @ X) @ X_transpose @ X
    return coefficients
