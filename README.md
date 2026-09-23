# Zeitblick – Landingpage

Marketing-/Verkaufs-Website für [Zeitblick](../zeitblick/), aufgebaut wie eine
klassische SaaS-Landingpage (Hero, Problem/Lösung, Live-Vorschau, Preise, FAQ),
in Design und Farben an die echte App angelehnt.

Vanilla HTML/CSS/JS, keine Abhängigkeiten außer Google Fonts. Live unter
https://smaloxzs.github.io/zeitblick-landing/ (GitHub Pages, eigenes Repo).

## Preismodell

**10 € pro Jahr** mit 7 Tagen kostenloser Testphase. Bezahlt wird über einen
Stripe-Zahlungslink mit **Managed Payments**: Stripe (über seinen Dienst Link)
ist gegenüber dem Kunden der Verkäufer und übernimmt Umsatzsteuer, Rechnungen
und die Abo-Kündigung (app.link.com). Kein eigenes Backend nötig. Nach dem
Kauf leitet Stripe auf `danke.html` weiter, dort gibt es den Download.
`kuendigen.html` erklärt Schritt für Schritt das Kündigen über app.link.com und
ist im Footer jeder Seite sowie in der FAQ verlinkt.

## Status

Vorschau-Phase: `noindex` gesetzt, Impressum mit Platzhalter-Adresse, da noch
kein Gewerbe angemeldet ist. Alle "Testen"-Buttons führen auf den Live-
Zahlungslink `https://buy.stripe.com/7sY9AU1iofcfcSf1mA2oE00` (7 Tage 0 €,
danach 10 €/Jahr). Die `.exe` ist nur noch auf `danke.html` verlinkt.

## CSS-Änderungen

Alle Seiten laden `style.css?v=N`. GitHub Pages lässt Browser CSS etwa 10
Minuten zwischenspeichern, deshalb nach jeder CSS-Änderung die Zahl `N` in
allen HTML-Dateien hochzählen, sonst sehen Besucher neue HTML-Inhalte mit
altem Styling.

## Lokal ansehen

```
python -m http.server 8774 --directory web-demos/zeitblick-landing
```

oder `index.html` direkt im Browser öffnen.

## Nächste Schritte

- Lizenzprüfung in der App: Aktuell prüft Zeitblick nicht, ob ein Abo aktiv
  ist. Dafür wäre ein kleiner Server nötig, der bei Stripe nachfragt.
- Impressum mit echter Adresse, dann `noindex` entfernen.
