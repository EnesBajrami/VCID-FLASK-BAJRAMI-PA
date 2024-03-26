from app import app, db
from app.models import Flashcard, FlashcardSet, User
from flask import jsonify, request, url_for
from app.errors import bad_request
from app.models import User
from app import csrf

# Endpunkt zum Abrufen einer einzelnen Flashcard anhand ihrer ID
@app.route('/api/flashcards/<int:id>', methods=['GET'])
def get_flashcard(id):
    # Abrufen der Flashcard anhand ihrer ID oder Rückgabe eines 404-Fehlers, wenn nicht gefunden
    flashcard = Flashcard.query.get_or_404(id)
    # Konvertieren der Flashcard-Daten in ein Wörterbuch und Rückgabe als JSON
    data = flashcard.to_dict()
    return jsonify(data)

# Endpunkt zum Abrufen eines Flashcard-Sets anhand seiner ID
@app.route('/api/flashcardset/<int:id>', methods=['GET'])
def get_flashcardset(id):
    # Abrufen des Flashcard-Sets anhand seiner ID oder Rückgabe eines 404-Fehlers, wenn nicht gefunden
    flashcardset = FlashcardSet.query.get_or_404(id)
    # Konvertieren der Flashcard-Set-Daten in ein Wörterbuch und Rückgabe als JSON
    data = flashcardset.to_dict()
    return jsonify(data)

# Endpunkt zum Abrufen eines Benutzers anhand seiner ID
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    # Abrufen des Benutzers anhand seiner ID oder Rückgabe eines 404-Fehlers, wenn nicht gefunden
    data = User.query.get_or_404(id).to_dict()
    # Rückgabe der Benutzerdaten als JSON
    return jsonify(data)

# Endpunkt zum Abrufen aller Benutzer
@app.route('/api/users', methods=['GET'])
def get_users():
    # Abrufen aller Benutzer und Konvertieren in eine Sammlung von Wörterbüchern
    data = User.to_collection()
    # Rückgabe der Benutzerdaten als JSON
    return jsonify(data)

# Endpunkt für die Benutzerregistrierung
@app.route('/api/users/create', methods=['POST'])
def create_user():
    # Abrufen der JSON-Daten aus der Anfrage oder ein leeres Wörterbuch, wenn keine vorhanden sind
    data = request.get_json() or {}
    # Überprüfen, ob die erforderlichen Felder vorhanden sind
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    # Überprüfen, ob der Benutzername bereits verwendet wird
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    # Überprüfen, ob die E-Mail-Adresse bereits verwendet wird
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    # Erstellen eines neuen Benutzers anhand der bereitgestellten Daten
    user = User()
    user.from_dict(data, new_user=True)
    # Hinzufügen des Benutzers zur Datenbank und Commit der Änderungen
    db.session.add(user)
    db.session.commit()
    # Erstellen einer JSON-Antwort mit den Benutzerdaten und dem Statuscode 201 (Created)
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_user', id=user.id)
    return response

# CSRF-Schutz wird für diesen Endpunkt deaktiviert
csrf.exempt(create_user)
