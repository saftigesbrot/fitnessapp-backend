# Admin Panel - XP und Score Management

## Übersicht

Das Django Admin Panel wurde erweitert, um XP und Score für Benutzer zu verwalten.

## Features

### 📊 Scoring Admin

**Anzeige:**
- User
- Aktueller Score
- Erstellungsdatum

**Funktionen:**
- ✅ **Score zu ausgewählten Users hinzufügen**
  - Wähle einen oder mehrere Score-Einträge aus
  - Klicke auf "Score zu ausgewählten Users hinzufügen" in der Action-Dropdown
  - Gib die Anzahl der Punkte ein, die hinzugefügt werden sollen
  - Der neue Score wird automatisch als neuer Eintrag gespeichert

### ⭐ Level Current Admin

**Anzeige:**
- User
- Level
- Gesamt-XP
- **Level-Fortschrittsbalken** (farbcodiert)
- XP zum nächsten Level

**Fortschrittsbalken-Farben:**
- 🔴 **Rot** (0-24%): Wenig Fortschritt
- 🟠 **Orange** (25-49%): Mäßiger Fortschritt
- 🟡 **Gelb** (50-74%): Guter Fortschritt
- 🟢 **Grün** (75-100%): Fast am Ziel

**Funktionen:**
- ✅ **XP zu ausgewählten Users hinzufügen**
  - Wähle einen oder mehrere User aus
  - Klicke auf "XP zu ausgewählten Users hinzufügen" in der Action-Dropdown
  - Gib die Anzahl der XP ein
  - **Automatisches Level-Up:** Wenn ein User genug XP für das nächste Level erreicht, wird er automatisch hochgestuft

**Detail-Ansicht:**
- Detaillierter Fortschrittsbalken
- Gesamt-XP Übersicht
- XP-Anforderungen für die nächsten 2-3 Level
- Visueller Fortschrittsbalken

## Verwendung

### Score hinzufügen

1. Gehe zu **Scorings > Scorings** im Admin Panel
2. Wähle die User aus (über Checkboxen)
3. Wähle **"Score zu ausgewählten Users hinzufügen"** aus dem Action-Dropdown
4. Klicke auf **"Los"**
5. Gib die Punktzahl ein (z.B. 100)
6. Klicke auf **"Score hinzufügen"**

### XP hinzufügen

1. Gehe zu **Scorings > Level currents** im Admin Panel
2. Wähle die User aus (über Checkboxen)
3. Wähle **"XP zu ausgewählten Users hinzufügen"** aus dem Action-Dropdown
4. Klicke auf **"Los"**
5. Gib die XP-Anzahl ein (z.B. 250)
6. Klicke auf **"XP hinzufügen"**
7. Level-Ups werden automatisch durchgeführt

### Level-Fortschritt anzeigen

In der **Listen-Ansicht** von Level currents:
- Siehst du den farbcodierten Fortschrittsbalken
- Die genaue XP-Anzeige zum nächsten Level

In der **Detail-Ansicht** eines Users:
- Klappe den Abschnitt **"Fortschritt"** auf
- Siehst du:
  - Detaillierten Fortschritt mit Prozentangabe
  - XP-Übersichtstabelle für mehrere Level
  - Großen visuellen Fortschrittsbalken

## Level-System

Das Level-System verwendet logarithmisches Wachstum:

```python
XP_benötigt = 100 * (Level ^ 1.5)
```

**Beispiele:**
- Level 1 → 2: ~141 XP
- Level 2 → 3: ~119 XP (260 gesamt)
- Level 3 → 4: ~140 XP (400 gesamt)
- Level 5 → 6: ~171 XP (730 gesamt)
- Level 10 → 11: ~268 XP (3162 gesamt)

## Technische Details

### Admin-Klassen

**ScoringAdmin:**
- Custom Action: `add_score_to_users`
- Template: `scorings/templates/admin/add_score_form.html`

**LevelCurrentAdmin:**
- Custom Action: `add_xp_to_users`
- Template: `scorings/templates/admin/add_xp_form.html`
- Custom Display Methods:
  - `level_progress_bar()` - Farbcodierter Balken
  - `xp_to_next_level()` - XP-Fortschritt
  - `level_progress_display()` - Detaillierte Ansicht
  - `xp_info_display()` - XP-Übersichtstabelle

### Automatische Level-Ups

Die `check_and_level_up()` Methode des `LevelCurrent` Models:
- Wird automatisch aufgerufen beim XP-Hinzufügen
- Prüft, ob genug XP für Level-Up vorhanden ist
- Führt mehrere Level-Ups durch, falls nötig
- Speichert die Änderungen automatisch

## Zugriff

**Admin Panel:** http://localhost:8000/admin

**Login:**
- Username: `admin`
- Password: `admin123`

(oder dein eigener Superuser)
