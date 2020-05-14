from app import app,db
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Активный Гомез'}
    posts = [
        {
            'author': { 'username': 'John'},
            'body': 'Хороший денек в Иж-Бобье!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Решила посмотреть классическую трилогию "Школьница"'
        },
        {
            'author':{'username': 'kk'},
            'body': 'Миу миу?'
        }
    ]

    return render_template('index.html', title='Active Gomez', posts=posts)


"""АУТЕНТИФИКАЦИЯ"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    #Аутентифицирован ли уже юзер?

    form = LoginForm() #Создание формы аутентификации

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Проверьте правильность логина или пароля')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


"""ВЫХОД"""
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



