from datetime import datetime as dt

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField(
        "Content",
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired()]
    )
    is_active = BooleanField("Active Post")
    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=dt.now()
    )
    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Tech"),
            ("other", "Other")
        ],
        validators=[DataRequired()]
    )