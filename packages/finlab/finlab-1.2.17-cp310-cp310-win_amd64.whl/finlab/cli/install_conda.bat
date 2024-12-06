@echo off

:install_conda
REM Check if conda is already installed
where conda >nul 2>nul
if %errorlevel%==0 (
    echo Conda is already installed. Skipping installation.
    goto :eof
)

REM Download and install Miniconda
echo Detected Windows OS.
curl -o miniconda.exe https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
start /wait "" miniconda.exe /S /D=%UserProfile%\miniconda3
del miniconda.exe

REM Add Miniconda to PATH
setx PATH "%UserProfile%\miniconda3\Scripts;%UserProfile%\miniconda3;%PATH%"

REM Initialize Conda for the Command Prompt
call %UserProfile%\miniconda3\Scripts\activate.bat

echo Conda installation completed or was already installed. Please restart your terminal.


