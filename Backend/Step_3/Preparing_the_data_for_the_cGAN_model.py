import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

BINARY_FILE_PATH = r'..\Files\‏‏binary_recipes.csv'
FILE_DB_WITH_Q_ON_GRAMS = r'..\Files\‏‏‏‏‏‏Food Ingredients and Recipe Dataset -with grams.csv'
def creating_arrays_for_the_model():


    df1 = pd.read_csv(BINARY_FILE_PATH)
    df2 = pd.read_csv(FILE_DB_WITH_Q_ON_GRAMS)

    X = df1.iloc[:, 1:12905].values
    Y = df2.iloc[:, 5:-1].values

    # Convert to NumPy arrays (if not already)
    X = np.array(X)
    Y = np.array(Y)

    print("Shape of Y:", Y.shape)
    print("Shape of X:", X.shape)

    print(X[len(X)-1])
    print(Y[len(Y)-1])
    return X, Y

if __name__ == '__main__':
   X, Y = creating_arrays_for_the_model()
