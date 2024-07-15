import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd
import math

FILE_DB_WITH_Q_ON_GRAMS = r'./Files_to_Generator/________stew_side_grams.csv'
avg_file_path = r'./Files_to_Generator/mean_stew_side.csv'
st_file_path = r'./Files_to_Generator/var_stew_side.csv'
generator = load_model(r'./Generators/generator_epoch_stew_side501.h5')
names_of_columns_stew_side = ['bulgur', 'barley', 'chickpeas', 'egg noodles', 'kidney beans',
       'fusilli', 'fettuccine', 'lentils', 'macaroni', 'lazanga', 'makaroni',
       'kosher salt', 'millet', 'paprika', 'onion powder', 'olive oil', 'oil',
       'nyuki', 'pasta', 'penne', 'pepper', 'pinto beans', 'polenta',
       'rize pasta', 'rice noodles', 'rice', 'quinoa', 'spaghetti',
       'split peas', 'asparagus', 'red potato', 'coriander', 'dill', 'parsley',
       'onion', 'red oninon', 'garlic', 'cayenne pepper', 'chili powder',
       'potato', 'sweet potato', 'cream']

def matching_the_products_to_the_generator(arr_ingredients):


    arr_ingredients = np.intersect1d(arr_ingredients, names_of_columns_stew_side)

    normalization_arr = [0] * len(names_of_columns_stew_side)
    for ingredient in arr_ingredients:
        #ingredient = ingredient.lower()
        if ingredient in names_of_columns_stew_side:
            index = names_of_columns_stew_side.index(ingredient)
            normalization_arr[index] = 1
    result = np.array(normalization_arr)
    return result

def matching_the_products_to_the_user(arr_ingredients):
    arr_ingredients_intersection = np.intersect1d(arr_ingredients, names_of_columns_stew_side)

    return arr_ingredients_intersection.tolist()

def generate_quantities_to_stew_side(arr_ingredients):
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
            "quantity": f"{predicted_quantities_original_scale[names_of_columns_stew_side.index(ingredient)]:.2f}"
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

    arrIngredients = ["bulgur", "chili powder", "pepper", "potato"]
    #generate_quantities(arrIngredients)

    # predicted_quantities_original_scale = inverse_transform_quantities(predicted_quantities[0], avg_file_path, st_file_path)
    # predicted_quantities_original_scale = round_up_quantities(predicted_quantities_original_scale)
    # print("Predicted quantities for the user's ingredients:")
    #
    # for ingredient in arrIngredients:
    #     print(
    #         f"{ingredient}: {predicted_quantities_original_scale[names_of_columns_stew_side.index(ingredient)]:.2f} grams")

