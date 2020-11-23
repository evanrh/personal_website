from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post = FileField('Post', validators=[FileRequired()])
    submit = SubmitField('Upload')