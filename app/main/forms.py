from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required(), Length(min=2)])
    submit = SubmitField('Submit')

class EssayForm(Form):
    essay = TextAreaField('Please input your essay', validators=[Required(), Length(min=2)])
    submit = SubmitField('Submit')