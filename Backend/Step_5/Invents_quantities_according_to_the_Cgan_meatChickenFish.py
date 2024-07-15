import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd
import math
FILE_DB_WITH_Q_ON_GRAMS = r'./Files_to_Generator/____meat_chicken_fish_grams.csv'
avg_file_path = r'./Files_to_Generator/mean_meat_chicken_fish.csv'
st_file_path = r'./Files_to_Generator/var_meat_chicken_fish.csv'
generator = load_model(r'./Generators/generator_meat_chicken_fish_epoch_2001.h5')
names_of_columns_meatChickenFish = ['entrecote', 'hamburger', 'Chicken thighs', 'Chicken sausage',
       'Brisket', 'beef schnitzel', 'Asado', 'Chicken wings', 'edges',
       'Lamb shoulder', 'Roast shoulder', 'roast beef', 'muscle meat',
       'mock fillet', 'Mince', 'meat ribs', 'shoulder cubes', 'sirloin',
       'turkey throat', 'turkey breast', 'turkey turkey', 'turky shawarma',
       'turky wings', 'turky thighs', 'turky liver', 'salt', 'black pepper',
       'garlic powder', 'onion powder', 'paprika', 'cayenne pepper', 'cumin',
       'oregano', 'thyme', 'rosemary', 'bay leaves', 'chili powder', 'parsley',
       'basil', 'cilantro', 'dill', 'soy sauce', 'bbq sauce', 'teriyaki sauce',
       'mustard', 'ketchup', 'mayonnaise', 'olive oil', 'oil', 'sesame oil',
       'balsamic vinegar', 'red wine vinegar', 'white wine vinegar',
       'apple cider vinegar', 'rice vinegar', 'onion', 'garlic', 'leeks',
       'scallions', 'ginger', 'almonds', 'pine nuts', 'raisins', 'cranberries',
       'apricots', 'dates', 'rice', 'quinoa', 'lentils', 'beans', 'peppers',
       'tomatoes', 'carrots', 'celery', 'mushrooms', 'zucchini', 'eggplant',
       'broccoli', 'cauliflower', 'cabbage', 'potatoes', 'carp', 'Dennis',
       'Bermondi', 'mullet', 'salmon', 'Sea bass', 'tilapia', 'tuna',
       'chili sauce']


def matching_the_products_to_the_generator(arr_ingredients):

    # arr_ingredients = arr_ingredients.lower()
    arr_ingredients = np.intersect1d(arr_ingredients, names_of_columns_meatChickenFish)

    normalization_arr = [0] * len(names_of_columns_meatChickenFish)
    for ingredient in arr_ingredients:
        # ingredient = ingredient.lower()
        if ingredient in names_of_columns_meatChickenFish:
            index = names_of_columns_meatChickenFish.index(ingredient)
            normalization_arr[index] = 1
    result = np.array(normalization_arr)
    return result
def matching_the_products_to_the_user(arr_ingredients):
    # Convert both arrays to lowercase
    # names_of_columns_meatChickenFish_lower = np.char.lower(names_of_columns_meatChickenFish)
    # arr_ingredients_lower = np.char.lower(arr_ingredients)

    # Find the intersection of the two arrays
    arr_ingredients_intersection = np.intersect1d(arr_ingredients, names_of_columns_meatChickenFish)

    # Return the intersection
    return arr_ingredients_intersection.tolist()


def generate_quantities_to_meatChickenFish(arr_ingredients):
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
            "quantity": f"{predicted_quantities_original_scale[names_of_columns_meatChickenFish.index(ingredient)]:.2f}"
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

    arrIngredients = ["sirloin", "onion powder", "basil", "black pepper", "tomatoes", "ketchup"]
    #predicted_quantities = generate_quantities(arrIngredients)
    #print(predicted_quantities)
    # print(predicted_quantities)
    # predicted_quantities_original_scale = inverse_transform_quantities(predicted_quantities[0], avg_file_path, st_file_path)
    #
    # print("Predicted quantities for the user's ingredients:")
    #
    # for ingredient in arrIngredients:
    #     print(
    #         f"{ingredient}: {predicted_quantities_original_scale[names_of_columns_meatChickenFish.index(ingredient)]:.2f} grams")
    #
    #