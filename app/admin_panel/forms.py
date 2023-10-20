from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, \
    FileField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app.models import Category


class AddCategory(FlaskForm):
    name = StringField(('Category name'), validators=[Length(min=1)])


class AddProductForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)

        with current_app.app_context():
            categories = Category.query.all()
            self.category.choices = [(category.id, category.name) for category in categories]

    name = StringField(('Product name'), validators=[DataRequired()])
    description = TextAreaField(('Description'), validators=[Length(min=0, max=140), Optional() ])
    image = FileField(('Upload a picture'), 
                      validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!'), 
                                  FileSize(max_size=5 * 1024 * 1024, 
                                           message='File size must be <= 5MB')])
    price = FloatField(('Enter the price'), validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField(('Enter the stock'), validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField(('Choose category'), coerce=int, validators=[DataRequired()])
    submit = SubmitField(('Add Product'))