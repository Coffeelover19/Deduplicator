# Deduplicator

Kleines Mini-Programm, das im aktuellen Start-Ordner Dateien anhand ihres Inhalts (SHA-256) vergleicht und doppelte Dateien löscht.

## Voraussetzungen

- **Python 3.8 oder neuer** muss installiert sein.
  Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  Beim Installieren den Haken bei **„Add Python to PATH"** setzen.

## Nutzung unter Windows

1. **Ordner öffnen**, in dem Duplikate gesucht werden sollen (z. B. `C:\Bilder`).
2. Die Datei `deduplicate.py` in diesen Ordner **kopieren**.
3. Im Ordner die **Adressleiste** des Explorers anklicken, `cmd` eingeben und **Enter** drücken – damit öffnet sich eine Eingabeaufforderung direkt im richtigen Ordner.
4. Folgenden Befehl eingeben und mit **Enter** bestätigen:

```cmd
python deduplicate.py
```

Das Programm gibt aus, welche Dateien gelöscht wurden, und meldet am Ende die Anzahl der entfernten Duplikate.

### Alternativ: Rechtsklick-Ausführung

- Rechtsklick auf `deduplicate.py` → **„Öffnen mit"** → **Python** auswählen.
- Das Programm läuft dann im aktuellen Ordner der Datei.

## Hinweise

- Es werden nur Dateien im aktuellen Ordner verarbeitet.
- Unterordner werden nicht durchsucht.
- Bei gleichen Inhalten bleibt die zuerst gefundene Datei erhalten, weitere Duplikate werden gelöscht.
