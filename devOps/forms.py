from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,Form
from wtforms.validators import Length, EqualTo, Email, DataRequired , ValidationError, InputRequired
from devOps.models import User



class AddNewProject(FlaskForm):
    nameOfProject= StringField(label="Name of your project")
    gitRepo= StringField(label="URL of your git repository")
    entry_file=StringField(label="Entry file of the application")
    path= StringField(label="where you would like to clone your repository")
    submit = SubmitField('Start analysing app')

class RequestResetForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must register first.')

# Corey
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')


    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField(label='Sign in')


class EmailForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])

class PasswordForm(FlaskForm):
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])



class CreateUser(Form):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    admin= BooleanField('admin?',default=False)
    submit = SubmitField(label='Create new user')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(CreateUser, self).__init__(*args, **kwargs)
     
    

class UpdateUser(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    admin= BooleanField('admin?',default=False)
    submit = SubmitField(label='Update user')

class DeleteUser(FlaskForm):
    
    submit = SubmitField(label='YES')


class DeleteProject(FlaskForm):
    
    submit = SubmitField(label='YES')

class UpdateProject(FlaskForm):

    nameOfProject= StringField(label="Name project")
    gitRepo= StringField(label="URL git repository")
    entry_file=StringField(label="Entry file of the application")
    path= StringField(label="where you would like to clone your repository")
    submit = SubmitField('Update the project')