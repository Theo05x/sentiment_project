# Script para lanzar FastAPI + Streamlit en paralelo (Windows PowerShell)
# Uso: .\scripts\run_dev.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Sentiment Analysis Dashboard - Dev Server" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-Not (Test-Path "app\main.py")) {
    Write-Host "Error: Este script debe ejecutarse desde la raiz del proyecto" -ForegroundColor Red
    exit 1
}

# Verificar que el entorno virtual está activado
if ($null -eq $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Advertencia: Entorno virtual no detectado" -ForegroundColor Yellow
    Write-Host "   Actívalo con: venv\Scripts\activate" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Iniciando servicios..." -ForegroundColor Green
Write-Host ""

# Lanzar FastAPI en background
Write-Host "[1/2] Iniciando FastAPI en http://127.0.0.1:8000" -ForegroundColor Yellow
$backendJob = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList "-m uvicorn app.main:app --reload --port 8000"
$backendPID = $backendJob.Id
Write-Host "      PID: $backendPID" -ForegroundColor Gray

# Esperar un poco para que FastAPI se inicie
Start-Sleep -Seconds 3

# Lanzar Streamlit
Write-Host "[2/2] Iniciando Streamlit en http://localhost:8501" -ForegroundColor Yellow
$frontendJob = Start-Process -NoNewWindow -PassThru -FilePath "streamlit" -ArgumentList "run frontend/app.py --logger.level=info"
$frontendPID = $frontendJob.Id
Write-Host "      PID: $frontendPID" -ForegroundColor Gray

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "  Servicios iniciados correctamente" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Frontend (Streamlit):  http://localhost:8501" -ForegroundColor Cyan
Write-Host "⚡ Backend (FastAPI):     http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "📖 API Docs:             http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener todos los servicios" -ForegroundColor Yellow
Write-Host ""

# Esperar a que los procesos terminen (Ctrl+C)
try {
    Wait-Process -Id $backendPID, $frontendPID
} catch {
    Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
    Stop-Process -Id $backendPID -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $frontendPID -Force -ErrorAction SilentlyContinue
    Write-Host "Servicios detenidos" -ForegroundColor Green
}
