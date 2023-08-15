from flask import Flask, redirect, url_for, request, render_template
from forms import RecipeForm
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['RECIPE_DATA'] = os.path.join('static', 'data_dir','')
app.config['RECIPE_IMG'] = os.path.join('static', 'image_dir','')

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/recipes')
def view_recipes():
    recipes = []
    for file in os.listdir(app.config['RECIPE_DATA']):
        if file.endswith('.csv'):
            recipe = pd.read_cvs(os.path.join(app.config['RECIPE_DATA'], file)).iloc[0]
            recipes.append(recipe)
    return render_template('recipes.html', recipes=recipes)

@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        ingredients = form.ingredients.data
        prep_instructions = form.preparation_instructions.data
        img_filename = secure_filename(form.image.data.filename)
        form.image.data.save(os.path.join(app.config['RECIPE_IMG'], img_filename))
        df = pd.DataFrame([{
            'name': recipe_name,
            'ingredients': ingredients,
            'prep_instructions': prep_instructions,
            'serving_instructions': serving_instructions,
            'image': img_filename
        }])
        df.to_csv(os.path.join(app.config['RECIPE_DATA'], recipe_name.replace(" ", "_") + '.csv'), index=False)
        return render_template('add_recipe.html', form=form)

    if __name__ == '__main__':
        app.run(debug=True)



