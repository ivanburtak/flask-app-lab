from flask import request, render_template, url_for, redirect, session, flash, make_response

from . import users_bp
from .forms import LoginForm

USER_DATA = {
    "user": "admin",
    "password": "1234"
}

@users_bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("hi.html",
                           name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)


@users_bp.route("/profile")
def profile():
    if "user" not in session:
        flash("Будь ласка, увійдіть, щоб переглянути профіль.", "warning")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "light")

    return render_template(
        "profile.html",
        title="Профіль",
        user=session["user"],
        cookies=request.cookies,
        theme=theme
    )

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == USER_DATA["user"] and password == USER_DATA["password"]:
            session["user"] = username
            flash(f"Ви успішно ввійшли! Запам'ятати: {"так" if remember else "ні"}", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірне ім'я користувача або пароль.", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html", form=form)

@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))

@users_bp.route('/add_cookie', methods=["POST"])
def add_cookie():
    if "user" not in session:
        flash("Ви повинні бути авторизовані.", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    value = request.form.get("value")
    duration = request.form.get("duration", type=int)

    resp = make_response(redirect(url_for("users.profile")))

    if key and value and duration:
        resp.set_cookie(key, value, max_age=duration)
        flash(f'Cookie "{key}" успішно додано на {duration} сек.', "success")
    else:
        flash("Будь ласка, заповніть усі поля для додавання cookie.", "danger")

    return resp

@users_bp.route('/delete_cookie/<key>')
def delete_cookie(key):
    if "user" not in session:
        flash("Ви повинні бути авторизовані.", "danger")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    if key in request.cookies:
        resp.delete_cookie(key)
        flash(f'Cookie "{key}" успішно видалено.', "info")
    else:
        flash(f'Cookie з ключем "{key}" не знайдено.', "warning")

    return resp

@users_bp.route("/delete_all_cookies")
def delete_all_cookies():
    if "user" not in session:
        flash("Ви повинні бути авторизовані.", "danger")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    for k in request.cookies.keys():
        resp.delete_cookie(k)
    flash("Усі cookie успішно видалено.", "info")
    return resp

@users_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if "user" not in session:
        flash("Будь ласка, увійдіть, щоб змінювати тему.", "warning")
        return redirect(url_for("users.login"))

    if theme not in ["light", "dark"]:
        flash("Невідома тема.", "danger")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("theme", theme, max_age=30*24*60*60)
    flash(f"Тема '{theme}' активована.", "info")
    return resp
