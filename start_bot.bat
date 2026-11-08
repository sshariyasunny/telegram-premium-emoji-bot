@echo off
title Telegram Premium Emoji Bot Launcher
cd /d "%~dp0"
echo ========================================================
echo    Starting Telegram Premium Emoji Bot (Silent Mode)
echo ========================================================
start "" pythonw main.py
echo Bot started in background!
timeout /t 3 >nul
exit
