@echo off
rem Price run: fetch, rebuild the page, publish.
rem
rem   run_weekly.cmd              fetch now, whatever the date
rem   run_weekly.cmd /ifstale     fetch only if the page predates the last
rem                               Wednesday 7am reset (what the task uses)
rem
rem The scheduled task fires daily and passes /ifstale, so whichever day the
rem machine is first awake after a Wednesday reset brings the page up to date
rem and every other run costs nothing. That is deliberate: Windows does not
rem reliably run a weekly task it missed while the machine was asleep. It
rem dropped the 23 September run and moved the next one a week out.
rem
rem Fetching must happen on this machine: Woolworths refuses requests from
rem data centre addresses, so this cannot run on a server.

setlocal
cd /d "%~dp0"
if not exist logs mkdir logs

set GUARD=
if /i "%~1"=="/ifstale" set GUARD=--if-stale

for /f "tokens=1-3 delims=/" %%a in ("%DATE:* =%") do set TODAY=%%c-%%b-%%a
set LOG=logs\run-%TODAY%.log

echo ==== run started %DATE% %TIME% %GUARD% ==== >> "%LOG%"

python fetch_prices.py %GUARD% >> "%LOG%" 2>&1
if errorlevel 1 (
  echo FETCH FAILED with code %ERRORLEVEL% >> "%LOG%"
  echo Fetch failed. See %LOG%
  exit /b 1
)

git add docs >> "%LOG%" 2>&1
git diff --cached --quiet
if not errorlevel 1 (
  echo nothing to publish >> "%LOG%"
  echo Done. Page already current.
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
