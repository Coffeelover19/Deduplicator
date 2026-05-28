# Deduplicator

Kleines Mini-Programm, das im aktuellen Start-Ordner Dateien anhand ihres Inhalts (SHA-256) vergleicht und doppelte Dateien löscht.

## Nutzung

```bash
python deduplicate.py
```

- Es werden nur Dateien im aktuellen Ordner verarbeitet.
- Unterordner werden nicht durchsucht.
- Bei gleichen Inhalten bleibt die zuerst gefundene Datei erhalten, weitere Duplikate werden gelöscht.
