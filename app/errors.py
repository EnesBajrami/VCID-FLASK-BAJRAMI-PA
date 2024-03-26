from flask import render_template, request, jsonify
from app import app, db
from werkzeug.http import HTTP_STATUS_CODES

# Fehlerbehandlung für den HTTP-Statuscode 404 (Seite nicht gefunden)
@app.errorhandler(404)
def not_found_error(error):
    # Überprüfen, ob die Anfrage JSON akzeptiert, und eine entsprechende Antwort senden
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Not Found'})
        response.status_code = 404
        return response
    # Andernfalls eine HTML-Seite mit dem Fehlercode 404 anzeigen
    else:
        return render_template('404.html'), 404

# Fehlerbehandlung für den HTTP-Statuscode 500 (Interner Serverfehler)
@app.errorhandler(500)
def internal_error(error):
    # Rollback der Datenbanktransaktion, falls vorhanden
    db.session.rollback()
    # Überprüfen, ob die Anfrage JSON akzeptiert, und eine entsprechende Antwort senden
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Internal Server Error'})
        response.status_code = 500
        return response
    # Andernfalls eine HTML-Seite mit dem Fehlercode 500 anzeigen
    else:
        return render_template('500.html'), 500

# Generierung einer JSON-Antwort für Fehlermeldungen
def error_response(status_code, message=None):
    # Erstellen einer Payload für die JSON-Antwort
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    # Hinzufügen einer benutzerdefinierten Nachricht, falls vorhanden
    if message:
        payload['message'] = message
    # Erstellen und Rückgabe der JSON-Antwort mit dem angegebenen Statuscode
    response = jsonify(payload)
    response.status_code = status_code
    return response

# Funktion für eine "Bad Request" Fehlerantwort
def bad_request(message):
    # Verwendung der error_response-Funktion mit dem Statuscode 400 (Bad Request)
    return error_response(400, message)
