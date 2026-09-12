@echo off
rem Weekly price run. Scheduled for Wednesday morning, when Australian
rem supermarket specials reset. Also safe to double-click any time.
rem
rem Fetching must happen on this machine: Woolworths refuses requests from
rem data centre addresses, so this cannot run on a server.

setlocal
cd /d "%~dp0"
if not exist logs mkdir logs

set STAMP=%DATE:/=-%
set LOG=logs\run-%STAMP: =_%.log

echo ==== run started %DATE% %TIME% ==== >> "%LOG%"
python fetch_prices.py >> "%LOG%" 2>&1
set RESULT=%ERRORLEVEL%

if not "%RESULT%"=="0" (
  echo fetch failed with code %RESULT% >> "%LOG%"
  echo Fetch failed. See "%LOG%".
  exit /b %RESULT%
)

rem Publish the rebuilt page. Nothing else in the repository should have
rem changed, so a quiet commit is expected.
git add docs
git diff --cached --quiet && (
  echo no price changes this run >> "%LOG%"
) || (
  git commit -m "Prices for %DATE%" >> "%LOG%" 2>&1
  git push >> "%LOG%" 2>&1
  if not "%ERRORLEVEL%"=="0" echo push failed >> "%LOG%"
)

echo ==== run finished %DATE% %TIME% ==== >> "%LOG%"
endlocal
