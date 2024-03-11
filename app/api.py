from app import app, db
from app.models import Flashcard, FlashcardSet, User
from flask import jsonify, request, url_for
from app.errors import bad_request
from app.models import User



@app.route('/api/flashcards/<int:id>', methods=['GET'])
def get_flashcard(id):
    flashcard = Flashcard.query.get_or_404(id)
    data = flashcard.to_dict()
    return jsonify(data)



@app.route('/api/flashcardset/<int:id>', methods=['GET'])
def get_flashcardset(id):
    flashcardset = FlashcardSet.query.get_or_404(id)
    data = flashcardset.to_dict()
    return jsonify(data)


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)

@app.route('/api/users', methods=['GET'])
def get_users():
    data = User.to_collection()
    return jsonify(data)


# Endpunkt für User-Registrierung
@app.route('/api/users/create', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_user', id=user.id)
    return response
