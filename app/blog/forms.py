from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    preview = StringField('Preview Text', widget=TextArea(), validators=[DataRequired()])
    categories = StringField('Categories')
    post = FileField('Post', validators=[FileRequired()])
    submit = SubmitField('Upload')