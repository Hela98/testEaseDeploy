from flask_wtf import FlaskForm

from wtforms import StringField

class MyForm(FlaskForm):
    gitRepo= StringField(label="URL of your git repository")
    path= StringField(label="where you would like to clone your repository")