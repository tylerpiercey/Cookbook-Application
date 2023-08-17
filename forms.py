from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import FileField
from flask_wtf.file import FileRequired, FileAllowed


class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired(), Length(min=3, max=100)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired(), Length(min=10)])
    preparation_instructions = TextAreaField('Preparation Instructions', validators=[DataRequired(), Length(min=10)])
    serving_instructions = TextAreaField('Serving Instructions', validators=[DataRequired(), Length(min=5)])
    image = FileField('Upload Recipe Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images '
                                                                                                             'only!')])
    submit = SubmitField('Add Recipe')
