@echo off
rem Weekly price run. Scheduled for Wednesday morning, when Australian
rem supermarket specials reset. Also safe to double-click any time.
rem
rem Fetching must happen on this machine: Woolworths refuses requests from
rem data centre addresses, so this cannot run on a server.

setlocal enabledelayedexpansion
cd /d "%~dp0"
if not exist logs mkdir logs

for /f "tokens=1-3 delims=/" %%a in ("%DATE:* =%") do set TODAY=%%c-%%b-%%a
set LOG=logs\run-%TODAY%.log

echo ==== run started %DATE% %TIME% ==== >> "%LOG%"

python fetch_prices.py >> "%LOG%" 2>&1
if errorlevel 1 (
  echo FETCH FAILED with code %ERRORLEVEL% >> "%LOG%"
  echo Fetch failed. See %LOG%
  exit /b 1
)

rem Publish the rebuilt page. Only docs/ should have changed.
git add docs >> "%LOG%" 2>&1
git diff --cached --quiet
if not errorlevel 1 (
  echo no change to publish >> "%LOG%"
  echo Done. No price changes this run.
  echo ==== run finished %DATE% %TIME% ==== >> "%LOG%"
  exit /b 0
)

git commit -m "Prices for %TODAY%" >> "%LOG%" 2>&1
if errorlevel 1 (
  echo COMMIT FAILED with code %ERRORLEVEL% >> "%LOG%"
  echo Commit failed. See %LOG%
  exit /b 1
)

git push >> "%LOG%" 2>&1
if errorlevel 1 (
  echo PUSH FAILED with code %ERRORLEVEL% >> "%LOG%"
  echo Page rebuilt and committed, but the push failed. See %LOG%
  exit /b 1
)

echo published >> "%LOG%"
echo Done. Page rebuilt and published.
echo ==== run finished %DATE% %TIME% ==== >> "%LOG%"
endlocal
