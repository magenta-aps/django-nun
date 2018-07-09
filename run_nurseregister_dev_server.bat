@echo off
call "%~dp0%configure_nurseregistersite.bat"
start python "%DJANGOPROJECT_ROOT_DIR%\manage.py" runserver 0.0.0.0:8000
