from app import app, db
from app.models import User, Post, Appointment

# Importieren der erforderlichen Module und Klassen aus der App

@app.shell_context_processor
def make_shell_context():
    # Eine Funktion wird definiert, die den Kontext für die Flask-Shell erstellt
    return {'db': db, 'User': User, 'Post': Post, 'Appointment': Appointment}
    # Die Funktion gibt ein Wörterbuch zurück, das die Datenbankinstanz (db) und die Modelle (User, Post, Appointment) enthält
