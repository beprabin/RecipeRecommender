import pandas as pd

def get_ingredients(titles):
    recipes = pd.read_csv('FoodIngredients.csv', nrows=200)
    df = pd.DataFrame(columns=['title', 'image','ingredients','instructions'])
    count = 0
    for title in titles:
        for i in range(len(recipes)):
        # print(titles)
            if recipes.loc[i, 'Title'] == title:

                 df.at[count, 'title'] = recipes['Title'].iloc[i]
                 df.at[count, 'image'] = recipes['Image_Name'].iloc[i]
                 df.at[count, 'ingredients'] = recipes['Ingredients'].iloc[i]
                 df.at[count, 'instructions'] = recipes['Instructions'].iloc[i]
                 count += 1
    return df


print(get_ingredients(['Thanksgiving Mac and Cheese']))





