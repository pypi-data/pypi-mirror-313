from typing import Any
from flask_wtf import FlaskForm # type: ignore
from flask_wtf.file import FileRequired, FileAllowed, FileField, FileSize # type: ignore
from wtforms import IntegerRangeField, SelectField, StringField, TimeField, TextAreaField
from wtforms.validators import Length, DataRequired, NumberRange, Regexp
from frolicapp.models import IMAGE_EXTENSIONS, EVT_NAME_LEN, EVT_THUMBNAIL_MAX_SIZE, EVT_DESCRIPTION_LEN, EVT_MAX_TEAMS_CONSTRAIN, EVT_ALLOWED_TEAM_SIZE_CONSTRAIN, MB, EVT_DETAILS_SIZE
from frolicapp.models import Branch
import re
import string

class SearchForm(FlaskForm): # type: ignore
    search = StringField(validators=[Length(min=0, max=20)], default='', filters=[str.strip, str.lower], render_kw=dict(placeholder='Type here...'))


evt_consts = dict(
    IMAGE_EXTENSIONS=IMAGE_EXTENSIONS,
    EVT_NAME_LEN=EVT_NAME_LEN,
    EVT_THUMBNAIL_MAX_SIZE=EVT_THUMBNAIL_MAX_SIZE//MB, EVT_DESCRIPTION_LEN=EVT_DESCRIPTION_LEN, EVT_MAX_TEAMS_CONSTRAIN=EVT_MAX_TEAMS_CONSTRAIN, EVT_ALLOWED_TEAM_SIZE_CONSTRAIN=EVT_ALLOWED_TEAM_SIZE_CONSTRAIN
)


# class RichTextEditorInput(TextInput):
#     def __call__(self, field: Field, **kwargs: Any) -> Markup:
#         return Markup('<div id="editor" style="height: 512px;"></div>')


class EventForm(FlaskForm): # type: ignore
    name = StringField('Title', validators=[DataRequired(), Length(min=EVT_NAME_LEN[0], max=EVT_NAME_LEN[1]), Regexp(f"^[{re.escape(string.ascii_lowercase + ' ')}]+$", message="Event name can only have lowercase English alphabets and spaces.")], default='', filters=[str.strip], render_kw=dict(placeholder='Event Title...'))
    branch = SelectField('Branch', validators=[DataRequired()], choices=[(x.value, x.value.upper()) for x in Branch], default=Branch.CSE.value)
    description = StringField('Brief Description', validators=[DataRequired(), Length(EVT_DESCRIPTION_LEN[0], EVT_DESCRIPTION_LEN[1]), Regexp(f"^[{re.escape(string.ascii_letters + ' ' + string.punctuation)}]+$", message=f"Event description can only have English alphabets, spaces or one of these punctuations: {string.punctuation} .")], default='', filters=[str.strip], render_kw=dict(placeholder='describe the event in brief...'))
    thumbnail = FileField('Thumbnail', validators=[FileRequired(), FileAllowed(IMAGE_EXTENSIONS), FileSize(min_size=1, max_size=EVT_THUMBNAIL_MAX_SIZE)]) 
    start_time = TimeField('Starting at', validators=[DataRequired()])
    max_teams = IntegerRangeField('Maximum number of teams', validators=[DataRequired(), NumberRange(min=EVT_MAX_TEAMS_CONSTRAIN.min, max=EVT_MAX_TEAMS_CONSTRAIN.max)], default=1)
    min_team_size = IntegerRangeField('Minimum team size', validators=[DataRequired(), NumberRange(min=EVT_ALLOWED_TEAM_SIZE_CONSTRAIN.min, max=EVT_ALLOWED_TEAM_SIZE_CONSTRAIN.max)], default=1)
    max_team_size = IntegerRangeField('Maximum team size', validators=[DataRequired(), NumberRange(min=EVT_ALLOWED_TEAM_SIZE_CONSTRAIN.min, max=EVT_ALLOWED_TEAM_SIZE_CONSTRAIN.max)], default=1)
    details = TextAreaField('Details', validators=[Length(min=0, max=EVT_DETAILS_SIZE)], default='', filters=[str.strip])
