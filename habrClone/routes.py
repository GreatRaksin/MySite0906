from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from habrClone import App, db
from habrClone.forms import LoginForm, RegistrationForm, AccountUpdateForm
from habrClone.models import User


@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html')


@App.route('/sign_in', methods=['GET', 'POST'])
def login():
    '''проверка текущего сеанса пользователя (вошел или нет)'''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    '''когда форма отправляется'''
    if form.validate_on_submit():
        '''находим пользователя в базе'''
        user = User.query.filter_by(username=form.username.data).first()
        '''если мы его там не нашли (None) или пароль невеный'''
        if user is None or not user.check_password(form.password.data):
            '''даем ему сообщение и возвращаем на страницу с логином'''
            flash('Неправильное имя пользователя и/или пароль!')
            return redirect(url_for('login'))

        '''если все ок, выполняем вход (login_user) и перенаправляем на главную'''
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@App.route('/sign_out')
def logout():
    logout_user()
    return redirect(url_for('index'))


@App.route('/sign_up', methods=['GET', 'POST'])
def register():
    '''проверка текущего сеанса пользователя (вошел или нет)'''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Вы успешно зарегистрировались!')

        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


@App.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Обновлено!')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    avatar = url_for('static', filename='img/avatars/' + current_user.avatar)
    return render_template('account.html', avatar=avatar, form=form)
