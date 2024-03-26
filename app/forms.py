# Import der erforderlichen Module
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

# Formular für die Anmeldung
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

# Formular für die Registrierung
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Validierung des Benutzernamens: Stellt sicher, dass der Benutzername eindeutig ist
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Validierung der E-Mail-Adresse: Stellt sicher, dass die E-Mail-Adresse eindeutig ist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Formular zum Bearbeiten des Benutzerprofils
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

# Formular zum Erstellen eines neuen Sets von Flashcards
class SetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    public = BooleanField('Make this set public')
    submit = SubmitField('Submit')

# Formular zum Hinzufügen einer neuen Flashcard zu einem Set
class FlashcardForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Formular für CSRF-Schutz (Cross-Site Request Forgery)
class CsrfForm(FlaskForm):
    pass  # Keine zusätzlichen Felder benötigt
