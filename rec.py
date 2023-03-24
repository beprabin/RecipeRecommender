import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

foods = pd.read_csv('FoodIngredients.csv', nrows=200)
# foods.head(1)['Ingredients']

# nltk.download('stopwords')
foods['Ingredients'] = foods['Ingredients'].str.lower()

",".join(stopwords.words('english'))
stop_words = set(stopwords.words('english'))


def remove_stop(x):
    return " ".join([word for word in str(x).split() if word not in stop_words])


filtered_ing = foods['Ingredients'].apply(lambda x: remove_stop(x))

tfv = TfidfVectorizer(min_df=3, max_features=None,
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                      ngram_range=(1, 3),
                      stop_words='english')

foods_cleaned_df = foods['Ingredients'].fillna('')
tfv_matrix = tfv.fit_transform(foods_cleaned_df)
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

indices = pd.Series(foods_cleaned_df.index, index=foods['Title'])


def giv_rec(title, sig=sig):
    idx = indices[title]

    sig_scores = list(enumerate(sig[idx]))

    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    sig_scores = sig_scores[1:11]

    food_indices = [i[0] for i in sig_scores]

    # data = []
    # for i in food_indices:
    #     item = []

    #     item.extend(list(foods_cleaned_df('foods')['Title'].values))
    #     item.extend(list(foods_cleaned_df('foods')['Image_Name'].values))
    #     item.extend(list(foods_cleaned_df('foods')['Instruction'].values))
    #     item.extend(list(foods_cleaned_df('foods')['Ingredients'].values))

    #     data.append(item)

    # return data
    # print(food_indices)
    items = []
    recom = pd.DataFrame(columns=['title', 'image', 'ingredients', 'instructions'])
    count = 0
    for i in food_indices:
        recom.at[count, 'title'] = foods['Title'].iloc[i]
        recom.at[count, 'image'] = foods['Image_Name'].iloc[i]
        recom.at[count, 'ingredients'] = foods['Ingredients'].iloc[i]
        recom.at[count, 'instructions'] = foods['Instructions'].iloc[i]
        count += 1
    return recom
    # data = []
    # item = []
    # item.append(foods['Title'].iloc[food_indices])
    # item.append(foods['Image_Name'].iloc[food_indices])
    # item.append(foods['Ingredients'].iloc[food_indices])
    # item.append(foods['Instructions'].iloc[food_indices])
    #
    # data.append(item)
    #
    # return data


print(giv_rec('Thanksgiving Mac and Cheese'))
