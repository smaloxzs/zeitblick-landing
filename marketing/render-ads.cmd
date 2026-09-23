@echo off
rem Rendert die Werbebilder aus ad.html per headless Edge als PNG.
rem Aufruf: Doppelklick. Deutsch: hier, Englisch: in en\, Link-Vorschauen im Website-Ordner.
setlocal
cd /d "%~dp0"
if not exist en mkdir en
set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
set "SRC=file:///%CD:\=/%/ad.html"
set "OPTS=--headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=8000"

rem Deutsch
"%EDGE%" %OPTS% --window-size=1200,630  --screenshot="%CD%\..\og-image.png"         "%SRC%?f=og"
"%EDGE%" %OPTS% --window-size=1080,1350 --screenshot="%CD%\instagram-post-1.png"    "%SRC%?f=post"
"%EDGE%" %OPTS% --window-size=1080,1350 --screenshot="%CD%\instagram-post-2.png"    "%SRC%?f=carousel"
"%EDGE%" %OPTS% --window-size=1080,1920 --screenshot="%CD%\story.png"               "%SRC%?f=story"

rem Englisch
"%EDGE%" %OPTS% --window-size=1200,630  --screenshot="%CD%\..\og-image-en.png"      "%SRC%?f=og&lang=en"
"%EDGE%" %OPTS% --window-size=1080,1350 --screenshot="%CD%\en\post-1.png"           "%SRC%?f=post&lang=en"
"%EDGE%" %OPTS% --window-size=1080,1350 --screenshot="%CD%\en\post-2.png"           "%SRC%?f=carousel&lang=en"
"%EDGE%" %OPTS% --window-size=1080,1920 --screenshot="%CD%\en\story.png"            "%SRC%?f=story&lang=en"
"%EDGE%" %OPTS% --window-size=1270,760  --screenshot="%CD%\en\producthunt-gallery.png" "%SRC%?f=ph&lang=en"
"%EDGE%" %OPTS% --window-size=480,480   --screenshot="%CD%\en\producthunt-thumbnail.png" "%SRC%?f=thumb"
echo Fertig.
