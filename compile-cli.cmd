pyinstaller --noconfirm --onedir --windowed --add-data "%~dp0src-low\script.js;." --add-data "%~dp0src-low\start_page.html;." --add-data "%~dp0src-low\styles.css;." --add-data "%~dp0src-low\config.ini;."  "%~dp0src-low\browser.py"
xcopy "%~dp0src-low\update.bat" "%~dp0dist\browser\" /Y

