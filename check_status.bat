@echo off
title Telegram Premium Emoji Bot Status
cd /d "%~dp0"
echo Checking bot status...
powershell -Command "
$procs = Get-CimInstance Win32_Process -Filter \"Name like 'python%' and CommandLine like '%%telegram primum emoji bot%%'\"
if ($procs) {
    Write-Host '>>> BOT IS RUNNING ONLINE! <<<' -ForegroundColor Green
    $procs | Select-Object ProcessId, CommandLine | Format-Table -AutoSize
} else {
    Write-Host '>>> BOT IS CURRENTLY STOPPED <<<' -ForegroundColor Red
}
"
pause

