# PAITAR-Flask
basic website to create flashcards &amp; flashcardssets
Lokales Setup der Anwendung
Um die Anwendung lokal auszuführen, müssen Sie zunächst sicherstellen, dass Ihre Umgebung richtig konfiguriert ist. Hier sind die Schritte, um die Anwendung lokal einzurichten:

1. Datenbankkonfiguration ändern:

Öffnen Sie die config.py-Datei und ändern Sie den Eintrag für SQLALCHEMY_DATABASE_URI entsprechend den Angaben für Ihre lokale Datenbank. Zum Beispiel:

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/databasename'

2. Virtuelle Umgebung erstellen:

Erstellen Sie eine virtuelle Umgebung, um die Abhängigkeiten der Anwendung zu isolieren:

python -m venv myenv

Aktivieren Sie die virtuelle Umgebung:

Unter Windows:
myenv\Scripts\activate

Unter Unix/macOS:
source myenv/bin/activate

3. Abhängigkeiten installieren:

Installieren Sie die erforderlichen Python-Pakete aus der requirements.txt-Datei:
pip install -r requirements.txt

4. Datenbankmigrationen durchführen:

Führen Sie die Datenbankmigrationen durch, um das Schema der Datenbank zu erstellen:
flask db init
flask db upgrade

5. Anwendung starten:

Starten Sie die Anwendung:
flask run

Die Anwendung sollte nun lokal auf Ihrem Rechner laufen. Öffnen Sie Ihren Webbrowser und navigieren Sie zur angezeigten URL, um die Anwendung zu verwenden.

Bitte stellen Sie sicher, dass Ihre lokale Datenbank läuft und die richtigen Zugangsdaten in der Konfigurationsdatei angegeben sind, bevor Sie die Anwendung starten.

