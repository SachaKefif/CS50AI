@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0submit-cs50.ps1" %*
exit /b %ERRORLEVEL%
