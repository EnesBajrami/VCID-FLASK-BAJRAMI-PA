from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm #die erstellte forms.py ist noch eine klasse bzw eine function erstllt wordne diese mus snatürlich den routes.py bekannt gemacht werden darum app.form im verzeichnis app befindet sich ein script forms.py dort drin ist eine function eine kalsse LoginForm mnit inhalten
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime, timedelta
from app.models import Flashcard, FlashcardSet
from app.forms import SetForm, FlashcardForm, CsrfForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Route /login wurde mit POST betreten. Prüfung, ob alles o.k. ist:
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Alles o.k., Login kann erfolgen
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # Route /login wurde mit GET betreten
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
        # Route /register wurde mit POST betreten. Prüfung, ob alles o.k. ist:
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    # Route /register wurde mit GET betreten
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)




@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
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



@app.route('/sets')
@login_required
def sets():
    user_sets = FlashcardSet.query.filter_by(user_id=current_user.id).all()
    csrf_form = CsrfForm()  # Verwenden Sie das CSRF-Schutzformular
    return render_template('sets.html', sets=user_sets, form=csrf_form)



@app.route('/set/<int:set_id>')
@login_required
def set_detail(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    if flashcard_set.author != current_user and not flashcard_set.public:
        flash('You do not have permission to view this set.', 'warning')
        return redirect(url_for('sets'))
    form = CsrfForm()  # Erstellen eines Formulars für CSRF-Schutz
    return render_template('set_detail.html', set=flashcard_set, form=form)




# Erstellen eines neuen Sets
@app.route('/set/new', methods=['GET', 'POST'])
@login_required
def new_set():
    form = SetForm()
    if form.validate_on_submit():
        flashcard_set = FlashcardSet(title=form.title.data, public=form.public.data, author=current_user)
        db.session.add(flashcard_set)
        db.session.commit()
        flash('Your flashcard set has been created!', 'success')
        return redirect(url_for('sets'))
    return render_template('create_set.html', form=form)

# Liste aller öffentlichen Sets
@app.route('/public_sets')
@login_required
def public_sets():
    sets = FlashcardSet.query.filter_by(public=True).all()
    return render_template('public_sets.html', sets=sets)

@app.route('/set/delete/<int:set_id>', methods=['POST'])
@login_required
def delete_set(set_id):
    set_to_delete = FlashcardSet.query.get_or_404(set_id)
    if set_to_delete.author != current_user:
        flash('You are not authorized to delete this set.', 'warning')
        return redirect(url_for('sets'))
    db.session.delete(set_to_delete)
    db.session.commit()
    flash('The set has been successfully deleted.', 'success')
    return redirect(url_for('sets'))


@app.route('/set/<int:set_id>/new_flashcard', methods=['GET', 'POST'])
@login_required
def new_flashcard(set_id):
    set = FlashcardSet.query.get_or_404(set_id)
    if set.author != current_user:
        flash('You are not authorized to add flashcards to this set.', 'warning')
        return redirect(url_for('sets'))
    form = FlashcardForm()
    if form.validate_on_submit():
        flashcard = Flashcard(question=form.question.data, answer=form.answer.data, set=set)
        db.session.add(flashcard)
        db.session.commit()
        flash('Your flashcard has been added.', 'success')
        return redirect(url_for('set_detail', set_id=set.id))
    return render_template('create_flashcard.html', form=form, set_id=set_id)



@app.route('/flashcard/delete/<int:card_id>', methods=['POST'])
@login_required
def delete_flashcard(card_id):
    card_to_delete = Flashcard.query.get_or_404(card_id)
    if card_to_delete.set.author != current_user:
        flash('You are not authorized to delete this flashcard.', 'warning')
        return redirect(url_for('flashcards'))
    db.session.delete(card_to_delete)
    db.session.commit()
    flash('The flashcard has been successfully deleted.', 'success')
    return redirect(request.referrer or url_for('sets'))

