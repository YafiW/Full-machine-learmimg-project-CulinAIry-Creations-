import os
import pandas as pd
def get_photo_names(folder_path):
    photo_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):  # Adjust file extensions as needed
                photo_name, ext = os.path.splitext(file)
                photo_name = photo_name.replace('-', ' ').replace('_', ' ')
                photo_name = photo_name.lower()
                photo_names.append(photo_name)
    return photo_names



def filter_columns_by_vector():
    df_path = r'../Files/‏‏‏‏binary_recipes - עותק.csv'


    vector = ['bermondi', 'carp', 'dennis', 'mullet', 'salmon', 'sea bass', 'tilapia', 'tuna', 'cheddar', 'chesse',
              'cottage', 'creame cheese', 'eggs', 'feta cheese', 'goat cheese', 'goat yogurt', 'gouda',
              'halloumi cheese', 'milk', 'mozzarellacheese', 'parmesan', 'parmesan shavings', 'resistant milk',
              'ricotta cheese', 'saturation milk', 'sour cream', 'yellow cheese', 'yogurt', 'yogurt bio', 'annuity',
              'apple pear', 'apricot', 'avocado', 'banana', 'blueberries', 'chery', 'clementine', 'golden mellon',
              'green grape', 'green apple', 'hermon apple', 'kiwi', 'lemon', 'loquat', 'majhol', 'mellon', 'nectarine',
              'orange', 'papaya', 'peach', 'pear', 'pineapple', 'pink lady apple', 'pitaya', 'pomelo', 'purple grapes',
              'quince', 'red grapefruit', 'sabers', 'spanish mellon', 'watermellon', 'yellow apple', 'asado',
              'beef schnitzel', 'brisket', 'chicken sausage', 'chicken thighs', 'chicken thighs', 'chicken wings',
              'edges', 'entrecote', 'hamburger', 'chicken breast', 'heart turky', 'lamb shoulder', 'meat ribs', 'mince',
              'mock fillet', 'muscle meat', 'roast beef', 'roast shoulder', 'shoulder cubes', 'sirloin',
              'turkey throat', 'turkey breast', 'turkey turkey', 'turky shawarma', 'turky liver', 'turky thighs',
              'turky wings', 'asparagus', 'beet', 'broccoli', 'cauliflower', 'celery leaves', 'chestnut pumpkin',
              'coriander', 'cucumber', 'dill', 'eggplant', 'garlic', 'ginger', 'green onion', 'green peper', 'guard',
              'head celery', 'hot peper', 'kolorbi', 'leeks', 'lettuce', 'mushrooms', 'nana', 'onion',
              'flour', 'sugar', 'baking powder', 'baking soda', 'yeast', 'cornstarch', 'cream of tartar',
              'cocoa powder',
              'vanilla extract', 'gelatin', 'cornmeal', 'oats', 'baking chocolate', 'rice', 'quinoa', 'barley',
              'couscous', 'bulgur', 'farro', 'millet', 'polenta', 'semolina', 'spaghetti', 'fettuccine', 'penne',
              'macaroni', 'fusilli', 'lasagna', 'egg noodles', 'rice noodles', 'ramen noodles', 'lentils', 'chickpeas',
              'black beans', 'kidney beans', 'pinto beans', 'navy beans', 'split peas', 'soybeans', 'almonds',
              'walnuts',
              'cashews', 'pecans', 'peanuts', 'pumpkin seeds', 'sunflower seeds', 'chia seeds', 'flaxseeds',
              'sesame seeds', 'salt', 'pepper', 'paprika', 'cumin', 'turmeric', 'cinnamon', 'nutmeg', 'cloves',
              'ginger', 'garlic powder', 'onion powder', 'oregano', 'basil', 'thyme', 'rosemary', 'sage', 'bay leaves',
              'chili powder', 'cayenne pepper', 'mustard powder', 'coriander', 'fennel seeds', 'raisins', 'apricots',
              'cranberries', 'dates', 'figs', 'prunes', 'apples', 'mango', 'pineapple', 'banana chips',
              'breakfast cereals', 'cornflakes', 'bran flakes', 'muesli', 'granola', 'pancake mix', 'waffle mix',
              'instant oatmeal', 'popcorn kernels', 'pretzels', 'crackers', 'rice cakes', 'potato chips',
              'tortilla chips',
              'trail mix', 'cake mix', 'brownie mix', 'cookie mix', 'muffin mix', 'bread mix', 'coffee', 'tea',
              'hot chocolate mix', 'dry soup mixes', 'bouillon cubes', 'powdered milk', 'powdered eggs',
              'instant mashed potatoes', 'dehydrated vegetables', 'nonfat dry milk', 'buttermilk powder', 'malt powder',
              'wheat gluten', 'vital wheat gluten']

    vector = [item.lower() for item in vector]

    # Read the data frame from the provided path
    df = pd.read_csv(df_path)

    # Filter columns based on the vector
    columns_to_keep = [col for col in df.columns if any(word in col.lower() for word in vector)]
    df_filtered = df[columns_to_keep]

    # Save the filtered data frame to the specified output path
    df_filtered.to_csv(df_path, index=False)

    num_remaining_columns = len(df_filtered.columns)
    print(f"Number of columns left in the dataframe: {num_remaining_columns}")





def process_dataframe():
    file_binary_path = r'../Files/‏‏‏‏binary_recipes - עותק.csv'
    file_grams_path = r'../Files/‏‏‏‏‏‏‏‏Food Ingredients and Recipe Dataset -with grams - עותק.csv'
    df_binary = pd.read_csv(file_binary_path)
    df_grams = pd.read_csv(file_grams_path)
    rows_to_drop = df_binary[df_binary.eq(1).sum(axis=1) < 4].index

    df_binary.drop(rows_to_drop, inplace=True)
    df_grams.drop(rows_to_drop, inplace=True)

    df_grams.to_csv(file_grams_path, index=False)
    df_binary.to_csv(file_binary_path, index=False)

    print(f"Number of rows left in the df_grams: {df_grams.shape[0]}")

    print(f"Number of rows left in the df_binary: {df_binary.shape[0]}")

def list_files_in_folder(folder_path):

    try:
        # List all files in the specified folder
        files = os.listdir(r'./downloaded_images_vegatables')

        # Filter out directories, only keep files
        file_list = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

        print(file_list)

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def add_columns_to_df():
    # Define the CSV file path
    csv_file = r'../Files/Files_to_Cgan/salad.csv'  # Ensure the correct extension

    # List of filenames with extensions
    columns_names = ['asparagus.jpg', 'beet.webp', 'broccoli.webp', 'cauliflower.webp', 'celery_leaves.webp',
                     'coriander.webp', 'cucumber.jpg', 'dill.webp', 'eggplant.webp', 'garlic.webp',
                     'green_onion.webp', 'green_peper.webp', 'guard.webp', 'hot_peper.webp', 'kohlrabi.webp',
                     'lettuce.webp', 'mushrooms.webp', 'nana.webp', 'onion.webp', 'orange_peper.webp',
                     'parsley.webp', 'purple_cabbage.webp', 'radish.webp', 'red_oninon.webp', 'red_peper.webp',
                     'squash.webp', 'tomato.jpg', 'white_cabbage.webp', 'yellow_peper.webp', 'zucchini.webp',
                     'artichoke.jpg', 'carrot.jpg']

    columns_names = [name.replace('_', ' ') for name in columns_names]
    columns_names = [os.path.splitext(photo)[0].lower() for photo in columns_names]

    # Create DataFrame with these column names
    df = pd.DataFrame(columns=columns_names)

    # Write DataFrame to CSV file
    df.to_csv(csv_file, index=False)

def fill_empty_cells_with_zero():
    # Read the CSV file into a pandas DataFrame
    csv_file = r'../Files/Files_to_Cgan/salad.csv'
    df = pd.read_csv(csv_file)

    # Iterate over each column, starting from the second one

    df = df.fillna(0)

    # Write the modified DataFrame to a new CSV file
    df.to_csv(csv_file, index=False)

def fill_non_zero_cells_with_one():
    csv_file = r'../Files/Files_to_Cgan/‏‏salad - binary.csv'
    # Read the CSV file into a pandas DataFrame, skipping the first row
    df = pd.read_csv(csv_file)

    # Iterate over each column, starting from the second one
    for column in df.columns[:]:
        # Fill non-zero cells in the column with '1'
        df[column] = df[column].apply(lambda x: 1 if x != 0 else x)

    # Write the modified DataFrame to a new CSV file
    df.to_csv(csv_file, index=False)
if __name__ == '__main__':

    #process_dataframe()
    #filter_dataframe_by_another()
    #filter_and_save_dataframe()
    #list_files_in_folder(r'./downloaded_images_vegatables')
    #add_columns_to_df()
    #fill_empty_cells_with_zero()
    fill_non_zero_cells_with_one()