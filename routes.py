from flask import (
    render_template,
    redirect,
    flash,
    url_for,
    session
)
import pickle
from extra.likes import *
from flask import request
import sqlite3
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import check_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from extra.models import User, Favourite
from extra.forms import login_form, register_form

foodlist = pickle.load(open('list.pkl', 'rb'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@app.route('/', methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template('hero.html',
                           food_name=foodlist['Title'].values,
                           image=foodlist['Image_Name'].values,
                           ingredient=foodlist['Ingredients'].values,
                           instruction=foodlist['Instructions'].values,
                           )

@app.route('/recs')
def rec():
    if request.method == "GET":
        df = pd.read_csv('FoodIngredients.csv', nrows=200)
        l = []
        count = 0
        for i in range(len(df)):
            l = l.append(df['Title'].iloc(count))
            count += 1

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


# @app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
# def login():
#     form = login_form(request.form)
#
#     if form.validate_on_submit():
#         try:
#             user = User.query.filter_by(email=form.email.data).first()
#             if check_password_hash(user.pwd, form.pwd.data):
#                 login_user(user)
#                 return redirect(url_for('index'))
#             else:
#                 flash('Invalid Username or Password!', "danger")
#         except Exception as e:
#             flash(e, "danger")
#
#     return render_template("login.html")
@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login"
                           )


# @app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
# def register():
#     form = RegisterForm()
#     print(form.email.data)
#     if form.validate_on_submit():
#         email = form.email.data
#         pwd = form.pwd.data
#         username = form.username.data
#
#         newuser = User(
#             username=username,
#             email=email,
#             pwd=bcrypt.generate_password_hash(pwd),
#         )
#
#         db.session.add(newuser)
#         db.session.commit()
#         flash(f"Account Successfully Created", "success")
#         return redirect(url_for("login"))
#
#     return render_template("auth.html", form=form)
#

@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Successfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occurred !", "danger")
    return render_template("auth.html",
                           form=form,
                           text="Create account",
                           title="Register",
                           btn_action="Register account"
                           )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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


def get_likes(user_id):
    # conn = get_db_connection()
    # #likes = conn.execute(' SELECT * FROM favourites WHERE user_id = 1').fetchall()
    # query = f'''SELECT * FROM favourite WHERE user_id = {user_id}'''
    # like = conn.execute(query).fetchall()
    # conn.close()
    # like = Favourite.query.get_or_404(user_id)
    like = db.session.query(Favourite).all()
    # like = [l.recipe for l in like]
    # t = []
    # for n in like:
    #     t.append(n['title'])
    l = [r for r in like]
    print(like)
    result = get_likes_data(l)
    print(result)
    return result


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/user/liked/add/')
@login_required
def add_fav(recipe_name):
    user_id = request.form['userid']
    recipe = request.form['recipe']
    favourite = Favourite(user_id=user_id,
                          recipe=recipe)
    db.session.add(favourites)
    db.session.commit()
    return redirect(url_for('recipe'))


if __name__ == '__main__':
    app.run(debug=True)
