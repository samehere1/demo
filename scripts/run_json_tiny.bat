@echo off
setlocal
REM Run the PowerShell script and keep the window open so viewers see success/errors
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_json_tiny.ps1"
echo(
echo Press any key to close...
pause >nul
endlocal
