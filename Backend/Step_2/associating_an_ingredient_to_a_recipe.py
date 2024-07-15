import pandas as pd
import ast

FILE_DB_PATH_AFTER = r'..\Files\‏‏Food Ingredients and Recipe Dataset - after.csv'
def mark_0_or_1_in_the_ingredients_columns():

    df = pd.read_csv(FILE_DB_PATH_AFTER)


    for index, row in df.iterrows():
        filtered_ingredients = row['filtered_ingredients']
        array_filtered_ingredients = ast.literal_eval(filtered_ingredients)
        existing_filtered_ingredients = df.columns.intersection(array_filtered_ingredients)
        for ingredient in existing_filtered_ingredients:
            try:
                df.at[index, ingredient] = 1
            except Exception as e:
                continue

    for index, row in df.iterrows():
        for column in df.columns:
            if pd.isna(row[column]):
                df.at[index, column] = 0

    df.to_csv(FILE_DB_PATH_AFTER, index=False)

def count_cells_with_1_in_row(row_index):
    df = pd.read_csv(FILE_DB_PATH_AFTER)
    row = df.iloc[row_index]
    count_ones = (row == 1).sum()
    print(row['Title'])
    return count_ones

def sum_column(column_name):
    df = pd.read_csv(FILE_DB_PATH_AFTER)

    column_sum = df[column_name].sum()

    return column_sum

if __name__ == '__main__':
    count_ones = count_cells_with_1_in_row(4494)
    print(count_ones)
    #mark_0_or_1_in_the_ingredients_columns()

