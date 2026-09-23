"""Echte Zeitblick-Screenshots mit BEISPIELDATEN fuer Werbung erzeugen.

Nimmt die echte App aus ../../zeitblick, fuettert sie mit einer erfundenen
Studenten-Woche (nie mit echten Tracking-Daten, die enthalten private
Fenstertitel) und fotografiert sie per headless Edge. Ergebnis in screens/:
app-week-de/en.png (Kalender) und app-stats-de/en.png (Statistik).

Aufruf: python app-screens.py   (danach render-ads.cmd fuer die X-Bilder)
"""
import json
import os
import random
import shutil
import subprocess
import tempfile
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, "..", "..", "zeitblick"))
OUT = os.path.join(HERE, "screens")
EDGE = os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")

WEEK_START = datetime(2026, 9, 14)      # Montag der gezeigten Woche
NOW = datetime(2026, 9, 20, 21, 40)     # "Jetzt" in den Screenshots (Sonntagabend)

# Fenstertitel je Aktivitaet (Browser-Titel steuern die Kategorie wie in echt)
T = {
    "mail":    ("chrome.exe", ["Inbox (4) - Gmail - Google Chrome", "University mail - Outlook - Google Chrome"]),
    "moodle":  ("chrome.exe", ["Moodle - Microeconomics I - Google Chrome", "Lecture 4 slides - Moodle - Google Chrome"]),
    "wiki":    ("chrome.exe", ["Opportunity cost - Wikipedia - Google Chrome", "Elasticity (economics) - Wikipedia - Google Chrome"]),
    "so":      ("chrome.exe", ["python - Parse JSON file - Stack Overflow - Google Chrome", "javascript - Array sort by date - Stack Overflow - Google Chrome"]),
    "mdn":     ("chrome.exe", ["Array.prototype.map() - JavaScript | MDN Web Docs - Google Chrome"]),
    "github":  ("chrome.exe", ["Pull requests - habit-app - GitHub - Google Chrome", "Issues - habit-app - GitHub - Google Chrome"]),
    "docs":    ("chrome.exe", ["Essay draft - Google Docs - Google Chrome", "Group project notes - Google Docs - Google Chrome"]),
    "reddit":  ("chrome.exe", ["r/productivity - Reddit - Google Chrome", "r/pcmasterrace - Reddit - Google Chrome"]),
    "insta":   ("chrome.exe", ["Instagram - Google Chrome"]),
    "yt":      ("chrome.exe", ["lofi hip hop radio - YouTube - Google Chrome", "How the economy works - YouTube - Google Chrome", "YouTube - Google Chrome"]),
    "netflix": ("chrome.exe", ["Netflix - Google Chrome"]),
    "code":    ("code.exe", ["app.js - habit-app - Visual Studio Code", "index.html - habit-app - Visual Studio Code", "server.py - habit-app - Visual Studio Code"]),
    "claude":  ("claude.exe", ["Claude"]),
    "word":    ("winword.exe", ["Seminar paper.docx - Word"]),
    "excel":   ("excel.exe", ["Budget 2026.xlsx - Excel"]),
    "anki":    ("anki.exe", ["Anki - Macroeconomics"]),
    "notes":   ("obsidian.exe", ["Lecture notes - Obsidian", "Weekly plan - Obsidian"]),
    "figma":   ("figma.exe", ["Portfolio site - Figma"]),
    "discord": ("discord.exe", ["#general | Study Group - Discord", "#valorant | Friends - Discord"]),
    "valo":    ("valorant-win64-shipping.exe", ["VALORANT"]),
    "cs":      ("cs2.exe", ["Counter-Strike 2"]),
    "spotify": ("spotify.exe", ["Spotify Premium"]),
    "files":   ("explorer.exe", ["Downloads", "Documents"]),
}

# Tagesablauf: (Startzeit, Minuten, Aktivitaet [, Zwischendurch-Aktivitaet])
PLAN = {
    0: [("08:40", 20, "mail"), ("09:02", 95, "code", "so"), ("10:40", 14, "reddit"),
        ("10:56", 70, "code", "github"), ("13:10", 55, "docs", "wiki"), ("14:08", 35, "moodle"),
        ("14:45", 18, "yt"), ("15:05", 45, "anki"), ("17:30", 25, "discord"),
        ("19:35", 115, "valo", "discord"), ("21:35", 30, "yt"), ("22:08", 15, "insta")],
    1: [("09:55", 18, "mail"), ("14:05", 80, "word", "wiki"), ("15:28", 20, "insta"),
        ("15:50", 40, "excel"), ("16:35", 25, "reddit"), ("19:10", 110, "netflix"),
        ("21:05", 65, "code", "claude"), ("22:15", 12, "discord")],
    2: [("08:35", 25, "mail", "moodle"), ("09:05", 110, "code", "mdn"), ("11:00", 12, "insta"),
        ("11:15", 50, "code", "claude"), ("13:20", 60, "docs", "wiki"), ("14:25", 22, "reddit"),
        ("14:50", 50, "notes", "moodle"), ("15:45", 25, "yt"), ("18:00", 20, "discord"),
        ("19:30", 130, "valo", "discord"), ("21:45", 25, "yt")],
    3: [("10:05", 15, "mail"), ("13:50", 90, "word", "wiki"), ("15:25", 15, "insta"),
        ("15:45", 45, "anki"), ("16:35", 20, "reddit"), ("17:00", 35, "code", "so"),
        ("19:20", 95, "netflix"), ("21:00", 40, "yt"), ("21:45", 20, "discord")],
    4: [("09:30", 120, "code", "github"), ("11:35", 20, "reddit"), ("14:10", 60, "figma"),
        ("15:15", 25, "insta"), ("15:45", 30, "spotify"), ("18:30", 15, "discord"),
        ("19:00", 150, "cs", "discord"), ("21:35", 60, "valo", "discord"), ("22:40", 20, "yt")],
    5: [("11:00", 40, "yt"), ("11:45", 20, "reddit"), ("13:30", 150, "valo", "discord"),
        ("16:10", 20, "insta"), ("16:35", 65, "figma"), ("17:45", 15, "discord"),
        ("20:00", 120, "netflix"), ("22:05", 20, "yt")],
    6: [("10:30", 25, "reddit"), ("10:58", 20, "insta"), ("11:20", 40, "notes"),
        ("14:00", 110, "code", "claude"), ("15:55", 12, "yt"), ("16:10", 45, "anki"),
        ("17:00", 20, "discord"), ("19:00", 60, "yt"), ("20:05", 30, "code", "so"),
        ("20:40", 58, "netflix")],
}


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%S")


def build_day(idx, rng):
    day = WEEK_START + timedelta(days=idx)
    sessions = []
    for entry in PLAN[idx]:
        start_s, minutes, main = entry[:3]
        side = entry[3] if len(entry) > 3 else None
        h, m = map(int, start_s.split(":"))
        t = day + timedelta(hours=h, minutes=m + rng.randint(-4, 4))
        end = t + timedelta(minutes=minutes * rng.uniform(0.9, 1.1))
        while t < end:
            # meistens die Hauptaktivitaet, ab und zu kurz etwas daneben
            key = side if side and rng.random() < 0.22 else main
            app, titles = T[key]
            length = timedelta(minutes=rng.uniform(2, 6) if key == side else rng.uniform(6, 22))
            s_end = min(t + length, end)
            sessions.append({"app": app, "title": rng.choice(titles), "start": iso(t), "end": iso(s_end)})
            t = s_end + timedelta(seconds=5)
            if rng.random() < 0.06:  # kurzer Blick in den Explorer
                f_end = t + timedelta(seconds=rng.randint(20, 50))
                sessions.append({"app": "explorer.exe", "title": rng.choice(T["files"][1]), "start": iso(t), "end": iso(f_end)})
                t = f_end + timedelta(seconds=5)
    sessions = [s for s in sessions if s["start"] < iso(NOW)]
    for s in sessions:
        s["end"] = min(s["end"], iso(NOW - timedelta(seconds=30)))
    last = datetime.fromisoformat(sessions[-1]["end"]) if sessions else day
    generated = NOW - timedelta(seconds=30) if day.date() == NOW.date() else last
    return {"date": day.strftime("%Y-%m-%d"), "generated": iso(generated), "sessions": sessions}


# Vor app.js: Uhr auf NOW stellen und Ansicht/Sprache aus der URL setzen
SHIM = """<script>
(function () {
  var p = new URLSearchParams(location.search);
  var RealDate = Date, offset = new RealDate("%s").getTime() - RealDate.now();
  class FakeDate extends RealDate {
    constructor(...a) { if (a.length) super(...a); else super(RealDate.now() + offset); }
    static now() { return RealDate.now() + offset; }
  }
  window.Date = FakeDate;
  var set = function (k, v) { localStorage.setItem(k, JSON.stringify(v)); };
  set("zeitblick.lang", p.get("lang") || "de");
  set("zeitblick.view", p.get("view") || "kalender");
  set("zeitblick.statsPeriod", "woche");
  set("zeitblick.sidebarTab", "ansicht");
  set("zeitblick.fokusTabSeen", true);
  set("zeitblick.detail", "min1");
  set("zeitblick.colorMode", "kategorie");
  set("zeitblick.hourH", 48);
})();
</script>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    work = tempfile.mkdtemp(prefix="zeitblick-demo-")
    try:
        for name in ("app.js", "style.css"):
            shutil.copy2(os.path.join(APP, name), work)
        with open(os.path.join(APP, "index.html"), encoding="utf-8") as f:
            html = f.read()
        html = html.replace('<script src="app.js"></script>', SHIM % iso(NOW) + '<script src="app.js"></script>')
        with open(os.path.join(work, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        with open(os.path.join(work, "categories.json"), "w", encoding="utf-8") as f:
            json.dump({"apps": {}}, f)
        os.makedirs(os.path.join(work, "data"))
        for idx in range(7):
            day = build_day(idx, random.Random(1000 + idx))
            with open(os.path.join(work, "data", day["date"] + ".json"), "w", encoding="utf-8") as f:
                json.dump(day, f)

        url = "file:///" + work.replace("\\", "/") + "/index.html"
        for lang in ("de", "en"):
            for view, name in (("kalender", "week"), ("statistik", "stats")):
                target = os.path.join(OUT, f"app-{name}-{lang}.png")
                subprocess.run([
                    EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--force-device-scale-factor=2",
                    "--virtual-time-budget=6000", "--window-size=1600,1000",
                    f"--user-data-dir={os.path.join(work, 'profile-' + lang + view)}",
                    f"--screenshot={target}", f"{url}?lang={lang}&view={view}",
                ], check=True, capture_output=True)
                print("OK", target)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
