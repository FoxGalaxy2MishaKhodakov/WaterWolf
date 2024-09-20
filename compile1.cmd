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
