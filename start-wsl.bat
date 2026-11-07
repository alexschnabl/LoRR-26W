@echo off
rem Double-click: opens an Ubuntu-24.04 (WSL) shell in this project's Start-Kit folder.
rem First launch asks you to create your Linux username and password.
wsl.exe -d Ubuntu-24.04 --cd "%~dp0Start-Kit"
if errorlevel 1 pause
