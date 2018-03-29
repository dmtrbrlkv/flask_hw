from flask import Flask, request
from flask.json import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators, ValidationError
from datetime import datetime, date
import json
import os.path


class ContactForm(FlaskForm):
    name = StringField(validators=[
        validators.length(min=4, max=25)
    ])
    email = StringField(validators=[
        validators.Length(min=6, max=35),
        validators.Email()
    ])

    job = StringField(validators=[
        validators.AnyOf(["IT", "HR", "Bank"]),
        validators.DataRequired()
    ])

    birthday = StringField(validators=[
        validators.DataRequired()
    ])

    def validate_birthday(form, field):
        data = field.data
        try:
            date = datetime.strptime(data, "%d.%m.%Y")
        except ValueError as e:
            raise ValidationError("Не удалось перевести {} в дату".format(data))

        today = datetime.today()
        if today.month != date.month:
            raise ValidationError("Сегодня не {} месяц".format(date.month))

class UserForm(FlaskForm):
    email = StringField(validators=[
        validators.DataRequired(),
        validators.Email()
    ])

    password = StringField(validators=[
        validators.Length(min=6)
    ])

    confirm_password = StringField()
    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError("Passwords must match")


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    print(request.method)
    if request.method == "GET":
        return "get", 200
    elif request.method == "POST":
        print(request.form)
        form = ContactForm(request.form)
        if form.validate():
            return "post valid", 200
        else:
            return "post invalid", 200
    else:
        return "WTF", 404


@app.route("/numbers/<int:n1>/<int:n2>")
def numbers(n1, n2):
    return "{} + {} = {}".format(n1, n2, n1 + n2)


@app.route("/strings/<s1>/<s2>/<s3>")
def strings(s1, s2, s3):
    return "наибольшая строка = '{}'".format(
        s1 if len(s1) >= len(s2) and len(s1) >= len(s3) else s2 if len(s2) >= len(s3) else s3)


@app.route("/file_exist/<path:filepath>")
def file_exist(filepath):
    print(filepath)
    try:
        with open(filepath) as f:
            return "файл {} существует".format(filepath)
    except:
        return "файл {} не существует".format(filepath)


@app.route("/serve/<path:filename>")
def file_content(filename):
    try:
        with open(os.path.join("files", filename)) as f:
            return f.read()
    except:
        return "файл {} не существует".format(filename), 404


@app.route("/locales")
def locales():
    locales =  ['ru', 'en', 'it']
    # return json.dumps(locales, indent=4)
    return jsonify(locales)


@app.route("/greet/<username>")
def greet(username):
    return "Hello, {}".format(username.capitalize())


@app.route("/form/user", methods = ["POST"])
def user():
    form = UserForm(request.form)
    if form.validate():
        status = 0
        errors = []
    else:
        status = 1
        errors = form.errors
    return jsonify({"status": status, "errors": errors})


if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY='secret key',
        WTF_CSRF_ENABLED=False
    )
    app.run()
