from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CoupleForm, EditProfileForm
from app.models import Authuser

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Jeff'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Authuser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Authuser(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#Create route for Couples Form
@app.route('/registercouple', methods=['GET', 'POST'])
def registercouple():
    if current_user.is_authenticated:
        form = CoupleForm()
        if form.validate_on_submit():
            couple = Couple(
                p1_first_name=form.p1_first_name.data,
                p1_surname=form.p1_surname.data,
                p2_first_name=form.p2_surname.data,
                p2_surname=form.p2_surname.data,
                mail_street_address_1=form.mail_street_address_1.data,
                mail_street_address_2=form.mail_street_address_2.data,
                mail_city=form.mail_city.data,
                mail_state_province=form.mail_state_province.data,
                mail_country=form.mail_country.data,
                telephone_number=form.telephone_number.data,
                note=form.note.data,
                email=form.email.data
                )
            db.session.add(couple)
            db.session.commit()
            flash('Congratulations, you have now registered the couple!')
            return redirect(url_for('login'))
        return render_template('register_couple.html', title='Couple Registration!', form=form)

#Create support for profile page
@app.route('/user/<username>')
@login_required
def user(username):
    user = Authuser.query.filter_by(username=username).first_or_404()
    couples = [
        {'author': user, 'body': 'Wedding #1'},
        {'author': user, 'body': 'Wedding #2'}
    ]
    return render_template('user.html', user=user, couples=couples)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
