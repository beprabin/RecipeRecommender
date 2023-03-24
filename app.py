from flask import Flask, render_template, request
import pickle
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
from likes import *

foodlist = pickle.load(open('list.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('hero.html',
                           food_name=foodlist['Title'].values,
                           image=foodlist['Image_Name'].values,
                           ingredient=foodlist['Ingredients'].values,
                           instruction=foodlist['Instructions'].values,
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_foods', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # return str(user_input)
    tfv = TfidfVectorizer(min_df=3, max_features=None,
                          strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                          ngram_range=(1, 3),
                          stop_words='english')

    foods_cleaned_df = foodlist['Ingredients'].fillna('')

    tfv_matrix = tfv.fit_transform(foods_cleaned_df)

    indices = pd.Series(foodlist.index, index=foodlist['food_name'].values)

    idx = indices[foodlist]

    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

    sig_scores = list(enumerate(sig[1]))

    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    sig_scores = sig_scores[1:11]

    food_indices = [i[0] for i in sig_scores]

    data = []
    item = []
    item.append(foodlist['Title'].iloc[food_indices])
    item.append(foodlist['Image_Name'].iloc[food_indices])
    item.append(foodlist['Ingredients'].iloc[food_indices])
    item.append(foodlist['Instructions'].iloc[food_indices])

    data.append(item)

    print(data)

    return data


@app.route('/user/liked/<userid>')
def favourites(userid):
    likes = get_likes(userid)
    return render_template('favourite.html', data=likes['title'].values, images=likes['image'].values)


def get_likes(userid):
    conn = get_db_connection()
    # likes = conn.execute(' SELECT * FROM favourites WHERE user_id = 1').fetchall()
    query = f'''SELECT * FROM favourites WHERE user_id = {userid}'''
    like = conn.execute(query).fetchall()
    conn.close()
    t = []
    for n in like:
        t.append(n['title'])
    result = get_likes_data(t)
    return result


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    app.run(debug=True)
