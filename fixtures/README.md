# Test-Daten für FitnessApp

Diese Fixtures enthalten vorgefertigte Test-Daten, damit du direkt mit der App starten kannst, ohne erst alles im Admin-Panel einrichten zu müssen.

## 📦 Was ist enthalten?

### 👥 Test-User (6 User)
Alle User haben das Passwort: **test123** (außer Admin)

- **admin** / admin123 (Superuser für Admin-Panel)
- **max_mustermann** / test123
- **sarah_schmidt** / test123
- **tom_mueller** / test123
- **lisa_wagner** / test123
- **jan_fischer** / test123

### 💪 Übungen (17 Stück)

**7 Kategorien:**
- Brust (Bankdrücken, Liegestütze, Butterfly)
- Rücken (Kreuzheben, Klimmzüge, Rudern)
- Beine (Kniebeugen, Ausfallschritte, Beinpresse)
- Schultern (Schulterdrücken, Seitheben)
- Arme (Bizeps Curls, Trizeps Dips)
- Bauch (Plank, Crunches)
- Cardio (Laufen, Burpees)

Alle Übungen sind **öffentlich** verfügbar.

### 📋 Trainingspläne (3 Stück)

1. **Einsteiger Ganzkörper** (Anfänger, 90 Sek. Pause)
2. **Brust & Trizeps** (Fortgeschritten, 60 Sek. Pause)
3. **Rücken & Bizeps** (Fortgeschritten, 60 Sek. Pause)

### 🏆 Rangliste

Alle Test-User haben bereits Scores und Level für die Rangliste:
- sarah_schmidt: 3200 Punkte, Level 10
- max_mustermann: 2850 Punkte, Level 8
- lisa_wagner: 2650 Punkte, Level 7
- tom_mueller: 1950 Punkte, Level 6
- jan_fischer: 1750 Punkte, Level 5

## 🚀 Test-Daten laden

### Voraussetzungen
Stelle sicher, dass die Datenbank-Migrationen durchgeführt wurden:
```bash
python manage.py migrate
```

### Test-Daten laden
```bash
python manage.py load_testdata
```

### Oder: Alte Daten löschen und neu laden
```bash
python manage.py load_testdata --clear
```

⚠️ **Achtung:** `--clear` löscht **alle** bestehenden User (außer Superuser), Übungen, Trainingspläne und Scores!

## 📝 Login

Nach dem Laden der Test-Daten kannst du dich einloggen mit:

**Admin-Panel:** http://localhost:8000/admin
- Username: `admin`
- Password: `admin123`

**App (beliebiger Test-User):**
- Username: `max_mustermann` (oder einer der anderen)
- Password: `test123`

## 🔄 Bei jedem App-Start automatisch laden

Falls du möchtest, dass die Daten bei jedem Start automatisch vorhanden sind, kannst du in deiner `settings.py` oder beim Start-Script folgendes hinzufügen:

```python
# In settings.py (am Ende)
if DEBUG:
    # Check ob Datenbank leer ist
    from django.contrib.auth.models import User
    if User.objects.count() == 0:
        from django.core.management import call_command
        call_command('load_testdata')
```

Oder beim Start:
```bash
python manage.py migrate && python manage.py load_testdata && python manage.py runserver
```

## 🔧 Fixtures manuell anpassen

Die Fixture-Datei liegt in: `fixtures/initial_data.json`

Du kannst sie nach Belieben anpassen. Nach Änderungen einfach neu laden:
```bash
python manage.py load_testdata --clear
```
