from FlaskForm import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from FlaskForm.file import FileRequired, FileField


class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired(), Length(min=3, max=100)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired(), Length(min=10)])
    preparation_instructions = TextAreaField('Preparation Instructions', validators=[DataRequired(), Length(min=10)])
    serving_instructions = TextAreaField('Serving Instructions', validators=[DataRequired(), Length(min=5)])
    image = FileField('Upload Recipe Image', validators=[FileRequired()])
    submit = SubmitField('Add Recipe')
