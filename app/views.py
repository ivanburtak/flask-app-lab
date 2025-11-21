from flask import render_template, redirect, flash, url_for
from . import app
from .forms import ContactForm
import logging

contact_logger = logging.getLogger('contact')
contact_logger.setLevel(logging.INFO)
contact_logger.propagate = False

file_handler = logging.FileHandler('contact.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
contact_logger.addHandler(file_handler)

@app.route('/')
def resume():
    return render_template('resume.html', title='Моє Резюме')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact_logger.info(
                f"Message from {form.name.data} ({form.email.data}, {form.phone.data}) | "
                f"subject={form.subject.data} | msg={form.message.data}"
            )

            flash(
                f"Дякую, {form.name.data}! Ваше повідомлення успішно надіслано.",
                category='success'
            )
            return redirect(url_for('contact'))  # PRG

        except Exception as e:
            flash("Сталася помилка при записі. Спробуйте ще раз.", category='danger')
            return redirect(url_for('contact'))

    return render_template('contact.html', form=form)