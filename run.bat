@echo off
REM Face Recognition System - Windows Batch File
cls

echo ================================
echo Face Recognition System Setup
echo ================================
echo.

REM Check Python
echo 1 - Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    pause
    exit /b 1
)
echo OK - Python found
echo.

REM Install dependencies
echo 2 - Installing dependencies...
pip install -r requirements.txt
echo OK - Dependencies installed
echo.

:menu
cls
echo ================================
echo MENU CHINH
echo ================================
echo 1. Thu thap du lieu khuon mat (collect_data.py)
echo 2. Huan luyen mo hinh (train.py)
echo 3. Nhan dien khuon mat (recognition.py)
echo 4. Xem huong dan (README.md)
echo 5. Thoat
echo.
set /p choice="Chon tuy chon (1-5): "

if "%choice%"=="1" (
    echo Chay thu thap du lieu...
    python collect_data.py
    pause
    goto menu
)
if "%choice%"=="2" (
    echo Chay huan luyen mo hinh...
    python train.py
    pause
    goto menu
)
if "%choice%"=="3" (
    echo Chay nhan dien khuon mat...
    python recognition.py
    pause
    goto menu
)
if "%choice%"=="4" (
    echo Mo README.md...
    type README.md
    pause
    goto menu
)
if "%choice%"=="5" (
    echo Tam biet!
    exit /b 0
)

echo ERROR: Tuy chon khong hop le!
pause
goto menu
