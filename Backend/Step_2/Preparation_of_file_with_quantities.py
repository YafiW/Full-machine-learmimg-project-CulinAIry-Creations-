import pandas as pd
import re
import ast
from fractions import Fraction
import math

FILE_DB_PATH = r'..\Files\‏‏Food Ingredients and Recipe Dataset - after.csv'
FILE_DB_WITH_Q = r'..\Files\‏‏‏‏Food Ingredients and Recipe Dataset -with full quantities.csv'
FILE_DB_WITH_Q_ON_GRAMS = r'..\Files\‏‏‏‏‏‏Food Ingredients and Recipe Dataset -with grams.csv'
measurement_words = ['tablespoons', 'tablespoon', 'pound', 'pounds', 'teaspoon', 'teaspoons',
                            'cup', 'cups', 'tsp', 'oz', 'tbsp', 'lb', 'lbs', 'ml', 'g', 'l', 'gallon',
                            'chunks', 'kg', 'kgs', 'kilogram', 'tbsp.', 'tsp.',
                            'box', 'package', 'packages', 'ounce', 'ounces', 'spoon', 'spoons',
                            'liters', 'fl', 'grams', 'gram', 'kilograms', 'half', 'jar', 'pinch', 'pitcher']


def filter_ingredient_in_cleaned_ingredients(array, string):
    words = string.split()
    words_lower = [word.lower() for word in words]
    for index, cell in enumerate(array):
        cell_lower = cell.lower()
        if all(word in cell_lower for word in words_lower):
            return index
    return -1
def find_measurement_word_in_some_cell(cell_with_cleaned_ingredient):
    cell_with_cleaned_ingredient = str(cell_with_cleaned_ingredient)
    cell_content = cell_with_cleaned_ingredient.lower()
    for word in measurement_words:

        if re.search(r'\b' + re.escape(word) + r'\b', cell_content):
            return word
    return None



def extract_number_before_word(sentence, word):
    number_pattern = r'-?\d+/\d+|-?\d+\.?\d*'
    sentence = sentence.lower()
    word_index = sentence.find(word)
    number_positions = [(m.group(), m.start()) for m in re.finditer(number_pattern, sentence)]
    closest_number = None
    smallest_distance = float('inf')
    for number, number_pos in number_positions:
        # בודק אם המספר שמצא נמצא לפני מילת המדידה, וגם בודק אם הוא הכי קרוב שאפשר למילה
        if number_pos < word_index and word_index - number_pos < smallest_distance:
            closest_number = number
            smallest_distance = word_index - number_pos
    if closest_number is not None:
        return Fraction(closest_number)

    return 1

def extract_first_number(text):

    pattern = r'-?\d+\.?\d*'
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


def extract_the_number_from_cell(sentence):

    number_pattern = re.compile(r'\b\d+(?:\.\d+)?(?:/\d+)?\b')
    match = number_pattern.search(sentence)

    if match:
        match_str = match.group()

        if '/' in match_str:
            return float(Fraction(match_str))
        elif '.' in match_str:
            return float(match_str)
        else:
            return int(match_str)
    else:
        return None


def round_number_or_fraction(value):
    try:
        fraction = Fraction(value)
        numerator = fraction.numerator
        denominator = fraction.denominator
        float_value = float(fraction)
        if numerator % denominator == denominator / 2:
            if float_value > 0:
                return math.ceil(float_value)
            else:
                return math.floor(float_value)
        else:
            return round(float_value)
    except ValueError:
        try:
            float_value = float(value)
            return round(float_value)
        except ValueError:
            raise ValueError("Input must be a whole number or a fraction")

def analyzing_measurement_unit_from_ingredients_column():
    df = pd.read_csv(FILE_DB_PATH)
    df2 = pd.read_csv(FILE_DB_WITH_Q)
    updates = []
    for i, (row1, row2) in enumerate(zip(df.itertuples(index=False), df2.itertuples(index=False))):
        cleaned_ingredients = ast.literal_eval(row1.Cleaned_Ingredients)
        filtered_ingredients = ast.literal_eval(row1.filtered_ingredients)

        for filtered_ingredient in filtered_ingredients:
            ind = filter_ingredient_in_cleaned_ingredients(cleaned_ingredients, filtered_ingredient)
            if ind != -1:
                measurement_word = find_measurement_word_in_some_cell(cleaned_ingredients[ind])
                if measurement_word is not None and filtered_ingredient in df2.columns:
                    number1 = extract_number_before_word(cleaned_ingredients[ind], measurement_word)
                    if number1 is not None:
                        value = str(number1) + " " + measurement_word
                        updates.append((i, filtered_ingredient, value))
                else:
                    number = extract_first_number(cleaned_ingredients[ind])
                    if number is not None:
                        updates.append((i, filtered_ingredient, str(number)))
                    else:
                        value2 = str(1) + " " + 'g'
                        updates.append((i, filtered_ingredient, value2))

    for row, column, value in updates:
        if column in df2.columns:
            if df2[column].dtype != 'object':
                df2[column] = df2[column].astype(str)
            df2.at[row, column] = value
            print(row, column, value)

    df2.to_csv(FILE_DB_WITH_Q, index=False)



def convert_measurement_unit_to_grams():
    df1 = pd.read_csv(FILE_DB_WITH_Q)
    df2 = pd.read_csv(FILE_DB_WITH_Q_ON_GRAMS)
    updates = []


    for i, (row1, row2) in enumerate(zip(df1.itertuples(index=False), df2.itertuples(index=False))):
        filtered_ingredients = row1.filtered_ingredients
        filtered_ingredients = ast.literal_eval(filtered_ingredients)
        for ingredient in filtered_ingredients:
            ingredient_content = df1.at[i, ingredient]
            if ingredient_content is not None:
                measurement_unit = find_measurement_word_in_some_cell(ingredient_content)
                if measurement_unit is not None:
                    quantity = extract_the_number_from_cell(ingredient_content)

                    if (measurement_unit == 'tablespoon' or measurement_unit == 'tablespoons' or measurement_unit == 'tbsp'
                            or measurement_unit == 'spoon' or measurement_unit == 'spoons'):
                        quantity_in_grams = quantity * 10
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif measurement_unit == 'teaspoon' or measurement_unit == 'teaspoons' or measurement_unit == 'tsp':
                        quantity_in_grams = quantity * 4
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif measurement_unit == 'half':
                        quantity_in_grams = quantity * 100
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif (measurement_unit == 'pound' or measurement_unit == 'pounds' or measurement_unit == 'lb'
                          or measurement_unit == 'lbs'):
                        quantity_in_grams = quantity * 453
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif (measurement_unit == 'cup' or measurement_unit == 'cups' or measurement_unit == 'box'
                          or measurement_unit == 'package' or measurement_unit == 'packages' or measurement_unit == 'chunks'):
                        quantity_in_grams = quantity * 200
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif measurement_unit == 'pitcher' or measurement_unit == 'jar':
                        quantity_in_grams = quantity * 500
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif (measurement_unit == 'oz' or measurement_unit == 'ounce' or measurement_unit == 'ounces'
                          or measurement_unit == 'fl'):
                        quantity_in_grams = quantity * 28
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif (measurement_unit == 'kg' or measurement_unit == 'kgs' or measurement_unit == 'kilogram'
                          or measurement_unit == 'kilograms' or measurement_unit == 'l' or measurement_unit == 'liter'
                          or measurement_unit == 'liters'):
                        quantity_in_grams = quantity * 1000
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif (measurement_unit == 'g' or measurement_unit == 'grams' or measurement_unit == 'gram'
                          or measurement_unit == 'ml' or measurement_unit == 'pinch'):
                        quantity_in_grams = quantity
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))
                    elif measurement_unit == 'gallon':
                        quantity_in_grams = quantity * 4000
                        quantity_in_grams = round_number_or_fraction(quantity_in_grams)
                        updates.append((i, ingredient, quantity_in_grams))

    for row, column, value in updates:
        if column in df2.columns:
            if df2[column].dtype != 'object':
                df2[column] = df2[column].astype(str)
            df2.at[row, column] = value
            print(row, column, value, type(value))

    df2.to_csv(FILE_DB_WITH_Q_ON_GRAMS, index=False)

if __name__ == '__main__':
    #analyzing_measurement_unit_from_ingredients_column()
    convert_measurement_unit_to_grams()
