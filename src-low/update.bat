@echo off

:: Отключаем процесс browser.exe, если он запущен
taskkill /f /im browser.exe

:: Пауза на несколько секунд, чтобы убедиться, что процесс завершен
timeout /t 3 /nobreak >nul

:: Распаковываем архив update.zip в текущую директорию с заменой файлов
powershell -Command "Expand-Archive -Path 'update.zip' -DestinationPath '.' -Force"

:: Запускаем файл browser.exe из текущей директории
start "" "%cd%\browser.exe"

:: Завершаем работу скрипта
exit
