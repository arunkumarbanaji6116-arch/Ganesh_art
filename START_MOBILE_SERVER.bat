@echo off
cd /d "%~dp0"
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM cloudflared.exe >nul 2>&1
del cf_active.log >nul 2>&1

start "Ganesh Node Server" /min node server.js
start "Ganesh Cloudflare Tunnel" /min cloudflared.exe tunnel --url http://127.0.0.1:8080 --logfile "%~dp0cf_active.log"

