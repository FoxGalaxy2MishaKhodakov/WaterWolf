pyinstaller --noconfirm --onefile --windowed --icon "C:\Users\MihaB\Desktop\kak\src-low\icon.ico" --add-data "C:\Users\MihaB\Desktop\kak\src-installer\background.png;." --add-data "C:\Users\MihaB\Desktop\kak\src-installer\browser.zip;."  "C:\Users\MihaB\Desktop\kak\src-installer\installer.py"
xcopy "%~dp0dist\dist\installer.exe" "%~dp0ready\" /Y