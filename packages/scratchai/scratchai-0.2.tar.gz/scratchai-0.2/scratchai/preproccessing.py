import numpy as np
import pandas as pd

class StandardScaler:
    def __init__(self):
        self.std = dict()
        self.mean = dict()
        
    def transform(self, X, columns):
        for column in columns:
            # store the feature standard and the mean for inverse sacling
            self.std[column] = X[column].std()
            self.mean[column] = X[column].mean()
            
            # scale the feature using the stored standard and mean
            X.loc[:, column] = (X[column] - self.mean[column]) / self.std[column]
            
        return X
    
    def inverse_transform(self, X, columns):
        for column in columns:
            X[column] = (X[column] + self.mean[column] * self.std[column])
            
        return X
    
def polynomial_features(X, degree = 1, inetraction_term = False):
    poly_features = []
    
    for row in X:
        inter_term = 1
        poly_row = []
        for v in row:
            inter_term *= v
            poly_row += [v ** d for d in range(1, degree + 1)]
        if inetraction_term:
            poly_row.append(inter_term)
        poly_features.append(poly_row)
        
    return np.array(poly_features)

def split_data(X, split_size = 0.8):
    first_set = X.sample(frac = split_size)
    second_set = X.drop(first_set.index)
    return first_set.reset_index(drop = True), second_set.reset_index(drop = True)

def ont_hot(X):
    encoded_data = pd.get_dummies(X).astype('int')
    return encoded_data