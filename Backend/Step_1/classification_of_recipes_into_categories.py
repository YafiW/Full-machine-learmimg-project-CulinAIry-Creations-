import pandas as pd
import numpy as np
import csv
FILE_PATH=r'../Files/__Food Ingredients and Recipe Dataset - after2.csv'
def removesUnnecessaryColumnsFromTheData():
    df = pd.read_csv(FILE_PATH)

    df.drop(columns=['Ingredients'], inplace=True)

    df.drop(columns=['Image_Name'], inplace=True)

    df.to_csv(FILE_PATH, index=False)


def addCategoryColumn():
    df = pd.read_csv(FILE_PATH)
    df['category'] = float('nan')
    df.to_csv(FILE_PATH, index=False)



def classifyingARecipeIntoACategory():
    df = pd.read_csv(FILE_PATH)
    stew_and_side_dishes_list = []
    salad_list = []
    cakes_list = []
    meat_and_chicken_and_fish_list = []

    title_column_index = 1
    df['category'] = df['category'].astype('object')
    for index, row in df.iterrows():
        try:
            title = row[df.columns[title_column_index]]

            if any(keyword.lower() in title.lower() for keyword in
                   ["salad", "caesar", "nicoise", "greens", "cucumber"]):
                df.at[index, 'category'] = "salad"
                salad_list.append(row)

            elif any(keyword.lower() in title.lower() for keyword in
                     ["cake", "pie", "tart", "dough", "croissant", "puff pastry", "strudel", "pastry",
                      "fudge", "cupcake", "bars", "brownies", "bread pudding","chocolate"]):
                df.at[index, 'category'] = "cake"
                cakes_list.append(row)

            elif any(keyword.lower() in title.lower() for keyword in
                   ["meat", "chicken", "braised", "pork", "lamb","turkey","duck","goose","venison", "bison", "quail"
                    ,"pheasant", "veal", "guinea fowl", "ostrich", "emu", "elk", "these", "meat balls",
                    "meatballs", "beef"
                    ,"salmon", "dennis",
                    "trout", "tuna", "cod", "bass", "mackerel", " haddock", "snapper", "halibut", "sardine", "carp",
                    "tilapia"]):
                df.at[index, 'category'] = "meat_and_chicken_and_fish_list"
                meat_and_chicken_and_fish_list.append(row)


            elif any(keyword.lower() in title.lower() for keyword in
                   ["stew", "cook", "soup", "casserole", "simmer", "slow cooked", "gumbo","pasta", "rice", "beans",
                    "potato", "flakes"]):
                df.at[index, 'category'] = "stew_and_side_dishes_list"
                stew_and_side_dishes_list.append(row)


        except Exception as e:

            continue

    df.to_csv(FILE_PATH, index=False)
    return (stew_and_side_dishes_list, cakes_list, salad_list, meat_and_chicken_and_fish_list)

if __name__ == '__main__':

    result1, result2, result3, result4 = classifyingARecipeIntoACategory()
    print(len(result1+result2+result3+result4))
