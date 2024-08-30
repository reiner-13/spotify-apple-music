from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class CreateAccountForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password1")])
    platform = RadioField("Platform", choices=[("spotify", "Spotify"), ("apple", "Apple Music")], render_kw={"class": "no-bullets"})
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data
        ))
        if user is not None:
            raise ValidationError("Please use a different username.")

class AddPlaylistForm(FlaskForm):
    pass