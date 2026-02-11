# Fitness App Backend

Dies ist das Backend für die FitnessApp, entwickelt mit **Django** und **Django REST Framework**. Es stellt die API-Endpunkte für Benutzerverwaltung, Übungen, Trainingspläne und Scoring bereit.

## Voraussetzungen

Bevor du startest, stelle sicher, dass du folgende Software installiert hast:

- **Python 3.9** oder höher: [Python herunterladen](https://www.python.org/downloads/)
- **pip** (wird normalerweise mit Python installiert)
- **Git** (zum Klonen des Repositories)

## Installation

Folge diesen Schritten, um das Backend auf deinem lokalen Rechner einzurichten.

### 1. Repository klonen und in das Verzeichnis wechseln

Öffne dein Terminal (Mac/Linux) oder die Eingabeaufforderung/PowerShell (Windows) und führe aus:

```bash
git clone <DEIN_REPO_URL>
cd fitnessapp/fitnessapp-backend
```

### 2. Virtuelle Umgebung erstellen

Es wird empfohlen, eine virtuelle Umgebung zu nutzen, um die Abhängigkeiten isoliert zu halten.

**Mac / Linux:**
```bash
python3 -m venv venv
```

**Windows:**
```powershell
python -m venv venv
```

### 3. Virtuelle Umgebung aktivieren

Je nach Betriebssystem ist der Befehl unterschiedlich:

**Mac / Linux:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

*Wenn die Umgebung aktiv ist, solltest du `(venv)` am Anfang deiner Befehlszeile sehen.*

### 4. Abhängigkeiten installieren

Installiere alle notwendigen Pakete aus der `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Datenbank einrichten

Erstelle die SQLite-Datenbank und die notwendigen Tabellen:

```bash
python manage.py migrate
```

### 6. Admin-Benutzer erstellen (Optional)

Um Zugriff auf das Django-Admin-Panel zu erhalten, erstelle einen Superuser:

```bash
python manage.py createsuperuser
```
Folge den Anweisungen (Benutzername, E-Mail, Passwort).

## Server starten

Starte den Entwicklungsserver:

```bash
python manage.py runserver
```

Der Server läuft nun unter: **http://127.0.0.1:8000/**

### Wichtige URLs

- **API Root**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/` (Login mit deinem erstellten Superuser)

## Projektstruktur

Das Backend ist in verschiedene "Apps" unterteilt, die jeweils spezifische Funktionen übernehmen:

- **`users/`**: Benutzerregistrierung und Authentifizierung (JWT).
- **`exercises/`**: Verwaltung von Übungskategorien und Übungen.
- **`trainings/`**: Erstellung und Verwaltung von Trainingsplänen.
- **`scorings/`**: Logik für das Punktesystem und Leaderboards.
- **`fitness_backend/`**: Hauptkonfiguration des Django-Projekts (`settings.py`, `urls.py`).

## Troubleshooting

- **Fehler: "Pillow is not installed"**: Stelle sicher, dass du `pip install -r requirements.txt` ausgeführt hast. Pillow wird für das Hochladen von Bildern benötigt.
- **Datenbankfehler ("no such table")**: Führe `python manage.py migrate` aus.
- **Zugriffsfehler (401 Unauthorized)**: Die meisten Endpunkte benötigen einen gültigen JWT-Token. Das Frontend kümmert sich normalerweise darum nach dem Login.
