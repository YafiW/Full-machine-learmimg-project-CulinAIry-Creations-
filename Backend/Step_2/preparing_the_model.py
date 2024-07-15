import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from keras.layers import Dropout
from sklearn.metrics import confusion_matrix
from keras.models import save_model
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns
File_Path = r'..\Files\__Food Ingredients and Recipe Dataset - after2.csv'
#FILE_HISTORY_PATH = r'..\Files\‏‏model_history.csv'
FILE_HISTORY_PATH = r'..\Files\model_history2.csv'
binary_file_path = r'..\Files\‏‏binary_recipes2.csv'

X = []
Y = []
def how_many_columns():
    df = pd.read_csv(File_Path)

    # Print the number of columns
    num_columns = df.shape[1]
    print("Number of columns:", num_columns)

def generates_binary_file():

    df = pd.read_csv(File_Path)

    categories = df['category'].str.get_dummies()
    columns_to_drop = ['Title', 'Instructions', 'Cleaned_Ingredients', 'filtered_ingredients']


    df.drop(columns=columns_to_drop, inplace=True)


    df = pd.concat([df, categories], axis=1)


    df.drop(columns=['category'], inplace=True)

    try:
        df.to_csv(binary_file_path, index=False)
        print("CSV file saved successfully.")
    except Exception as e:
        print("Error saving CSV file:", e)


def creating_arrays_for_the_model():

    # Read the CSV file
    df = pd.read_csv(binary_file_path)

    # Extract features (X) and labels (Y)
    X = df.iloc[:, 1:12905].values
    Y = df.iloc[:, 12905:].values

    # Convert to NumPy arrays (if not already)
    X = np.array(X)
    Y = np.array(Y)

    print("Shape of Y:", Y.shape)

    print(len(X))
    print(len(Y))
    return X, Y

def build_model(X_train,X_test,Y_train,Y_test):
    model = Sequential()

    # Input layer
    model.add(Dense(4096, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(Dropout(0.25))

    # Hidden layers
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.25))
    #model.add(Dense(4096, activation='relu'))
    #model.add(Dropout(0.25))


    # Output layer
    model.add(Dense(4, activation='softmax'))

    model.summary()

    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    # Add the early_stopping callback to the fit method
    history = model.fit(X_train,
                        Y_train,
                        batch_size=32,
                        epochs=100,  # Set a higher epoch if using early stopping
                        validation_data=(X_test, Y_test),
                        callbacks=[early_stopping])  # Add early_stopping here

    #model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

    #history = model.fit(X_train,
                        #Y_train,
                        #batch_size=32,
                        #epochs=10,
                        #validation_data=(X_test, Y_test))

    model.save(r'..\Models\my_model2.h5')
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(FILE_HISTORY_PATH, mode='a', header=True)
    Y_pred_probs = model.predict(X_test)
    Y_pred = np.argmax(Y_pred_probs, axis=1)
    Y_true = np.argmax(Y_test, axis=1)

    cm = confusion_matrix(Y_true, Y_pred)
    print("Confusion Matrix:")
    print(cm)
    # Calculate total number of predictions
    total_predictions = np.sum(cm)

    # Calculate the number of correct predictions (diagonal elements)
    correct_predictions = np.sum(np.diag(cm))

    # Calculate accuracy
    accuracy = correct_predictions / total_predictions

    # Print accuracy
    print("Accuracy:", accuracy)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=category_names, yticklabels=category_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()


if __name__ == '__main__':
    #generates_binary_file()
    #how_many_columns()
    X, Y = creating_arrays_for_the_model()
    category_names = ['cake', 'meat_and_chicken_and_fish_list', 'salad', 'stew_and_side_dishes_list']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    build_model(X_train, X_test, Y_train, Y_test)
    print("X_train.shape: ",X_train.shape[1])
