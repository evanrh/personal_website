from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, FieldList, HiddenField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

# Make sure to include the CSRF Token in any form to validate information correctly
class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    preview = StringField('Preview Text', validators=[DataRequired()], widget=TextArea())
    body = StringField('Body', widget=TextArea())
    categories = FieldList(StringField('Category'))
    submit = SubmitField('Save')

class EditPostForm(NewPostForm):
    id = HiddenField('ID', validators=[DataRequired()])