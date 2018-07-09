@echo off

REM set root dir
set DJANGOPROJECT_ROOT_DIR=%~dp0%

REM load virtual env
call "%DJANGOPROJECT_ROOT_DIR%venv\Scripts\activate"

:finish
REM tell django which file to use for settings
SET DJANGO_SETTINGS_MODULE=nurseregistersite.settings
