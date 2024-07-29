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

class PolyReg():
    def __init__(self, degree, learning_rate, iterations):
        self.degree = degree
        self.learning_rate = learning_rate
        self.iterations = iterations
        
    def transform(self, X):
        X_transform = np.ones((X.shape[0], 1))
        for j in range(1, self.degree + 1):
            for k in range(X.shape[1]):
                X_transform = np.hstack((X_transform, np.power(X[:, k], j).reshape(-1, 1)))
        return X_transform
    
    def normalize(self, X):
        X[:, 1:] = (X[:, 1:] - np.mean(X[:, 1:], axis=0)) / np.std(X[:, 1:], axis=0)
        return X
        
    def fit(self, X, y):
        self.X = X
        self.y = y
        self.m, self.n = self.X.shape
        self.w = np.zeros((self.n * self.degree) + 1)
        
        X_transform = self.transform(self.X)
        X_normalize = self.normalize(X_transform)
        
        for i in range(self.iterations):
            h = self.predict_internal(X_normalize)
            error = h - self.y
            self.w = self.w - self.learning_rate * (1/self.m) * np.dot(X_normalize.T, error)
        return self
    
    def predict_internal(self, X):
        return np.dot(X, self.w)
    
    def predict(self, X):
        X_transform = self.transform(X)
        X_normalize = self.normalize(X_transform)
        return self.predict_internal(X_normalize)

model = PolyReg(degree=2, learning_rate=0.01, iterations=500)
model.fit(X_train, y_train)

Y_pred = model.predict(X_test)

for el in Y_pred:
    print(el)
