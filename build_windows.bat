@echo off
REM Build script for Windows

REM Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller could not be found. Please install it with: pip install pyinstaller
    pause
    exit /b
)

echo Cleaning previous build...
rmdir /s /q build dist
del /q *.spec

echo Building Windows executable...
REM --onefile: Single exe
REM --windowed: No console
REM --icon: Add an icon if you have one (skipping for now)

pyinstaller --noconfirm --onefile --windowed --name "Punjab_Chakki" ^
    --hidden-import "PIL" ^
    --hidden-import "PIL._tkinter_finder" ^
    --collect-all "tkinter" ^
    --collect-all "ui" ^
    main.py

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b
)

echo Build complete. Executable is in dist/Punjab_Chakki.exe
echo IMPORTANT: Make sure 'punjab_chakki.db' is in the same directory as the .exe
pause
