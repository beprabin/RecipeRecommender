from flask import Flask
import pickle
from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session
)
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

# login_manager = LoginManager()
# login_manager.session_protection = "strong"
# login_manager.login_view = "login"
# login_manager.login_message_category = "info"
#
# db = SQLAlchemy()
# migrate = Migrate()
# bcrypt = Bcrypt()

foodlist = pickle.load(open('list.pkl', 'rb'))
sig = pickle.load(open('sig.pkl', 'rb'))
app = Flask(__name__)


# def create_app():

#     app.secret_key = 'secret-key'
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#
#     login_manager.init_app(app)
#     db.init_app(app)
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)
#
#     return app

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

    indices = pd.Series(foodlist.index, index=foodlist['Title'].values)

    idx = indices[user_input]
    # print(idx)
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

    sig_scores = list(enumerate(sig[idx]))

    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    sig_scores = sig_scores[1:11]

    # print(sig_scores)

    food_indices = [i[0] for i in sig_scores]

    # datas=foodlist.iloc[food_indices]
    recom = pd.DataFrame(columns=['id', 'title', 'image', 'ingredients', 'instructions'])
    count = 0
    for i in food_indices:
        recom.at[count, 'id'] = i
        recom.at[count, 'Title'] = foodlist['Title'].iloc[i]
        recom.at[count, 'Image_Name'] = foodlist['Image_Name'].iloc[i]
        recom.at[count, 'Ingredients'] = foodlist['Ingredients'].iloc[i]
        recom.at[count, 'Instructions'] = foodlist['Instructions'].iloc[i]
        count += 1
    print(recom['id'])

    return render_template('recommend.html',
                           id=recom['id'].values,
                           food_name=recom['Title'].values,
                           image=recom['Image_Name'].values,
                           ingredient=recom['Ingredients'].values,
                           instruction=recom['Instructions'].values)


@app.route('/selected-item/<id>')
def selected_item(id):
    item = pd.DataFrame(columns=['id', 'title', 'image', 'ingredients', 'instructions'])

    # item.at[id, 'id'] = id
    print(id)
    item.at[0, 'Title'] = foodlist['Title'].iloc[int(id)]
    item.at[0, 'Image_Name'] = foodlist['Image_Name'].iloc[int(id)]
    item.at[0, 'Ingredients'] = foodlist['Ingredients'].iloc[int(id)]
    item.at[0, 'Instructions'] = foodlist['Instructions'].iloc[int(id)]

    return render_template('selecteditem.html',
                           food_name=item['Title'].values,
                           image=item['Image_Name'].values,
                           ingredient=item['Ingredients'].values,
                           instruction=item['Instructions'].values)


# @app.route('/')
# def index():
#     return render_template('hero.html',
#                            food_name=foodlist['Title'].values,
#                            image=foodlist['Image_Name'].values,
#                            ingredient=foodlist['Ingredients'].values,
#                            instruction=foodlist['Instructions'].values,
#                            )
#
#
# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')
#
#
# @app.route('/recipe/<title>')
# def show_recipe(title):
#     return render_template('ingredients.html', title=title)
#

# @app.route('/recommend_foods', methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     # return str(user_input)
#     tfv = TfidfVectorizer(min_df=3, max_features=None,
#                           strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
#                           ngram_range=(1, 3),
#                           stop_words='english')
#
#     foods_cleaned_df = foodlist['Ingredients'].fillna('')
#
#     tfv_matrix = tfv.fit_transform(foods_cleaned_df)
#
#     indices = pd.Series(foodlist.index, index=foodlist['food_name'].values)
#
#     idx = indices[foodlist]
#
#     sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
#
#     sig_scores = list(enumerate(sig[1]))
#
#     sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
#
#     sig_scores = sig_scores[1:11]
#
#     food_indices = [i[0] for i in sig_scores]
#
#     data = []
#     item = []
#     item.append(foodlist['Title'].iloc[food_indices])
#     item.append(foodlist['Image_Name'].iloc[food_indices])
#     item.append(foodlist['Ingredients'].iloc[food_indices])
#     item.append(foodlist['Instructions'].iloc[food_indices])
#
#     data.append(item)
#
#     print(data)
#
#     return data
#

# @app.route('/user/liked/<userid>')
# def favourites(userid):
#     likes = get_likes(userid)
#     return render_template('favourite.html', data=likes['title'].values, images=likes['image'].values)
#
#
# def get_likes(userid):
#     conn = get_db_connection()
#     # likes = conn.execute(' SELECT * FROM favourites WHERE user_id = 1').fetchall()
#     query = f'''SELECT * FROM favourites WHERE user_id = {userid}'''
#     like = conn.execute(query).fetchall()
#     conn.close()
#     t = []
#     for n in like:
#         t.append(n['title'])
#     result = get_likes_data(t)
#     return result
#
#
# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn


if __name__ == '__main__':
    app.run(debug=True)
