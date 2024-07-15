import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
from Invents_quantities_according_to_the_Cgan_meatChickenFish import generate_quantities_to_meatChickenFish
from Invents_quantities_according_to_the_Cgan_cake import generate_quantities_to_cake
from Invents_quantities_according_to_the_Cgan_salad import generate_quantities_to_salad
from Invents_quantities_according_to_the_Cgan_stew_side import generate_quantities_to_stew_side



FILE_DB_PATH = r'../Files/__Food Ingredients and Recipe Dataset - after2.csv'
model = load_model(r'..\Models\my_model1.h5')
ingredients_to_cups = ['soy sauce', 'bbq sauce', 'teriyaki sauce',
                    'mustard', 'ketchup', 'mayonnaise', 'olive oil', 'oil', 'sesame oil',
                    'balsamic vinegar', 'red wine vinegar', 'white wine vinegar',
                    'apple cider vinegar', 'rice vinegar','vinegar','milk','orange juice','chili sauce']

ingredients_to_units = ['beet', 'celery leaves', 'coriander',
       'cucumber', 'eggplant', 'garlic', 'green onion', 'green peper',
       'guard', 'hot peper', 'kohlrabi', 'lettuce', 'mushrooms',
       'onion', 'orange peper', 'purple cabbage', 'radish',
       'red oninon', 'red peper', 'squash', 'tomato', 'white cabbage',
       'yellow peper', 'zucchini', 'artichoke', 'carrot',
       'black pepper', 'apple pear','banana', 'blueberries', 'chery', 'clementine', 'green-grape',
       'green apple', 'hermon apple', 'kiwi', 'lemon', 'orange', 'peach',
       'nectarine', 'yellow apple', 'pear', 'purple grapes', 'pineapple','asparagus', 'red potato',
       'potatoes', 'sweet potato','eggs']
def adapting_the_products_to_the_existing_products(arr_ingredients_from_the_user):

    arr_ingredients_from_the_user_to_category_model = [ingredient.lower() for ingredient in arr_ingredients_from_the_user]

    arr_ingredients_from_the_user_to_category_model = ['chicken' if 'chicken' in arr_ingredients_from_the_user_to_category_model else product for product in arr_ingredients_from_the_user_to_category_model]

    ingredients_to_replace_meat = ["hamburger", "entrecote", "beef schnitzel", "heart turkey",
                                   "mock fillet", "muscle meat", "turkey throat", "turkey shawarma"]
    ingredients_to_replace_fish = ["bermondi", "carp", "dennis", "mullet", "sea bass"]

    ingredients_to_replace_meat_set = set(ingredients_to_replace_meat)
    ingredients_to_replace_fish_set = set(ingredients_to_replace_fish)

    seen_replacements = set()

    result = []
    for ingredient in arr_ingredients_from_the_user_to_category_model:
        if ingredient in ingredients_to_replace_meat_set:
            if "pork" not in seen_replacements:
                result.append("pork")
                seen_replacements.add("pork")
        elif ingredient in ingredients_to_replace_fish_set:
            if "salmon" not in seen_replacements:
                result.append("salmon")
                seen_replacements.add("salmon")
        else:
            if ingredient not in seen_replacements:
                result.append(ingredient)
                seen_replacements.add(ingredient)

    return result




def normalization_of_data_from_the_user(arr_ingredients):
    df = pd.read_csv(FILE_DB_PATH)
    names_of_columns_ingredients = list(df.columns[5:-1])
    normalization_arr = [0] * len(names_of_columns_ingredients)
    for ingredient in arr_ingredients:
        ingredient = ingredient.lower()
        if ingredient in names_of_columns_ingredients:
            index = names_of_columns_ingredients.index(ingredient)
            normalization_arr[index] = 1
    result = np.array(normalization_arr)
    return result

def sending_to_the_model(normalization_arr):

    normalization_arr = normalization_arr.reshape(1, -1)  # Reshape to (1, 12904)
    prediction = model.predict(normalization_arr)
    prediction_sum = np.sum(prediction)  # Sum of the predicted array
    return prediction, prediction_sum

def converts_grams_to_the_appropriate_unit(arrIngredients):
    for ingredient in arrIngredients:
        if ingredient["product"] in ingredients_to_cups:
            if float(ingredient["quantity"]) < 200:
                ingredient["quantity"] = float(ingredient["quantity"])
                ingredient["quantity"] = ingredient["quantity"] / 10
                ingredient["quantity"] = str(ingredient["quantity"]) + ' tsp.'
            else:
                ingredient["quantity"] = float(ingredient["quantity"])
                ingredient["quantity"] = ingredient["quantity"] / 200
                ingredient["quantity"] = str(ingredient["quantity"]) + ' cups'
        elif ingredient["product"] not in ingredients_to_units:
            ingredient["quantity"] = ingredient["quantity"] + ' grams'
    return arrIngredients

def the_final_prediction_result(arrIngredients):
    result = []
    predicted_category = ''
    arrIngredientsToPredicition = adapting_the_products_to_the_existing_products(arrIngredients)
    print(arrIngredients, "arrIngredients")
    normalization_arrIngredients = normalization_of_data_from_the_user(arrIngredientsToPredicition)
    arr_prediction, result2_sum = sending_to_the_model(normalization_arrIngredients)
    print(arr_prediction)
    arr_prediction = arr_prediction[0]
    print(arr_prediction)
    print(normalization_arrIngredients, "arr to model1")
    max_val = arr_prediction[0]
    max_ind = 0

    for index, value in enumerate(arr_prediction):
        if value > max_val:
            max_val = value
            max_ind = index
    if max_ind == 0:
        predicted_category = "cake"
        print("cake")

        result = generate_quantities_to_cake(arrIngredients)
    elif max_ind == 1:
        predicted_category = "meat and chicken and fish"
        print("meat and chicken and fish")
        print(arrIngredients, "to model2")
        result = generate_quantities_to_meatChickenFish(arrIngredients)
    elif max_ind == 2:
        predicted_category = "salad"
        print("salad")
        result = generate_quantities_to_salad(arrIngredients)
    else:
        predicted_category = "stew and side"
        print("stew and side")
        result = generate_quantities_to_stew_side(arrIngredients)
    result = converts_grams_to_the_appropriate_unit(result)
    result.append(predicted_category)
    return result

if __name__ == '__main__':
    arr = ["potatoes", "sugar", "olive oil", "onion", "salt", "entrecote", "sea bass", "carp", "beef schnitzel"]
    # print(arr)
    # arr = adapting_the_products_to_the_existing_products(arr)
    # print(arr)
    # result = normalization_of_data_from_the_user(arr)
    # result2, result2_sum = sending_to_the_model(result)
    # result2 = result2[0]
    # print(result2)
    # print(result2_sum)
    # print(the_final_prediction_result(result2))


