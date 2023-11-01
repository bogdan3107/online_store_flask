from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField(('Username'), validators=[DataRequired()])
    delivery_address = TextAreaField(('Your delivery address'),
                             validators=[Length(min=1, max=128)])
    phone_number = StringField(('Your phone number'), validators=[
    validators.Regexp(r'^\d{10}$', message='Invalid phone number format')
    ])
    submit = SubmitField(('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(('Please use a different username.'))
            