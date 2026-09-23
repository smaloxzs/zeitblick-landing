@echo off
rem Rendert die Werbebilder aus ad.html per headless Edge als PNG.
rem Aufruf: Doppelklick. Ergebnis: og-image.png im Website-Ordner, Rest hier.
setlocal
cd /d "%~dp0"
set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
set "SRC=file:///%CD:\=/%/ad.html"
set "OPTS=--headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=8000"

"%EDGE%" %OPTS% --window-size=1200,630  --screenshot="%CD%\..\og-image.png"         "%SRC%?f=og"
"%EDGE%" %OPTS% --window-size=1080,1350 --screenshot="%CD%\instagram-post-1.png"    "%SRC%?f=post"
"%EDGE%" %OPTS% --window-size=1080,1350 --screenshot="%CD%\instagram-post-2.png"    "%SRC%?f=carousel"
"%EDGE%" %OPTS% --window-size=1080,1920 --screenshot="%CD%\story.png"               "%SRC%?f=story"
echo Fertig.
