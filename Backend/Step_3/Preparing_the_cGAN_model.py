from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, LeakyReLU, BatchNormalization, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from Preparing_the_data_for_the_cGAN_model import creating_arrays_for_the_model
from tensorflow.keras.layers import Layer
import os
import sys
from sklearn.preprocessing import StandardScaler
BINARY_FILE_PATH = r'/content/drive/MyDrive/pro/step_4/cakes_binary.csv'
FILE_DB_WITH_Q_ON_GRAMS = r'/content/drive/MyDrive/pro/step_4/cakes_grams.csv'

scaler = StandardScaler()


def creating_arrays_for_the_model():


    df1 = pd.read_csv(BINARY_FILE_PATH)
    df2 = pd.read_csv(FILE_DB_WITH_Q_ON_GRAMS)

    X = df1.iloc[1:, :].values
    Y = df2.iloc[1:, :].values

    # Convert to NumPy arrays (if not already)
    X = np.array(X)
    Y = np.array(Y)

    print("Shape of Y:", Y.shape)
    print("Shape of X:", X.shape)

    print(X[len(X)-2])
    print(Y[len(Y)-2])
    return X, Y


def build_generator(input_dim):
    inputs = Input(shape=(input_dim,))
    x = Dense(128)(inputs)
    x = LeakyReLU(alpha=0.2)(x)
    x = BatchNormalization(momentum=0.8)(x)
    x = Dense(256)(x)
    x = LeakyReLU(alpha=0.2)(x)
    x = BatchNormalization(momentum=0.8)(x)
    x = Dense(512)(x)
    x = LeakyReLU(alpha=0.2)(x)
    x = BatchNormalization(momentum=0.8)(x)
    outputs = Dense(input_dim, activation='linear')(x)

    model = Model(inputs, outputs)
    return model


def build_discriminator(input_dim):
    inputs = Input(shape=(input_dim * 2,))
    x = Dense(4096)(inputs)
    x = LeakyReLU(alpha=0.2)(x)
    x = Dropout(0.5)(x)
    x = Dense(4096)(x)
    x = LeakyReLU(alpha=0.2)(x)
    x = Dropout(0.5)(x)
    outputs = Dense(1, activation='sigmoid')(x)

    model = Model(inputs, outputs)
    return model


class ConcatenateLayer(Layer):
    def call(self, inputs):
        return tf.concat(inputs, axis=1)

def build_cgan(generator, discriminator, input_dim):
    discriminator.trainable = False

    recipe_input = Input(shape=(input_dim,))
    quantity_output = generator(recipe_input)
    combined_input = ConcatenateLayer()([recipe_input, quantity_output])

    validity = discriminator(combined_input)

    model = Model(recipe_input, validity)
    model.compile(optimizer=Adam(0.0002, 0.5), loss='binary_crossentropy')
    discriminator.trainable = True
    return model


def train(generator, discriminator, cgan, X_train, y_train, epochs, batch_size=32):
    valid = np.ones((batch_size, 1), dtype=np.float32)
    fake = np.zeros((batch_size, 1), dtype=np.float32)
    sample_idx = np.random.randint(0, X_train.shape[0], 1)
    sample_recipe = X_train[sample_idx]
    sample_quantity = y_train[sample_idx]

    for epoch in range(epochs+1):
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        recipe_batch = X_train[idx]
        quantity_batch = y_train[idx]

        generated_quantities = generator.predict(recipe_batch)

        real_combined = np.concatenate([recipe_batch, quantity_batch], axis=1).astype(np.float32)
        fake_combined = np.concatenate([recipe_batch, generated_quantities], axis=1).astype(np.float32)

        d_loss_real = discriminator.train_on_batch(real_combined, valid)
        d_loss_fake = discriminator.train_on_batch(fake_combined, fake)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        g_loss = cgan.train_on_batch(recipe_batch, valid)

        print(f"{epoch + 1}/{epochs} [D loss: {d_loss[0]} | D accuracy: {100 * d_loss[1]:.2f}] [G loss: {g_loss}]")

        if epoch % 100 == 0:
            generator.save(f"./cGAN_models/generator_epoch_{epoch + 1}.h5")
            discriminator.save(f"./cGAN_models/discriminator_epoch_{epoch + 1}.h5")

            generated_quantity = generator.predict(sample_recipe)

            print("Sample Recipe:", sample_recipe)
            print("Actual Quantity:", sample_quantity)
            print("Generated Quantity:", generated_quantity)
            present_ingredient_indices = np.where(sample_recipe[0] == 1)[0]
            generated_quantity_=scaler.inverse_transform(generated_quantity)
            sample_quantity_=scaler.inverse_transform(sample_quantity)
            # Print the actual and generated quantities for the present ingredients
            print("\nSample Recipe (only present ingredients):")
            for idx in present_ingredient_indices:
                print(f"Ingredient {idx}: Actual Quantity = {sample_quantity_[0][idx]}, Generated Quantity = {generated_quantity_[0][idx]}")



if __name__ == '__main__':
    X, Y = creating_arrays_for_the_model()
    scaler.fit(Y)
    Y=scaler.transform(Y)
    print("X dtype:", X.dtype)
    print("Y dtype:", Y.dtype)
    st = scaler.scale_
    avg = scaler.mean_
    print(st)
    print(avg)
    file_path_st = r'/content/drive/MyDrive/pro/step_4/var_cakes.csv'
    file_path_avg = r'/content/drive/MyDrive/pro/step_4/mean_cakes.csv'
    st_df = pd.DataFrame([st])
    avg_df = pd.DataFrame([avg])
    st_df.to_csv(file_path_st, index=False, header=False)
    avg_df.to_csv(file_path_avg, index=False, header=False)

    X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

    input_dim = X_train.shape[1]
    generator = build_generator(input_dim)
    generator.summary()
    discriminator = build_discriminator(input_dim)
    discriminator.summary()
    discriminator.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    cgan = build_cgan(generator, discriminator, input_dim)
    cgan.summary()
    epochs = 2000
    batch_size = 64
    train(generator, discriminator, cgan, X_train, y_train, epochs, batch_size)