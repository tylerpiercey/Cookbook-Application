from flask import Flask, redirect, url_for, request, render_template
from forms import RecipeForm
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['RECIPE_DATA'] = os.path.join('static', 'RECIPE_DATA', '')
app.config['RECIPE_IMG'] = os.path.join('static', 'RECIPE_IMG', '')


@app.route('/')
def homepage():
    form = RecipeForm()
    return render_template('index.html', form=form)


@app.route('/recipes')
def view_recipes():
    form = RecipeForm()
    recipes = []
    for file in os.listdir(app.config['RECIPE_DATA']):
        if file.endswith('.csv'):
            recipe = pd.read_csv(os.path.join(app.config['RECIPE_DATA'], file)).iloc[0].to_dict()
            recipes.append(recipe)
    return render_template('recipes.html', form=form, recipes=recipes)


@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        ingredients = form.ingredients.data
        prep_instructions = form.preparation_instructions.data
        serving_instructions = form.serving_instructions.data
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
        return redirect(url_for('view_recipes'))
    print(form.errors)
    return render_template('add_recipe.html', form=form)


@app.route('/delete_recipe/<recipe_name>', methods=['POST'])
def delete_recipe(recipe_name):
    try:
        os.remove(os.path.join(app.config['RECIPE_DATA'], recipe_name.replace(" ", "_") + '.csv'))
    except Exception as e:
        print(e)
    return redirect(url_for('view_recipes'))


@app.route('/search', methods=['GET', 'POST'])
def search_recipes():
    if request.method == "POST":
        query = request.form.get('query')
        matching_recipes = []
        for file in os.listdir(app.config['RECIPE_DATA']):
            if file.endswith('.csv'):
                recipe = pd.read_csv(os.path.join(app.config['RECIPE_DATA'], file)).iloc[0]
                if query.lower() in recipe['name'].lower() or query.lower() in recipe['ingredients'].lower():
                    matching_recipes.append(recipe)
        return render_template('recipes.html', recipes=matching_recipes)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
