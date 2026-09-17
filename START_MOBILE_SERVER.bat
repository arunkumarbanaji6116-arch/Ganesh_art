@echo off
cd /d "%~dp0"
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM cloudflared.exe >nul 2>&1
del cf_active.log >nul 2>&1

start "Ganesh Node Server" /min node server.js
start "Ganesh Mobile Tunnel" /min cmd /c npx -y localtunnel --port 8080 --subdomain arun-ganesh-art

