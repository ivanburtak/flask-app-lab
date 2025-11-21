from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        # Якщо буде знайдено @, то тоді це поле стає поштою і
        # вона має проходити через окрему валідацію,
        # але тоді прийдеться уникнути цієї форми і розробляти це окремо
        "Ім'я користувача / Email",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=4, max=10)]
    )
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")