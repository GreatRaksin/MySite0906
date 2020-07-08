import os

from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from habrClone import App, db
from habrClone.forms import LoginForm, RegistrationForm, AccountUpdateForm, NewsForm, ZvonokForm
from habrClone.models import User, New, Zvonok


@App.route('/', methods=['GET', 'POST'])
@App.route('/index', methods=['GET', 'POST'])
def index():
    form = ZvonokForm()
    if form.validate_on_submit():
        zvonok = Zvonok(text=form.body.data, phone=form.phone.data, user_username=current_user.username)
        db.session.add(zvonok)
        db.session.commit()

        flash('Обращение отправлено!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


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
            flash('Неправильное имя пользователя и/или пароль!', 'danger')
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

        flash('Вы успешно зарегистрировались!', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = f_name + f_ext
    pic_path = os.path.join(App.root_path, 'static/img/avatars',
                            pic_fn)  # MySite0906/habrClone/, static/img/avatar, avatar.jpg

    resize_image = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(resize_image)

    image.save(pic_path)
    return pic_fn


@App.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Обновлено!', 'info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    avatar = url_for('static', filename='img/avatars/' + current_user.avatar)
    news = New.query.filter_by(user_id=current_user.id)

    zvonki = Zvonok.query.all()
    return render_template('account.html', avatar=avatar, form=form, news=news, zvonki=zvonki)


@App.route('/about')
def about_page():
    return render_template('about.html', title='О нас')


@App.route('/blog', methods=['GET', 'POST'])
def news():
    form = NewsForm()
    if form.validate_on_submit():
        new = New(article=current_user.username, body=form.body.data, user_id=current_user.id)
        db.session.add(new)
        db.session.commit()

        flash('Новость опубликована!', 'success')
        return redirect(url_for('news'))

    news = New.query.all()
    return render_template('blog.html', title='Блог', form=form, news=news)
