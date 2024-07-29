### Initialisation

```python
class PolyReg():
    def __init__(self, degree, learning_rate, iterations):
        self.degree = degree
        self.learning_rate = learning_rate
        self.iterations = iterations
```

1. **`class PolyReg():`**: Déclare une nouvelle classe appelée `PolyReg`.
2. **`def __init__(self, degree, learning_rate, iterations):`**: Définit le constructeur de la classe qui initialise les objets de la classe avec des paramètres spécifiques.
3. **`self.degree = degree`**: Attribue le paramètre `degree` à l'attribut `degree` de l'objet.
4. **`self.learning_rate = learning_rate`**: Attribue le paramètre `learning_rate` à l'attribut `learning_rate` de l'objet.
5. **`self.iterations = iterations`**: Attribue le paramètre `iterations` à l'attribut `iterations` de l'objet.

### Transformation des caractéristiques

```python
def transform(self, X):
    X_transform = np.ones((X.shape[0], 1))
    for j in range(1, self.degree + 1):
        for k in range(X.shape[1]):
            X_transform = np.hstack((X_transform, np.power(X[:, k], j).reshape(-1, 1)))
    return X_transform
```

1. **`def transform(self, X):`**: Définit une méthode `transform` qui prend en entrée une matrice `X`.
2. **`X_transform = np.ones((X.shape[0], 1))`**: Initialise `X_transform` avec une colonne de 1 (pour le biais) et un nombre de lignes égal à celui de `X`.
3. **`for j in range(1, self.degree + 1):`**: Boucle sur les puissances des polynômes de 1 à `degree`.
4. **`for k in range(X.shape[1]):`**: Boucle sur chaque caractéristique (colonne) de `X`.
5. **`X_transform = np.hstack((X_transform, np.power(X[:, k], j).reshape(-1, 1)))`**: Calcule `X[:, k]` élevé à la puissance `j`, reforme le résultat en une colonne, et l'ajoute horizontalement à `X_transform`.
6. **`return X_transform`**: Retourne la matrice transformée `X_transform`.

### Normalisation des caractéristiques

```python
def normalize(self, X):
    X[:, 1:] = (X[:, 1:] - np.mean(X[:, 1:], axis=0)) / np.std(X[:, 1:], axis=0)
    return X
```

1. **`def normalize(self, X):`**: Définit une méthode `normalize` qui prend en entrée une matrice `X`.
2. **`X[:, 1:] = (X[:, 1:] - np.mean(X[:, 1:], axis=0)) / np.std(X[:, 1:], axis=0)`**: Normalise chaque colonne de `X` sauf la première en soustrayant la moyenne et en divisant par l'écart-type.
3. **`return X`**: Retourne la matrice normalisée `X`.

### Ajustement du modèle

```python
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
```

1. **`def fit(self, X, y):`**: Définit une méthode `fit` qui prend en entrée les caractéristiques `X` et les cibles `y`.
2. **`self.X = X`**: Stocke `X` dans l'attribut `X` de l'objet.
3. **`self.y = y`**: Stocke `y` dans l'attribut `y` de l'objet.
4. **`self.m, self.n = self.X.shape`**: Décompose la forme de `X` en nombre d'échantillons `m` et nombre de caractéristiques `n`.
5. **`self.w = np.zeros((self.n * self.degree) + 1)`**: Initialise les poids `w` à zéro avec une taille appropriée pour les caractéristiques polynomiales.
6. **`X_transform = self.transform(self.X)`**: Transforme `X` en utilisant la méthode `transform`.
7. **`X_normalize = self.normalize(X_transform)`**: Normalise `X_transform` en utilisant la méthode `normalize`.
8. **`for i in range(self.iterations):`**: Boucle sur le nombre d'itérations spécifié.
9. **`h = self.predict_internal(X_normalize)`**: Calcule les prédictions internes `h` en utilisant `X_normalize`.
10. **`error = h - self.y`**: Calcule l'erreur entre les prédictions `h` et les cibles `y`.
11. **`self.w = self.w - self.learning_rate * (1/self.m) * np.dot(X_normalize.T, error)`**: Met à jour les poids `w` en utilisant la descente de gradient.
12. **`return self`**: Retourne l'objet ajusté.

### Prédiction interne

```python
def predict_internal(self, X):
    return np.dot(X, self.w)
```

1. **`def predict_internal(self, X):`**: Définit une méthode `predict_internal` qui prend en entrée une matrice `X`.
2. **`return np.dot(X, self.w)`**: Retourne le produit matriciel de `X` et des poids `w`, calculant ainsi les prédictions internes.

### Prédiction

```python
def predict(self, X):
    X_transform = self.transform(X)
    X_normalize = self.normalize(X_transform)
    return self.predict_internal(X_normalize)
```

1. **`def predict(self, X):`**: Définit une méthode `predict` qui prend en entrée une matrice `X`.
2. **`X_transform = self.transform(X)`**: Transforme `X` en utilisant la méthode `transform`.
3. **`X_normalize = self.normalize(X_transform)`**: Normalise `X_transform` en utilisant la méthode `normalize`.
4. **`return self.predict_internal(X_normalize)`**: Retourne les prédictions internes calculées avec `X_normalize`.

Cette décomposition ligne par ligne montre comment la classe `PolyReg` transforme et normalise les données d'entrée, ajuste les poids du modèle par descente de gradient, et génère des prédictions pour de nouvelles données.