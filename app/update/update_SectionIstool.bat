@echo off

set "SCRIPT_DIR=%~dp0..\.."

timeout /t 3

xcopy /E /I /Y "%SCRIPT_DIR%\app\update\SectionIstool_update_temp\*" "%SCRIPT_DIR%\"
rmdir /S /Q "%SCRIPT_DIR%\app\update\SectionIstool_update_temp"

cd /d "%SCRIPT_DIR%"

start "" "SectionIstool.exe"
