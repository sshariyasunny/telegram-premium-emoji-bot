@echo off
title Stopping Telegram Premium Emoji Bot
cd /d "%~dp0"
echo ========================================================
echo    Stopping Telegram Premium Emoji Bot...
echo ========================================================
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name like 'python%' and CommandLine like '%%telegram primum emoji bot%%'\" | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host \"Terminated process PID: $($_.ProcessId)\" }"
echo Done!
timeout /t 2 >nul
exit

