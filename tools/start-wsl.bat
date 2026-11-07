@echo off
rem Double-click: opens an Ubuntu-24.04 (WSL) shell in the repository's Start-Kit folder.
wsl.exe -d Ubuntu-24.04 --cd "%~dp0..\Start-Kit"
if errorlevel 1 pause
