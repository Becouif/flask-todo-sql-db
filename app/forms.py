from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    todo = StringField('Todo',validators=[DataRequired()],render_kw={'placeholder' : 'Enter your todo here','autofocus': True,"size": 32, "id": "todo-input"})
    add_todo = SubmitField('Add Todo')