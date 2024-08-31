:: Создание дистрибутива приложения
pyinstaller --noconfirm --onedir --windowed --icon "%~dp0src-low\icon.ico" --add-data "%~dp0src-low\icons;icons/" --add-data "%~dp0src-low\script.js;." --add-data "%~dp0src-low\icon.ico;." --add-data "%~dp0src-low\start_page.html;." --add-data "%~dp0src-low\styles.css;." --add-data "%~dp0src-low\background.jpg;." --add-data "%~dp0src-low\config.ini;."  "%~dp0src-low\browser.py"

:: Копирование файла update.bat в папку browser
xcopy "%~dp0src-low\update.bat" "%~dp0dist\browser\" /Y

:: Переход в директорию с файлами
cd /d "C:\Users\MihaB\Desktop\kak\dist\browser"

:: Архивация папки _internal и файла browser.exe в update.zip
powershell Compress-Archive -Path "_internal", "browser.exe" -DestinationPath "C:\Users\MihaB\Desktop\kak\ready\update.zip"

:: Архивация всей папки browser в browser.zip
cd ..
powershell Compress-Archive -Path "browser" -DestinationPath "C:\Users\MihaB\Desktop\kak\src-installer\browser.zip"
