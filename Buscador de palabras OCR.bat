@echo off
chcp 1252 >nul
title ANALIZADOR OCR UNIVERSAL - Configuracion
color 0B

echo.
echo ========================================
echo   ANALIZADOR OCR UNIVERSAL
echo ========================================
echo.
echo Iniciando configuracion automatica...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   PYTHON NO ENCONTRADO
    echo ========================================
    echo.
    echo PYTHON es requerido para ejecutar esta aplicacion.
    echo.
    echo INSTRUCCIONES DE INSTALACION:
    echo   1. Vaya a: https://www.python.org/downloads/
    echo   2. Descargue Python 3.8 o superior
    echo   3. Durante la instalacion, marque:
    echo      - "Add Python to PATH"
    echo      - "Install for all users"
    echo   4. Reinicie su computadora
    echo   5. Ejecute este archivo nuevamente
    echo.
    echo Presione cualquier tecla para abrir la pagina de descarga...
    pause >nul
    start https://www.python.org/downloads/
    echo.
    echo Vuelva a ejecutar este archivo despues de instalar Python.
    echo.
    pause
    exit /b 1
)

python --version
echo Python encontrado correctamente.
echo.

echo [2/4] Configurando entorno OCR...
REM Configurar PATH y TESSDATA_PREFIX
set "PATH=%PATH%;C:\Program Files\Tesseract-OCR"
set "PATH=%PATH%;%~dp0poppler\Library\bin"
set "TESSDATA_PREFIX=%~dp0tessdata"
echo Rutas configuradas.
echo.

echo [3/4] Verificando e instalando dependencias Python...
python "%~dp0instalador_automatico.py" --auto

REM Verificar que la instalacion fue exitosa
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   ERROR EN INSTALACION
    echo ========================================
    echo.
    echo No se pudieron instalar las dependencias automaticamente.
    echo.
    echo SOLUCIONES:
    echo   1. Verificar conexion a internet
    echo   2. Ejecutar como administrador
    echo   3. Instalar manualmente:
    echo      pip install PyPDF2 openpyxl pytesseract pdf2image
    echo.
    pause
    exit /b 1
)

echo Dependencias verificadas correctamente.
echo.

echo [4/4] Iniciando aplicacion GUI...
echo.
echo La ventana se cerrara automaticamente cuando
echo la aplicacion grafica este lista...
echo.

REM Ejecutar la aplicacion GUI y cerrar ventana automaticamente
if exist "C:\Users\matia\AppData\Local\Programs\Python\Python312\pythonw.exe" (
    start "" "C:\Users\matia\AppData\Local\Programs\Python\Python312\pythonw.exe" gui_analizador_ocr_universal.py
) else (
    start "" pythonw gui_analizador_ocr_universal.py
)

REM Esperar un momento para que se inicie la GUI y luego cerrar
timeout /t 3 /nobreak >nul
exit