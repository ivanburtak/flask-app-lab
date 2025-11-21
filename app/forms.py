from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional


class ContactForm(FlaskForm):
    name = StringField(
        'Ім’я',
        validators=[
            DataRequired(message="Поле не може бути порожнім"),
            Length(min=4, max=10, message="Довжина має бути 4–10 символів")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Поле не може бути порожнім"),
            Email(message="Некоректний email")
        ]
    )

    phone = StringField(
        'Телефон',
        validators=[
            Optional(),
            Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")
        ]
    )

    subject = SelectField(
        'Тема',
        choices=[
            ('support', 'Підтримка'),
            ('question', 'Питання'),
            ('offer', 'Пропозиція'),
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        'Повідомлення',
        validators=[
            DataRequired(),
            Length(max=500, message="Максимум 500 символів")
        ]
    )

    submit = SubmitField("Надіслати")