import pandas as pd 
import numpy as np

f, n = map(int, input().strip().split())
data = [input().strip() for _ in range(n)]

n_test = int(input())
data_test = [input().strip() for _ in range(n_test)]

data_train = [list(map(float, row.split())) for row in data]
data_test = [list(map(float, row.split())) for row in data_test]

col_train = [f'{i+1}' for i in range(f)] + ['Target']
col_test = [f'{i+1}' for i in range(f)]

df_Train = pd.DataFrame(data_train, columns=col_train)
df_test = pd.DataFrame(data_test, columns=col_test)


# X_train = df_Train.iloc[:, :-1].values
# y_train = df_Train.iloc[:, -1].values
X_train = df_Train.iloc[:, :-1]
y_train = df_Train.iloc[:, -1]

# X_test = df_test.values

#####################################################################
def feature_eng(df: pd.DataFrame):
    df['sum'] = df.sum(axis=1) / len(df.columns)
    return df


X_train = feature_eng(X_train)
X_test = feature_eng(df_test)
#####################################################################

X_train = X_train.values
X_test = X_test.values

class LinearRegression():
    def __init__(self, learning_rate, iterations):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weight = None
        self.bias = None
        self.tolerance = 1e-6
        
    def fit(self, X, y):
        num_sample, num_features = X.shape
        self.weight = np.random.rand(num_features)
        self.bias = 0
        
        for i in range(self.iterations):
            y_pred = np.dot(X, self.weight) + self.bias
            #derivate :
            # dw = (1 / num_sample) * np.dot(X.T, y_pred - y)
            dw = (1 / num_sample) * np.dot(X.T, (y_pred - y))
            db = (1/num_sample) * np.sum(y_pred-y)
            
            # self.weight = self.weight - self.learning_rate * dw
            # self.bias = self.bias - self.learning_rate * db
            
            new_weight = self.weight - self.learning_rate * dw
            new_bias = self.bias - self.learning_rate * db
            
            #conv check
            if np.all(np.abs(new_weight - self.weight) < self.tolerance) and np.abs(new_bias - self.bias) < self.tolerance:
                print(f"Convergence reached at iteration {i+1}")
                break
            
            self.weight = new_weight
            self.bias = new_bias
            
        return self
    
    def predict(self, X):
        return np.dot(X, self.weight) + self.bias

model = LinearRegression(0.01, 1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

for el in y_pred:
    print(el)
        
    

    