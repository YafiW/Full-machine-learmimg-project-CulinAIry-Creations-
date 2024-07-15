import re
from fractions import Fraction

measurement_words = ['tablespoons', 'tablespoon', 'pound', 'pounds', 'teaspoon', 'teaspoons',
                            'cup', 'cups', 'tsp', 'oz', 'tbsp', 'lb', 'lbs', 'ml', 'g', 'l', 'gallon',
                            'chunks', 'kg', 'room', 'kgs', 'kilogram', 'tbsp.', 'tsp.',
                            'box', 'package', 'packages', 'ounce', 'ounces', 'spoon', 'spoons',
                            'liters', 'fl', 'grams', 'gram', 'kilograms', 'half', 'jar', 'pinch', 'pitcher']


def find_measurement_word_in_some_cell(cell_with_cleaned_ingredient):
    cell_content = cell_with_cleaned_ingredient.lower()
    for word in measurement_words:

        if re.search(r'\b' + re.escape(word) + r'\b', cell_content):
            return word
    return None


def extract_closest_number_to_word(sentence, word):

    number_pattern = r'-?\d+/\d+|-?\d+\.?\d*'

    sentence = sentence.lower()

    word_index = sentence.find(word)
    number_positions = [(m.group(), m.start()) for m in re.finditer(number_pattern, sentence)]

    closest_number = None
    smallest_distance = float('inf')

    for number, number_pos in number_positions:
        if number_pos < word_index and word_index - number_pos < smallest_distance:
            closest_number = number
            smallest_distance = word_index - number_pos

    if closest_number is not None:
        return Fraction(closest_number)

    return 1

text = '3 Tbsp. apple cider vinegar'
result = find_measurement_word_in_some_cell(text)
print("Result:", result)