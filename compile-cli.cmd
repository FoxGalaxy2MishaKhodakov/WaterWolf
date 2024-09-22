@echo off
color 2

pip install -r "%~dp0requirements.txt"

:: Создание дистрибутива приложения
pyinstaller --noconfirm --onedir --windowed --icon "%~dp0src-low\icon.ico" --add-data "%~dp0src-low\icons;icons/" --add-data "%~dp0src-low\script.js;." --add-data "%~dp0src-low\password.txt;." --add-data "%~dp0src-low\icon.ico;." --add-data "%~dp0src-low\start_page.html;." --add-data "%~dp0src-low\styles.css;." --add-data "%~dp0src-low\background.jpg;." --add-data "%~dp0src-low\config.ini;."  "%~dp0src-low\browser.py"

:: Копирование файла update.bat и black-web.txt в папку browser
xcopy "%~dp0src-low\update.bat" "%~dp0dist\browser\" /Y
xcopy "%~dp0src-low\black-web.txt" "%~dp0dist\browser\" /Y

:: Переход в директорию с файлами
cd /d "C:\Users\MihaB\Desktop\kak\dist\browser"

:: Архивация папки _internal и файла browser.exe с black-web.txt в update.zip
powershell Compress-Archive -Path "_internal", "browser.exe", "black-web.txt" -DestinationPath "C:\Users\MihaB\Desktop\kak\ready\update.zip"

:: Архивация всей папки browser в browser.zip
cd ..
powershell Compress-Archive -Path "browser" -DestinationPath "C:\Users\MihaB\Desktop\kak\src-installer\browser.zip"

pyinstaller --noconfirm --onefile --windowed --icon "C:\Users\MihaB\Desktop\kak\src-low\icon.ico" --add-data "C:\Users\MihaB\Desktop\kak\src-installer\background.png;." --add-data "C:\Users\MihaB\Desktop\kak\src-installer\browser.zip;."  "C:\Users\MihaB\Desktop\kak\src-installer\installer.py"
xcopy "%~dp0dist\dist\installer.exe" "%~dp0ready\" /Y

if exist "build" (
    rd /s /q "build"
    echo Папка build успешно удалена.
) else (
    echo Папка build не найдена.
)

REM Удаление папки dist, если она существует
if exist "dist" (
    rd /s /q "dist"
    echo Папка dist успешно удалена.
) else (
    echo Папка dist не найдена.
)

cd ..

if exist "build" (
    rd /s /q "build"
    echo Папка build успешно удалена.
) else (
    echo Папка build не найдена.
)

REM Удаление папки dist, если она существует
if exist "dist" (
    rd /s /q "dist"
    echo Папка dist успешно удалена.
) else (
    echo Папка dist не найдена.
)

REM Удаление файла browser.spec, если он существует
if exist "browser.spec" (
    del /q "browser.spec"
    echo Файл browser.spec успешно удалён.
) else (
    echo Файл browser.spec не найден.
)

cd src-installer

REM Удаление файла browser.zip, если он существует
if exist "browser.zip" (
    del /q "browser.zip"
    echo Файл browser.zip успешно удалён.
) else (
    echo Файл browser.zip не найден.
)

echo WaterWolf was compiled successfully
pause
