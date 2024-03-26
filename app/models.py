# Grundlegende Importe und Initialisierung
from datetime import datetime
from app import db, login
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask import url_for

# Modelldefinition für einen Benutzer
class User(UserMixin, db.Model):
    # Datenbanksäulendefinitionen
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    sets = db.relationship('FlashcardSet', backref='author', lazy='dynamic')

    # Methoden für Passwortmanagement
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Repräsentation des Benutzerobjekts
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # Erstellen einer URL für das Benutzeravatar
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    # Konvertierung von Benutzerdaten in ein Wörterbuch (für API-Antworten)
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'about_me': self.about_me,
            '_links': {
                'self': url_for('get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data
    
    # Generierung einer Sammlung von Benutzerdaten
    def to_collection():
        users = User.query.all()
        data = {'items': [item.to_dict() for item in users]}
        return data
    
    # Aktualisierung von Benutzerdaten aus einem Wörterbuch
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

# Benutzer-Loader für Flask-Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Modelldefinition für eine Flashcard
class Flashcard(db.Model):
    # Datenbanksäulendefinitionen
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(140), nullable=False)
    answer = db.Column(db.String(140), nullable=False)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_set.id'))

    # Konvertierung von Flashcard-Daten in ein Wörterbuch
    def to_dict(self):
        data = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            '_links': {
                'self': url_for('get_flashcard', id=self.id, _external=True),
            }
        }
        return data

# Modelldefinition für einen Flashcard-Set
class FlashcardSet(db.Model):
    # Datenbanksäulendefinitionen
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flashcards = db.relationship('Flashcard', backref='set', lazy='dynamic')

    # Konvertierung von FlashcardSet-Daten in ein Wörterbuch
    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'public': self.public,
            'user_id': self.user_id,
            '_links': {
                'self': url_for('get_flashcardset', id=self.id, _external=True),
            }
        }
        return data
