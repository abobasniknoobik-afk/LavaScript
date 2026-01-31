@echo off
title LavaScript Installer
echo 🌋 Установка LavaScript для Windows...

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден! Установи его с python.org
    pause
    exit
)

:: Регистрация расширения .ls
set ENGINE_PATH=%~dp0engine.py
assoc .ls=LavaScript
ftype LavaScript=python.exe "%ENGINE_PATH%" "%%1" %%*

echo 🌋 Готово! Теперь файлы .ls открываются через LavaScript.
pause
