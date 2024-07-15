import pandas as pd
import nltk
import ast

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

FILE_DB_PATH_BEF = r'..\Files\‏‏‏‏Food Ingredients and Recipe Dataset - change - עותק.csv'
FILE_DB_PATH_AFTER = r'..\Files\‏‏‏‏‏‏Food Ingredients and Recipe Dataset - after עותק.csv'

def deletes_lines_without_category_from_the_file():
    df = pd.read_csv(FILE_DB_PATH_BEF)

    df_filtered = df.dropna(subset=['category'])

    df_filtered.to_csv(r'..\Files\‏‏Food Ingredients and Recipe Dataset - after.csv', index=False)


def filter_measurement_words(words):

    common_measurement_words = ['big', 'small', 'tablespoons', 'tablespoon', 'pound', 'pounds', 'teaspoon', 'teaspoons',
                                'cup', 'cups', 'tsp', 'oz', 'tbsp', 'plus', 'more', 'lb', 'lbs', 'ml', 'g', 'l', 'whole',
                                'end', 'medium', 'large', 'inch', 'gallon', 'extra', 'chunks', 'pieces', 'kg', 'room',
                                'temperature', 'box', 'package', 'packages', 'ounce', 'ounces', 'parts', 'spoon',
                                'liters', 'fl', 'grams', 'gram', 'kilograms', 'half', 'cut', 'lengthwise', 'strips',
                                'crosswise', 'jar', 'pinch', 'pitcher']
    return [word for word in words if word.lower() not in common_measurement_words and word.isalpha()]

def noun_identifier(ingredients):
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(ingredients)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos) ]
    return nouns

def find_or_index(text):
    return text.find("or")


def remove_repeated_words(string):
    string_lower = string.lower()
    words = string_lower.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    repeated_words = set(word for word, count in word_count.items() if count > 1)
    cleaned_words = ['' if word in repeated_words else word for word in words]
    cleaned_string = ' '.join(cleaned_words).strip()

    return cleaned_string

def split_arr_of_ingredients_from_recipe():
    arr_ingredients = []
    df = pd.read_csv(FILE_DB_PATH_AFTER)
    column_values = df.iloc[:, 3]
    for value in column_values:
        array_ingredients = ast.literal_eval(value)
        for ingredient in array_ingredients:
            nouns_from_ingredients = noun_identifier(ingredient)
            filter_nouns_from_ingredients = filter_measurement_words(nouns_from_ingredients)
            index_or = find_or_index(ingredient)
            if index_or != -1:
                before_or = " ".join(filter_nouns_from_ingredients[:index_or])
                after_or = " ".join(filter_nouns_from_ingredients[index_or + 1:])
                before_or = remove_repeated_words(before_or)
                after_or = remove_repeated_words(after_or)
                arr_ingredients.append(before_or)
                arr_ingredients.append(after_or)
            else:
                str_filter_nouns_from_ingredients = ' '.join(filter_nouns_from_ingredients)
                str_filter_nouns_from_ingredients = remove_repeated_words(str_filter_nouns_from_ingredients)
                arr_ingredients.append(str_filter_nouns_from_ingredients)

    return arr_ingredients


def remove_duplicates_and_empty_strings(arr_ingredients):

    arr_lower = [s.lower().strip() for s in arr_ingredients]
    unique_non_empty_strings = set(filter(None, arr_lower))
    return list(unique_non_empty_strings)


def add_columns_of_ingredients_to_DB(arr_ingredients):
    df = pd.read_csv(FILE_DB_PATH_AFTER)
    product_dfs = [pd.DataFrame({product: [''] * len(df)}) for product in arr_ingredients]
    df = pd.concat([df] + product_dfs, axis=1)
    df.to_csv(FILE_DB_PATH_AFTER, index=False)


def add_noun_ingredients_column():
    cleaned_ingredients_column_index = 3
    df = pd.read_csv(FILE_DB_PATH_AFTER)
    filtered_ingredients_per_row = []
    for index, row in df.iterrows():
        array_ingredients_per_line = []
        str_ingredients = row[df.columns[cleaned_ingredients_column_index]]
        array_ingredients = ast.literal_eval(str_ingredients)

        for ingredient in array_ingredients:
            nouns_from_ingredient = noun_identifier(ingredient)
            filter_nouns_from_ingredients = filter_measurement_words(nouns_from_ingredient)
            index_or = find_or_index(ingredient)
            if index_or != -1:
                before_or = " ".join(filter_nouns_from_ingredients[:index_or])
                after_or = " ".join(filter_nouns_from_ingredients[index_or + 1:])
                before_or = remove_repeated_words(before_or)  # Assuming this function is defined elsewhere
                after_or = remove_repeated_words(after_or)
                array_ingredients_per_line.append(before_or)
                array_ingredients_per_line.append(after_or)
            else:
                str_filter_nouns_from_ingredients = ' '.join(filter_nouns_from_ingredients)
                str_filter_nouns_from_ingredients = remove_repeated_words(str_filter_nouns_from_ingredients)
                array_ingredients_per_line.append(str_filter_nouns_from_ingredients)
        array_ingredients_per_line = remove_duplicates_and_empty_strings(array_ingredients_per_line)
        filtered_ingredients_per_row.append(array_ingredients_per_line)
    df['filtered_ingredients'] = filtered_ingredients_per_row
    df.to_csv(FILE_DB_PATH_AFTER, index=False)

if __name__ == '__main__':
     deletes_lines_without_category_from_the_file()
     arr_of_ingredients = split_arr_of_ingredients_from_recipe()
     arr_of_ingredients2 = remove_duplicates_and_empty_strings(arr_of_ingredients)
     print(len(arr_of_ingredients2))
     add_columns_of_ingredients_to_DB(arr_of_ingredients2)
     add_noun_ingredients_column()
