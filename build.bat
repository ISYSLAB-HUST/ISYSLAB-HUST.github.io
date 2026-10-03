@echo off
REM ============================================================
REM  iSyslab site - rebuild the site into _site\
REM  Run this after editing anything under content\.
REM ============================================================
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY where python >nul 2>nul && set "PY=python"

if not defined PY (
  echo.
  echo   Python 3 was not found on PATH.
  echo   Install it from https://www.python.org/downloads/
  echo   and remember to tick "Add python.exe to PATH" during setup.
  echo.
  pause
  exit /b 1
)

%PY% "tools\build.py" %*
echo.
pause
