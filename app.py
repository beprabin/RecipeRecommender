from flask import Flask, render_template,request
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

foodlist = pickle.load(open('list.pkl','rb'))
sig = pickle.load(open('sig.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hero.html',
                            food_name = foodlist['Title'].values,
                            image = foodlist['Image_Name'].values,
                            ingredient = foodlist['Ingredients'].values,
                            instruction = foodlist['Instructions'].values,
                          )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_foods', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # return str(user_input)
    tfv = TfidfVectorizer(min_df=3, max_features=None,
            strip_accents ='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1,3),
            stop_words= 'english')                 

    foods_cleaned_df = foodlist['Ingredients'].fillna('')

    tfv_matrix = tfv.fit_transform(foods_cleaned_df)
    
    indices = pd.Series(foodlist.index, index=foodlist['Title'].values)
    
    idx = indices[user_input]
    # print(idx)
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    
    sig_scores = list(enumerate(sig[idx]))
    
    sig_scores = sorted(sig_scores ,key=lambda x: x[1], reverse=True)
    
    sig_scores = sig_scores[1:11]

    # print(sig_scores)

    food_indices = [i[0] for i in sig_scores]
    
    # datas=foodlist.iloc[food_indices]
    recom = pd.DataFrame(columns=['id','title', 'image', 'ingredients', 'instructions'])
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
                            id = recom['id'].values,
                            food_name = recom['Title'].values,
                            image = recom['Image_Name'].values,
                            ingredient = recom['Ingredients'].values,
                            instruction = recom['Instructions'].values)

@app.route('/selected-item/<id>')
def selected_item(id):
    item = pd.DataFrame(columns=['id','title', 'image', 'ingredients', 'instructions'])
    
    # item.at[id, 'id'] = id
    print(id)
    item.at[0, 'Title'] = foodlist['Title'].iloc[int(id)]
    item.at[0, 'Image_Name'] = foodlist['Image_Name'].iloc[int(id)]
    item.at[0, 'Ingredients'] = foodlist['Ingredients'].iloc[int(id)]
    item.at[0, 'Instructions'] = foodlist['Instructions'].iloc[int(id)]

    return render_template('selecteditem.html', 
                        food_name = item['Title'].values,
                        image = item['Image_Name'].values,
                        ingredient = item['Ingredients'].values,
                        instruction = item['Instructions'].values)
    
if __name__ == '__main__':
    app.run(debug=True)