@echo off

set username=%USERNAME%
set target_directory="C:\Users\\%username%\\Desktop\\Attendance-System"
call C:/Users/%username%/anaconda3/Scripts/activate streamlit-env
taskkill /F /IM streamlit.exe

REM Wait for the web server to shut down 
tasklist | find /i "streamlit.exe" >nul 2>&1
if errorlevel 1 (
    goto clone_pull
) else (
    timeout /t 1 >nul
    goto waitloop
)

cd %target_directory%

:clone_pull
git pull origin main

streamlit run app.py --server.headless true
pause
