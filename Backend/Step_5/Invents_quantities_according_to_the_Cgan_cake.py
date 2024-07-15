import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd
import math

avg_file_path = r'./Files_to_Generator/mean_cakes.csv'
st_file_path = r'./Files_to_Generator/var_cakes.csv'
generator = load_model(r'./Generators/generator_epoch_1401_cake.h5')
names_of_columns_cake = ['eggs', 'sour cream', 'oil', 'baking soda', 'vanilla extract',
       'peanut Butter', 'baking powder', 'chocolate chips', 'walnuts', 'salt',
       'cocoa powder', 'sugar', 'milk', 'flour', 'Oatmeal', 'orange juice',
       'cornflour', 'ground coke', 'ground cinnamon', 'yeast',
       'dark chocolate', 'sweet cream']

def matching_the_products_to_the_generator(arr_ingredients):

    arr_ingredients = np.intersect1d(arr_ingredients, names_of_columns_cake)

    normalization_arr = [0] * len(names_of_columns_cake)
    for ingredient in arr_ingredients:
        #ingredient = ingredient.lower()
        if ingredient in names_of_columns_cake:
            index = names_of_columns_cake.index(ingredient)
            normalization_arr[index] = 1
    result = np.array(normalization_arr)
    return result

def matching_the_products_to_the_user(arr_ingredients):
    # result = []
    # arr_ingredients = np.intersect1d(arr_ingredients, names_of_columns_cake)
    # print(arr_ingredients, "after matching_the_products_to_the_user")
    # for ingredient in arr_ingredients:
    #     ingredient = ingredient.lower()
    #     if ingredient in names_of_columns_cake:
    #         result.append(ingredient)
    # return result
    arr_ingredients_intersection = np.intersect1d(arr_ingredients, names_of_columns_cake)

    # Return the intersection
    return arr_ingredients_intersection.tolist()
def generate_quantities_to_cake(arr_ingredients):
    arr_ingredients = matching_the_products_to_the_user(arr_ingredients)
    arr_ingredients_to_model = matching_the_products_to_the_generator(arr_ingredients)
    print(arr_ingredients)
    print(arr_ingredients_to_model)
    arr_ingredients_to_model = np.expand_dims(arr_ingredients_to_model, axis=0)
    quantities = generator.predict(arr_ingredients_to_model)
    predicted_quantities_original_scale = inverse_transform_quantities(quantities[0], avg_file_path, st_file_path)

    predicted_quantities_original_scale = round_up_quantities(predicted_quantities_original_scale)
    print("Predicted quantities for the user's ingredients:")
    result_list = []
    for ingredient in arr_ingredients:
        result_list.append({
            "product": ingredient,
            "quantity": f"{predicted_quantities_original_scale[names_of_columns_cake.index(ingredient)]:.2f}"
        })

    return result_list
def inverse_transform_quantities(predicted_quantities, avg_file_path, st_file_path):
    dfAVG = pd.read_csv(avg_file_path,header=None)
    avgcol = dfAVG.values.flatten()
    dfST = pd.read_csv(st_file_path,header=None)
    stcol = dfST.values.flatten()
    float_avgcol = [float(x) for x in avgcol]
    float_stcol = [float(x) for x in stcol]
    result = []
    for i in range(len(predicted_quantities)):
        transformed_value = (predicted_quantities[i] * float_stcol[i]) + float_avgcol[i]
        result.append(transformed_value)
    return result

def round_up_quantities(predicted_quantities):
    return [math.ceil(abs(number)) for number in predicted_quantities]

if __name__ == '__main__':

    arrIngredients = ["sugar", "chocolate chips", "ground coke", "flour", "baking soda", "oil"]
    # predicted_quantities = generate_quantities(arrIngredients)
    # print(predicted_quantities)
    # predicted_quantities_original_scale = inverse_transform_quantities(predicted_quantities[0], avg_file_path, st_file_path)
    # predicted_quantities_original_scale = round_up_quantities(predicted_quantities_original_scale)
    # print("Predicted quantities for the user's ingredients:")
    #
    # for ingredient in arrIngredients:
    #     print(
    #         f"{ingredient}: {predicted_quantities_original_scale[names_of_columns_cake.index(ingredient)]:.2f} grams")
    #
