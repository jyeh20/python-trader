@echo off
:: Get the day of the week (0 for Sunday, 1 for Monday, ..., 6 for Saturday)
for /f "tokens=1-2 delims==" %%A in ('wmic path win32_localtime get dayofweek /format:list') do (
    if "%%A"=="DayOfWeek" set DOW=%%B
)

set PATH_TO_VENV="..\env"
SET PATH_TO_REQUIREMENTS=".\requirements.txt"
SET PATH_TO_STOCK_ANALYZER="..\stock_analysis.py"

:: Check if the day is a weekday (Monday=1 to Friday=5)
if %DOW% geq 1 if %DOW% leq 5 (
    :: Check if virtual environment directory exists
    if not exist %PATH_TO_VENV% (
        :: Create virtual environment
        python -m venv %PATH_TO_VENV%
        :: Activate virtual environment and install dependencies
        call %PATH_TO_VENV%\Scripts\activate
        pip install -r %PATH_TO_REQUIREMENTS%
        deactivate
    )
    :: Activate virtual environment
    call %PATH_TO_VENV%\Scripts\activate
    :: Launch the Python script
    python %PATH_TO_STOCK_ANALYZER%
    :: Deactivate virtual environment
    deactivate
) else (
    echo Today is not a weekday. The script will not run.
)
