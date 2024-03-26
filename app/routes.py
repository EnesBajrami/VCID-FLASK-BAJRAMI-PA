# Import-Statements und Initialisierung
from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SetForm, FlashcardForm, CsrfForm
from app.models import User, Flashcard, FlashcardSet
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

# Startseite der Anwendung
@app.route('/')
@app.route('/index')
@login_required
def index():
    # Zeigt die Startseite an, auf der der Benutzer nach dem Einloggen landet.
    return render_template('index.html', title='Home')

# Login-Seite der Anwendung
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Weiterleitung, wenn der Benutzer bereits eingeloggt ist.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Überprüfung des Benutzernamens und Passworts nach Formularabsendung.
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Benutzer einloggen und zur 'next' Seite weiterleiten, falls vorhanden.
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # Anzeige der Login-Seite.
    return render_template('login.html', title='Sign In', form=form)

# Logout-Funktionalität
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Registrierungsseite
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Weiterleitung, wenn der Benutzer bereits eingeloggt ist.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Benutzerkonto erstellen, wenn das Formular gültig ist.
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    # Anzeige der Registrierungsseite.
    return render_template('register.html', title='Register', form=form)

# Benutzerprofilseite
@app.route('/user/<username>')
@login_required
def user(username):
    # Abrufen des Benutzerobjekts, das zum Benutzernamen gehört.
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

# Profilbearbeitungsseite
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # Aktualisieren der Benutzerdaten mit den Formulardaten.
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        # Vorbelegung der Formularfelder mit den aktuellen Benutzerdaten.
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# Seite für die Anzeige und Verwaltung von Flashcard-Sets
@app.route('/sets')
@login_required
def sets():
    # Abrufen aller Sets des aktuellen Benutzers.
    user_sets = FlashcardSet.query.filter_by(user_id=current_user.id).all()
    csrf_form = CsrfForm()  # CSRF-Schutz für Formulare.
    return render_template('sets.html', sets=user_sets, form=csrf_form)




# Detailansicht eines Flashcard-Sets anzeigen
@app.route('/set/<int:set_id>')
@login_required
def set_detail(set_id):
    # Abrufen des Sets oder Anzeige einer Fehlermeldung, wenn es nicht existiert
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    # Zugriffsbeschränkung: Prüfen, ob der aktuelle Benutzer der Autor ist oder ob das Set öffentlich ist
    if flashcard_set.author != current_user and not flashcard_set.public:
        flash('You do not have permission to view this set.', 'warning')
        return redirect(url_for('sets'))
    form = CsrfForm()  # CSRF-Schutz für Formulare
    return render_template('set_detail.html', set=flashcard_set, form=form)

# Route zum Erstellen eines neuen Flashcard-Sets
@app.route('/set/new', methods=['GET', 'POST'])
@login_required
def new_set():
    form = SetForm()
    if form.validate_on_submit():
        # Erstellen eines neuen Flashcard-Sets und Speichern in der Datenbank
        flashcard_set = FlashcardSet(title=form.title.data, public=form.public.data, author=current_user)
        db.session.add(flashcard_set)
        db.session.commit()
        flash('Your flashcard set has been created!', 'success')
        return redirect(url_for('sets'))
    return render_template('create_set.html', form=form)

# Anzeigen aller öffentlichen Flashcard-Sets
@app.route('/public_sets')
@login_required
def public_sets():
    # Abrufen aller öffentlichen Sets
    sets = FlashcardSet.query.filter_by(public=True).all()
    return render_template('public_sets.html', sets=sets)

# Löschen eines Flashcard-Sets
@app.route('/set/delete/<int:set_id>', methods=['POST'])
@login_required
def delete_set(set_id):
    # Abrufen des zu löschenden Sets oder Anzeige einer Fehlermeldung, wenn es nicht existiert
    set_to_delete = FlashcardSet.query.get_or_404(set_id)
    # Überprüfen, ob der aktuelle Benutzer der Autor des Sets ist
    if set_to_delete.author != current_user:
        flash('You are not authorized to delete this set.', 'warning')
        return redirect(url_for('sets'))
    # Löschen des Sets und Aktualisieren der Datenbank
    db.session.delete(set_to_delete)
    db.session.commit()
    flash('The set has been successfully deleted.', 'success')
    return redirect(url_for('sets'))

# Hinzufügen einer neuen Flashcard zu einem Set
@app.route('/set/<int:set_id>/new_flashcard', methods=['GET', 'POST'])
@login_required
def new_flashcard(set_id):
    # Abrufen des Sets oder Anzeige einer Fehlermeldung, wenn es nicht existiert
    set = FlashcardSet.query.get_or_404(set_id)
    # Überprüfen, ob der aktuelle Benutzer der Autor des Sets ist
    if set.author != current_user:
        flash('You are not authorized to add flashcards to this set.', 'warning')
        return redirect(url_for('sets'))
    form = FlashcardForm()
    if form.validate_on_submit():
        # Erstellen einer neuen Flashcard und Speichern in der Datenbank
        flashcard = Flashcard(question=form.question.data, answer=form.answer.data, set=set)
        db.session.add(flashcard)
        db.session.commit()
        flash('Your flashcard has been added.', 'success')
        return redirect(url_for('set_detail', set_id=set.id))
    return render_template('create_flashcard.html', form=form, set_id=set_id)

# Löschen einer Flashcard
@app.route('/flashcard/delete/<int:card_id>', methods=['POST'])
@login_required
def delete_flashcard(card_id):
    # Abrufen der zu löschenden Flashcard oder Anzeige einer Fehlermeldung, wenn sie nicht existiert
    card_to_delete = Flashcard.query.get_or_404(card_id)
    # Überprüfen, ob der aktuelle Benutzer der Autor des übergeordneten Sets ist
    if card_to_delete.set.author != current_user:
        flash('You are not authorized to delete this flashcard.', 'warning')
        return redirect(url_for('flashcards'))
    # Löschen der Flashcard und Aktualisieren der Datenbank
    db.session.delete(card_to_delete)
    db.session.commit()
    flash('The flashcard has been successfully deleted.', 'success')
    return redirect(request.referrer or url_for('sets'))


