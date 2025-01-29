@echo off
setlocal

REM Set the virtual environment folder name
set VENV_DIR=venv

REM Check if the virtual environment exists, if not, create it
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM Activate the virtual environment
call %VENV_DIR%\Scripts\activate

REM Check if requirements are installed
echo Checking dependencies...
pip freeze > installed_requirements.txt
fc installed_requirements.txt requirements.txt > nul
if %errorlevel% neq 0 (
    echo Installing missing dependencies...
    pip install -r requirements.txt
) else (
    echo All dependencies are already installed.
)

REM Run the Python script
echo Running menu.py...
python menu.py

REM End script
endlocal