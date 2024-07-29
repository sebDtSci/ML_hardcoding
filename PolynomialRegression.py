import pandas as pd
import numpy as np

f, n = map(int, input().strip().split())
data = [input().strip() for _ in range(n)]

n_test = int(input())
data_test = [input().strip() for _ in range(n_test)]



data_train = [list(map(float, row.split())) for row in data]
data_test = [list(map(float, row.split())) for row in data_test]


columns_train = [f'F{i+1}' for i in range(f)] + ["Target"]
columns_test = [f'F{i+1}' for i in range(f)]


df_Train = pd.DataFrame(data_train, columns=columns_train)
df_test = pd.DataFrame(data_test, columns=columns_test)


X_train = df_Train.iloc[:, :-1].values
y_train = df_Train.iloc[:, -1].values
X_test = df_test.values

def linear_regression(X, y):
    # (X^T X)^(-1) X^T y
    X_transpose = X.T
    coefficients = np.linalg.inv(X_transpose @ X) @ X_transpose @ X
    return coefficients

def polynomial_features(X, degree):
    n_samples, n_features = X.shape
    columns = [np.ones(n_samples)]
    for d in range(1, degree + 1):
        for items in range(n_features):
            columns.append(X[:, items]**d)
    return np.column_stack(columns)

degree = 2

X_poly_train = polynomial_features(X_train, degree)
coefficients = linear_regression(X_poly_train, y_train)
X_poly_test = polynomial_features(X_test, degree)
y_test_pred = X_poly_test @ coefficients
print(y_test_pred)
