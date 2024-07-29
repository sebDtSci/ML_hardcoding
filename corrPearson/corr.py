import numpy as np 

x = input().strip()
x = list(map(int, x.split()))
y = input().strip()
y = list(map(int, y.split()))

print(x)
def corr_pearson(x:list, y:list)-> float:
    
    n = len(x)
    
    x_sum = sum(x)
    y_sum = sum(y)
    
    x_square_sum = sum([i**2 for i in x])
    y_square_sum = sum([i**2 for i in y])
    
    # x_y_sum = sum([x[i] * y[i] for i in range(len(x))])
    # x_y_sum2 = sum([nx * ny for i, (nx, ny) in enumerate(zip(x, y))])
    x_y_sum2 = sum([nx * ny for nx, ny in zip(x, y)])
    
    numerator = n* (x_y_sum2) - (x_sum * y_sum)
    denominator = np.sqrt((n * x_square_sum - x_sum**2) *(n* y_square_sum - y_sum**2))
    # denominator = ((n * x_square_sum - x_sum**2) *(n* y_square_sum - y_sum**2))*(1/2)
    
    
    res = numerator / denominator
    return res
    

print(round(corr_pearson(x, y), 3))