@echo off
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%job_search.py"

echo Creating scheduled task...
schtasks /create /tn "DailyJobSearch" /tr "python \"%PYTHON_SCRIPT%\"" /sc daily /st 12:00 /f

if %errorlevel% equ 0 (
    echo Task created successfully!
) else (
    echo Failed to create task. Please run as Administrator.
)
pause
