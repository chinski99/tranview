from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class TextInputForm(Form):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[Length(min=0, max=1400)])
