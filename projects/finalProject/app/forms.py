from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(max=64)], render_kw={'placeholder': 'name' })
	password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'password' })
	email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'email' })
	submit = SubmitField('Sign up')

class PostForm(FlaskForm):
	total = StringField('Total', validators=[DataRequired(), Length(max=64)])
	content = TextAreaField('Content')
	submit = SubmitField('Send')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': 'email' })
	password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'password'})
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign in')
		
