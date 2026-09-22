# Zeitblick – Landingpage

Marketing-/Verkaufs-Website für [Zeitblick](../zeitblick/), aufgebaut wie eine
klassische SaaS-Landingpage (Hero, Problem/Lösung, Live-Vorschau, Preise, FAQ),
in Design und Farben an die echte App angelehnt.

Vanilla HTML/CSS/JS, keine Abhängigkeiten außer Google Fonts. Noch **keine**
echte Zahlungsanbindung — der "Platz sichern"-Button im Preise-Bereich öffnet
stattdessen eine vorausgefüllte E-Mail (kein Backend vorhanden).

## Status

Vorschau/Preview-Phase: `noindex` gesetzt, Impressum/Datenschutz mit
Platzhaltern (wie bei `smalox-webdesign`), da noch kein Gewerbe für den Verkauf
angemeldet ist.

## Lokal ansehen

```
python -m http.server 8774 --directory web-demos/zeitblick-landing
```

oder `index.html` direkt im Browser öffnen.

## Nächste Schritte (nicht Teil dieser Seite)

- Echte Zahlungsanbindung (z. B. Stripe) für das 5-€/Monat-Abo — dafür wird ein
  Backend nötig, eine reine statische Seite reicht nicht mehr aus.
- Zeitblick als einzelne, sich selbst aktualisierende Installer-Datei bündeln
  (z. B. PyInstaller + Auto-Update-Mechanismus), statt der aktuellen
  `.cmd`-Skripte.
- Fokus-Timer (Pomodoro: 25 Min. Fokus / 5 Min. Pause) mit automatischer
  Ablenkungssperre während des Fokus-Blocks — als neues Feature der App selbst,
  auf dieser Seite bereits im Roadmap-Abschnitt angeteasert.
- Werbung/Marketing, sobald ein echter Verkaufsstart ansteht.
