@echo off
cd /d "%~dp0"
echo Checking virtual environment...
if exist venv\ (
    echo venv already exists, skipping creation.
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
)
echo.
echo Setup complete. Shortcut created on desktop.
echo Run launch.bat to start the app.
pause