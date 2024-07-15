import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd
import math

avg_file_path = r'./Files_to_Generator/mean_salad.csv'
st_file_path = r'./Files_to_Generator/var_salad.csv'
generator = load_model(r'./Generators/generator_epoch_501_salad.h5')
names_of_columns_salad = ['beet', 'broccoli', 'cauliflower', 'celery leaves', 'coriander',
       'cucumber', 'dill', 'eggplant', 'garlic', 'green onion', 'green peper',
       'guard', 'hot peper', 'kohlrabi', 'lettuce', 'mushrooms', 'nana',
       'onion', 'orange peper', 'parsley', 'purple cabbage', 'radish',
       'red oninon', 'red peper', 'squash', 'tomato', 'white cabbage',
       'yellow peper', 'zucchini', 'artichoke', 'carrot', 'olive oil',
       'vinegar', 'oil', 'salt', 'pepper', 'halloumi cheese', 'apple pear',
       'banana', 'blueberries', 'chery', 'clementine', 'green-grape',
       'green apple', 'hermon apple', 'kiwi', 'lemon', 'orange', 'peach',
       'nectarine', 'yellow apple', 'pear', 'purple grapes', 'pineapple']

def matching_the_products_to_the_generator(arr_ingredients):

    arr_ingredients = np.intersect1d(arr_ingredients, names_of_columns_salad)

    normalization_arr = [0] * len(names_of_columns_salad)
    for ingredient in arr_ingredients:
        #ingredient = ingredient.lower()
        if ingredient in names_of_columns_salad:
            index = names_of_columns_salad.index(ingredient)
            normalization_arr[index] = 1
    result = np.array(normalization_arr)
    return result
def matching_the_products_to_the_user(arr_ingredients):

    arr_ingredients_intersection = np.intersect1d(arr_ingredients, names_of_columns_salad)

    return arr_ingredients_intersection.tolist()

def generate_quantities_to_salad(arr_ingredients):
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
            "quantity": f"{predicted_quantities_original_scale[names_of_columns_salad.index(ingredient)]:.2f}"
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

    arrIngredients = ["kohlrabi", "onion", "lemon", "kiwi", "olive oil", "eggplant"]
    #predicted_quantities = generate_quantities(arrIngredients)
    # print(predicted_quantities)
    # predicted_quantities_original_scale = inverse_transform_quantities(predicted_quantities[0], avg_file_path, st_file_path)
    # predicted_quantities_original_scale = round_up_quantities(predicted_quantities_original_scale)
    # print("Predicted quantities for the user's ingredients:")
    #
    # for ingredient in arrIngredients:
    #     print(
    #         f"{ingredient}: {predicted_quantities_original_scale[names_of_columns_salad.index(ingredient)]:.2f} grams")

