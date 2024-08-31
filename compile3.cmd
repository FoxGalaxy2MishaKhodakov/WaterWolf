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