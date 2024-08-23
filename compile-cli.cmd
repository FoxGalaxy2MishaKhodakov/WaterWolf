pyinstaller --noconfirm --onedir --windowed --add-data "C:\Users\MihaB\Desktop\kak\src-low\icons;icons/" --add-data "C:\Users\MihaB\Desktop\kak\src-low\config.ini;." --add-data "C:\Users\MihaB\Desktop\kak\src-low\script.js;." --add-data "C:\Users\MihaB\Desktop\kak\src-low\start_page.html;." --add-data "C:\Users\MihaB\Desktop\kak\src-low\styles.css;."  "C:\Users\MihaB\Desktop\kak\src-low\browser.py"
xcopy "%~dp0src-low\update.bat" "%~dp0dist\browser\" /Y

