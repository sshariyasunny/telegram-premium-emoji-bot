@echo off
title Restarting Telegram Premium Emoji Bot
cd /d "%~dp0"
echo Stopping old instances...
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name like 'python%' and CommandLine like '%%telegram primum emoji bot%%'\" | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
timeout /t 1 >nul
echo Starting fresh instance...
start "" pythonw main.py
echo Bot restarted successfully!
timeout /t 2 >nul
exit

