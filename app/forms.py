from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.db_models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    user_type = SelectField('User Type', choices=[('', 'Select one...'), ('merchant', 'Merchant'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Register')

    # Flask-WTF automatically calls validate_<field_name> methods during form.validate_on_submit()
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Username is already in use.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email is already in use.')
    
    def validate_confirm(self, confirm):
        equal_validator = EqualTo('password', message='Passwords do not match.')
        equal_validator(self, confirm)