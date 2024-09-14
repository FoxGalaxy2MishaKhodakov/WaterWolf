@echo off

:: Отключаем процесс browser.exe, если он запущен
taskkill /f /im browser.exe

:: Пауза на несколько секунд, чтобы убедиться, что процесс завершен
timeout /t 3 /nobreak >nul

:: Распаковываем архив update.zip в текущую директорию с заменой файлов
powershell -Command "Expand-Archive -Path 'update.zip' -DestinationPath '.' -Force"

:: Проверяем, была ли распаковка успешной
if %errorlevel% neq 0 (
    echo Ошибка при распаковке файла update.zip
    exit /b %errorlevel%
)

:: Удаляем файл update.zip после успешной распаковки
del "update.zip"

:: Проверяем, была ли операция удаления успешной
if %errorlevel% neq 0 (
    echo Ошибка при удалении файла update.zip
    exit /b %errorlevel%
)

:: Запускаем файл browser.exe из текущей директории
start "" "%cd%\browser.exe"

:: Завершаем работу скрипта
exit
