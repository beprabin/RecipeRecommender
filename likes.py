import pandas as pd


def get_likes_data(titles):
    recipes = pd.read_csv('FoodIngredients.csv', nrows=200)
    df = pd.DataFrame(columns=['title', 'image'])
    count = 0
    for title in titles:
        for i in range(len(recipes)):
            if recipes.loc[i, 'Title'] == title:
                print(recipes.loc[i, 'Title'])
                # values.append(recipes.loc[i])
                df.at[count, 'title'] = recipes['Title'].iloc[i]
                df.at[count, 'image'] = recipes['Image_Name'].iloc[i]
                count += 1
    return df


print(get_likes_data(['Thanksgiving Mac and Cheese', 'Apples and Oranges']))
